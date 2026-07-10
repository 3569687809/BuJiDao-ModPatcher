# ============================================================
# PlatformPatcher
#
# 用户界面模块
#
# 功能：
# 1. 创建主窗口
# 2. 显示日志
# 3. 检测目标窗口
# 4. 调用补丁模块
#
# ============================================================

from PySide6.QtCore import Slot

import os

from tray import TrayManager

from monitor import MinecraftMonitor

from worker import PatchWorker

import config

from resource import get_resource_path

from worker import PatchWorker

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QMessageBox
)


from PySide6.QtGui import QIcon



from window_detector import (
    find_target_window
)


from patcher import (
    Patcher
)


from logger import (
    info,
    error
)



class MainWindow(QMainWindow):


    def __init__(self):

        super().__init__()

        self.worker = None

        self.tray_manager = None

        self.monitor = None

        self.patcher = Patcher()


        self.init_window()

        self.init_ui()



    def init_window(self):


        # ==================================================
        # 窗口标题修改位置
        #
        # 后续如果程序名称需要修改，
        # 只需要修改下面这一行。
        #
        # ==================================================

        self.setWindowTitle(
            "布吉岛ModPC补丁注入器"
        )

        # ==================================================
        # 加载程序图标
        #
        # 支持：
        #
        # 开发环境：
        #     resources/app.ico
        #
        # EXE环境：
        #     PyInstaller 内置资源
        #
        # ==================================================

        icon_path = get_resource_path(
            "app.ico"
        )

        if os.path.exists(icon_path):
            self.setWindowIcon(
                QIcon(icon_path)
            )


        self.resize(
            480,
            300
        )



    def init_ui(self):


        widget = QWidget()

        self.setCentralWidget(
            widget
        )


        layout = QVBoxLayout()


        widget.setLayout(
            layout
        )



        self.status_label = QLabel(
            "状态：等待检测"
        )


        layout.addWidget(
            self.status_label
        )

        self.log_box = QTextEdit()

        self.log_box.setReadOnly(
            True
        )

        # 限制日志窗口高度，
        # 给下面提示区域留空间

        self.log_box.setFixedHeight(
            190
        )

        self.log_box.append(
            "等待开始……"
        )

        layout.addWidget(
            self.log_box
        )

        # ===============================
        # 用户提示区域
        # ===============================

        self.tip_label = QLabel(
            "提示：\n"
            "托盘模式启动时可能会卡上1~5秒，\n"
            "进入布吉岛等待注入完成后，重新进入布吉岛即可。"
        )

        # 允许换行

        self.tip_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.tip_label
        )



        self.start_button = QPushButton(
            "开始注入"
        )


        # ==================================
        # 托盘监听按钮
        # ==================================

        self.monitor_button = QPushButton(
            "打开托盘监听进程"
        )

        self.monitor_button.clicked.connect(
            self.start_monitor_mode
        )


        self.start_button.clicked.connect(
            self.start_patch
        )


        layout.addWidget(
            self.start_button
        )


        layout.addWidget(
            self.monitor_button
        )



    def log(self, message):


        self.log_box.append(
            message
        )



        info(
            message
        )

    def start_patch(self):

        self.start_button.setEnabled(
                False
            )

        self.log(
                "正在开始注入流程..."
            )

        self.log(
                "提示：由于正在搜索游戏文件并替换资源，过程中可能会卡顿 1~5 秒，请耐心等待。"
            )

        self.log(
                "正在检测目标窗口..."
            )



        # ============================
        # 检测窗口
        # ============================


        hwnd = find_target_window()



        if hwnd is None:


            self.log(
                "未找到Minecraft窗口"
            )


            self.status_label.setText(
                "状态：未找到窗口"
            )


            QMessageBox.warning(
                self,
                "提示",
                "未检测到目标窗口"
            )


            self.start_button.setEnabled(
                True
            )


            return



        self.log(
            f"检测成功，窗口句柄：{hwnd}"
        )



        self.status_label.setText(
            "状态：准备文件"
        )



        # ============================
        # 调用补丁模块
        # ============================

        # 创建后台线程

        self.worker = PatchWorker()

        # 接收实时日志

        self.worker.log_signal.connect(
            self.log
        )

        # 任务完成回调

        self.worker.finished_signal.connect(
            self.patch_finished
        )

        # 启动线程

        self.worker.start()

    def show_monitor_popup(
            self,
            title,
            message
    ):

        QMessageBox.information(
            None,
            title,
            message
        )

    def start_monitor_mode(self):

        self.log(
            "正在开启托盘监听模式..."
        )

        # ==============================
        # 创建监听线程
        # ==============================

        if self.monitor is None:
            self.monitor = MinecraftMonitor(self)

            self.monitor.popup_signal.connect(
                self.show_monitor_popup
            )

            from app_manager import register_monitor

            register_monitor(
                self.monitor
            )

        # ==============================
        # 创建托盘
        # ==============================

        if self.tray_manager is None:
            self.tray_manager = TrayManager(
                self
            )

        self.tray_manager.enable_tray()

        # ==============================
        # 绑定监听对象
        # ==============================

        self.tray_manager.monitor = self.monitor

        # ==============================
        # 启动监听
        # ==============================

        if not self.monitor.isRunning():
            self.monitor.start_monitor()

        self.log(
            "后台监听线程已启动"
        )

        # 不要直接 hide
        # 改成最小化到托盘

        self.showMinimized()

        self.hide()

    def closeEvent(self, event):

        if self.monitor and self.monitor.isRunning():
            self.hide()

            event.ignore()

            return

        from app_manager import shutdown

        shutdown()

        event.accept()


    def patch_finished(self, result):

            if result["success"]:

                self.log(
                    result["message"]
                )

                for file in result["files"]:
                    self.log(
                        f"已准备：{file}"
                    )

                self.status_label.setText(
                    "状态：准备完成"
                )

                QMessageBox.information(
                    self,
                    "成功",
                    "已注入成功，请重新进入布吉岛"
                )

                self.close()


            else:

                self.log(
                    result["message"]
                )

                self.status_label.setText(
                    "状态：失败"
                )

                error(
                    result["message"]
                )

                QMessageBox.critical(
                    self,
                    "注入失败",
                    result["message"]
                )

            self.start_button.setEnabled(
                True
            )