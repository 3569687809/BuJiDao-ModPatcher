# ============================================================
# PlatformPatcher
#
# 后台监听线程
#
# 功能：
# 1. 监听 Minecraft 窗口出现/消失
# 2. 检测 HudAddonScript.mcp 文件变化
# 3. 自动执行补丁注入
# 4. 支持两种检测模式：事件驱动（watchdog）和轮询回退
#
# ============================================================

import threading

from PySide6.QtCore import QThread, Signal

from config import monitor_mode
from file_detector import get_latest_file, get_folder_id
from file_state import save_old_path, clear_new_path
from injection_lock import injection_lock
from logger import info, success, log_error
from notifier import success as success_notify
from patch_manager import get_patcher
from window_detector import find_target_window

# 新增：文件监听器（基于 watchdog）
from file_watcher import PackcacheWatcher


class MinecraftMonitor(QThread):

    # 信号定义
    finished_signal = Signal()  

    def __init__(self):
        super().__init__()
        self.running = True
        self.stop_event = threading.Event()
        self.injected = False
        self.current_new_file = None
        self.old_id = None
        self.new_path = None
        self.window_lost_count = 0

        # 新增：文件监听器（基于 watchdog）
        self.file_watcher = None

    def log(self, message: str):
        info(f"[Monitor] {message}")

    def run(self):
        self.log("Minecraft监听模式已启动")

        try:
            while self.running:
                # ==================================================
                # 等待 Minecraft 出现
                # ==================================================
                if not self.injected:
                    self.log("正在等待Minecraft窗口...")

                    while self.running and not self.injected:
                        hwnd = find_target_window()

                        if hwnd:
                            new_file = self.check_new_file()
                            if new_file:
                                self.current_new_file = new_file
                                self.inject()
                            else:
                                self.stop_event.wait(1)
                        else:
                            self.window_lost_count = 0
                            self.stop_event.wait(2)

                # ==================================================
                # 等待 Minecraft 消失
                # ==================================================
                else:
                    self.log("等待Minecraft关闭...")

                    while self.running and self.injected:
                        hwnd = find_target_window()

                        if not hwnd:
                            self.window_lost_count += 1

                            if self.window_lost_count >= 3:
                                if self.current_new_file:
                                    save_old_path(self.current_new_file)
                                    clear_new_path()

                                    # 新增：更新 file_watcher 的 old_id
                                    if self.file_watcher:
                                        new_old_id = get_folder_id(self.current_new_file)
                                        self.file_watcher.update_old_folder_id(new_old_id)
                                        self.file_watcher.clear_queue()
                                    self.old_id = get_folder_id(
                                        self.current_new_file
                                    )

                                    self.log(
                                        f"旧文件ID更新为：{self.old_id}"
                                    )

                                    success(
                                        "已保存旧路径\n等待下次启动游戏..."
                                    )

                                    success_notify("已保存旧路径\n等待下次启动游戏...")

                                self.injected = False
                                self.current_new_file = None
                                self.window_lost_count = 0

                        self.stop_event.wait(2)

        except Exception as e:
            log_error(str(e))
            self.log(f"监听线程异常：{e}")

        finally:
            # 新增：停止文件监听器
            if self.file_watcher:
                self.file_watcher.stop()

            self.log("后台监听进程已退出")
            self.finished_signal.emit()

    def check_new_file(self):
        """
        检查是否有新文件
        
        优先使用 file_watcher 的事件驱动模式，
        如果 file_watcher 不可用，回退到轮询模式。
        """
        if self.file_watcher:
            event = self.file_watcher.get_new_file_event(timeout=0)
            if event and event["type"] == "new_file":
                self.new_path = event["path"]
                self.log(f"检测到新文件ID:{event['folder_id']}")
                success_notify("已检测到新的文件路径\n正在执行注入...")
                self.stop_event.wait(3)
                success_notify("已注入完成！\n请重启布吉岛", 15000)
                return self.new_path
            return None

        # 回退：轮询模式
        path = get_latest_file()
        if not path:
            return None

        current_id = get_folder_id(path)
        if current_id != self.old_id:
            self.new_path = path
            self.log(f"检测到新文件ID:{current_id}")
            success_notify("已检测到新的文件路径\n正在执行注入...")
            self.stop_event.wait(3)
            success_notify("已注入完成！\n请重启布吉岛", 15000)
            return path

        return None
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



    def inject(self):
        
        if not self.new_path:
            self.log("没有可注入的新文件")
            return

        with injection_lock:
            patcher = get_patcher()
            if not patcher:
                self.log("Patcher 未初始化")
                return

            result = patcher.inject(self.new_path)

            if result["success"]:
                self.injected = True
                self.log("注入成功")
            else:
                self.log(f"注入失败：{result.get('error', '未知错误')}")

    def prepare_old_path(self):
        
        path = get_latest_file()
        if path:
            self.old_id = get_folder_id(path)
            self.log(f"已记录旧文件ID:{self.old_id}")

            # 启动文件监听器
            self.file_watcher = PackcacheWatcher(self.old_id)
            if self.file_watcher.start():
                self.log("文件监听器已启动")
            else:
                self.log("文件监听器启动失败，将使用轮询模式")

            success_notify("已存入旧文件路径\n等待新的布吉岛文件生成...")

    def stop_monitor(self):
        self.log("正在停止后台监听进程...")
        self.running = False
        self.stop_event.set()

        if self.file_watcher:
            self.file_watcher.stop()

        if self.isRunning():
            self.wait(3000)
        else:
            self.log("后台监听进程已退出")
