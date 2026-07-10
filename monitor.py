# ============================================================
# PlatformPatcher
#
# Minecraft 后台监听模块
#
# 功能：
# 1. 等待 Minecraft 窗口出现
# 2. 自动执行注入
# 3. 注入后等待 Minecraft 关闭
# 4. 关闭后重新等待下一次启动
#
# ============================================================
from time import sleep

from PySide6.QtCore import (
    QThread,
    Signal
)

import threading
import time


from file_state import save_new_path, clear_new_path
from file_state import (
    load_old_path,
    save_old_path,
    normalize
)

from patch_manager import get_patcher

from window_detector import (
    find_target_window
)

from notifier import (
    success,
    warning,
    error
)

from logger import (
    info,
    error as log_error
)

from file_detector import (
    get_latest_file,
    get_folder_id
)
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QTimer


class MinecraftMonitor(QThread):


    # 日志信号

    log_signal = Signal(str)

    popup_signal = Signal(str, str)

    finished_signal = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.old_id = None
        self.new_path = None

        self.old_file = None

        self.current_new_file = None

        self.wait_new_file = False

        self.running = False

        self.injected = False

        # 防止重复启动

        self.lock = threading.Lock()

        # 停止事件

        self.stop_event = threading.Event()

        # Minecraft消失确认次数

        self.window_lost_count = 0

        self.patcher = get_patcher()

    def prepare_old_path(self):

        path = get_latest_file()

        if path:
            self.old_id = get_folder_id(
                path
            )

            self.log(
                f"已记录旧文件ID:{self.old_id}"
            )

            success(
                "已存入旧文件路径\n等待新的布吉岛文件生成..."
            )

    def check_new_file(self):

        path = get_latest_file()

        if not path:
            return None

        current_id = get_folder_id(
            path
        )

        if current_id != self.old_id:
            self.new_path = path

            self.log(
                f"检测到新文件ID:{current_id}"
            )

            success(
                "已检测到新的文件路径\n正在执行注入..."
            )

            self.stop_event.wait(3)

            success(
                "已注入完成！\n请重启布吉岛",15000
            )

            return path

        return None

    def prepare_old_file(self):

        old = load_old_path()

        if old:

            self.old_file = normalize(old)

            self.log(
                "已存入旧文件路径，等待新文件路径..."
            )

            self.popup_signal.emit(
                "PlatformPatcher",
                "已存入旧文件路径\n等待新的布吉岛文件路径生成..."
            )


        else:

            self.log(
                "暂无历史文件路径，等待首次生成..."
            )




    def log(self, message):


        self.log_signal.emit(
            message
        )


        info(
            message
        )

    def start_monitor(self):

        with self.lock:
            if self.isRunning():
                self.log(
                    "监听线程已经运行"
                )

                return

            self.prepare_old_path()

            self.running = True

            self.start()


    def stop_monitor(self):

        self.log(
            "正在停止后台监听进程..."
        )

        self.running = False

        self.stop_event.set()

        if self.isRunning():

            self.wait(
                3000
            )


        else:

            self.log(
                "后台监听进程已退出"
            )





    def run(self):

        self.log(
            "Minecraft监听模式已启动"
        )

        try:

            while self.running:

                # ==================================================
                # 状态1：
                # 等待 Minecraft 出现
                # ==================================================

                if not self.injected:

                    self.log(
                        "正在等待Minecraft窗口..."
                    )

                    while self.running and not self.injected:

                        hwnd = find_target_window()

                        if hwnd:

                            new_file = self.check_new_file()

                            if new_file:
                                self.current_new_file = new_file

                                self.inject()


                        else:

                            self.window_lost_count += 1

                        self.stop_event.wait(2)



                # ==================================================
                # 状态2：
                # 已注入
                # 等待 Minecraft 消失
                # ==================================================

                else:

                    self.log(
                        "等待Minecraft关闭..."
                    )


                    while self.running and self.injected:

                        hwnd = find_target_window()

                        if not hwnd:

                            self.window_lost_count += 1

                            if self.window_lost_count >= 3:

                                if self.current_new_file:
                                    save_old_path(
                                        self.current_new_file
                                    )

                                    clear_new_path()

                                    success(
                                        "已保存旧路径\n等待下次启动游戏..."
                                    )

                                self.injected = False

                                self.current_new_file = None

                                self.window_lost_count = 0



                        self.stop_event.wait(2)



        except Exception as e:

            log_error(
                str(e)
            )


            self.log(
                f"监听线程异常：{e}"
            )


        finally:

            self.log(
                "后台监听进程已退出"
            )


            self.finished_signal.emit()




    def inject(self):


                """
                执行注入
                """


                try:


                    result = self.patcher.start_patch()

                    if result["success"]:

                        self.injected = True

                        self.window_lost_count = 0

                        # ==================================
                        # 保存当前新文件路径
                        #
                        # 注意：
                        # 这里不是保存旧路径
                        # 只是记录本次正在使用的新路径
                        #
                        # Minecraft关闭后才会升级为旧路径
                        # ==================================

                        from file_state import save_new_path

                        save_new_path(
                            self.current_new_file
                        )

                        self.log(
                            result["message"]
                        )



                    else:



                     # 文件占用情况

                        if result.get(
                        "occupied",
                        False
                        ):


                            self.injected = True



                            warning(
                            "检测到文件被占用，无需重复注入"
                            )



                            self.log(
                            "文件被占用，认为已经注入"
                            )

                        else:

                            self.injected = True

                            error(
                            "注入失败，请查看错误报告"
                            )

                            self.log(
                            result["message"]
                            )

                            self.log(
                            "本次Minecraft启动注入失败，停止重复尝试"
                            )





                except Exception as e:



                    log_error(
                str(e)
            )



                    error(
                "注入发生异常"
                )