# ============================================================
# PlatformPatcher
#
# 系统托盘模块
#
# 功能：
# 1. 创建右下角托盘图标
# 2. 托盘菜单
# 3. 控制监听模式
# 4. 管理窗口显示隐藏
#
# ============================================================

from logger import info

import config

from PySide6.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
)

from PySide6.QtGui import (
    QAction,
    QIcon
)

from PySide6.QtCore import QObject


from resource import get_resource_path


from notifier import set_tray_icon




class TrayManager(QObject):

    def tray_activated(self, reason):

        """
        托盘图标事件

        双击:
        显示窗口并关闭监听模式
        """

        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.disable_monitor_mode()

    def disable_monitor_mode(self):

        self.log(
            "正在关闭监听模式..."
        )

        config.disable_monitor()

        if self.monitor:
            self.monitor.stop_monitor()

            self.monitor = None

        from app_manager import register_monitor

        register_monitor(None)

        if self.monitor:
            self.monitor.stop_monitor()

            self.monitor.deleteLater()

            self.monitor = None

        self.tray.hide()

        self.monitor_action.setChecked(False)

        self.monitor_action.setText(
            "开启监听模式"
        )

        self.show_window()

        self.log(
            "已关闭监听模式"
        )

    def log(self, message):

        if self.window:
            self.window.log(
                message
            )

    def toggle_monitor(self, checked):

        if checked:

            config.enable_monitor()

            self.window.start_monitor_mode()

        else:

            self.disable_monitor_mode()

    def exit_app(self):

        info(
            "用户从托盘退出程序"
        )

        from app_manager import shutdown

        shutdown()

    def enable_tray(self):

        self.tray.show()

        self.tray.setVisible(True)

        self.monitor_action.setChecked(True)

        self.monitor_action.setText(
            "关闭监听模式"
        )


    def __init__(
        self,
        window
    ):

        super().__init__()


        self.window = window


        self.monitor = None

        self.exit_action = None

        self.tray = QSystemTrayIcon()


        # 加载图标

        icon_path = get_resource_path(
            "app.ico"
        )


        self.tray.setIcon(
            QIcon(icon_path)
        )


        self.tray.setToolTip(
            "布吉岛ModPC补丁注入-监听中"
        )


        self.create_menu()



        # 注册通知对象

        set_tray_icon(
            self.tray
        )

        from app_manager import register_tray

        register_tray(
            self
        )

        self.tray.activated.connect(
            self.tray_activated
        )

        # 创建后立即显示托盘

        self.tray.show()




    def create_menu(self):


        menu = QMenu()



        # 显示窗口


        show_action = QAction(
            "显示主窗口"
        )


        show_action.triggered.connect(
            self.show_window
        )



        menu.addAction(
            show_action
        )



        # 监听模式


        self.monitor_action = QAction(
            "开启监听模式"
        )


        self.monitor_action.setCheckable(
            True
        )


        self.monitor_action.triggered.connect(
            self.toggle_monitor
        )


        menu.addAction(
            self.monitor_action
        )

        menu.addSeparator()



        # 退出


        self.exit_action = QAction(
            "退出程序"
        )

        self.exit_action.triggered.connect(
            self.exit_app
        )

        menu.addAction(
            self.exit_action
        )



        self.tray.setContextMenu(
            menu
        )





    def start(self):

        self.enable_tray()





    def hide_window(self):


        self.window.hide()

    def show_window(self):

        self.window.show()

        self.window.activateWindow()