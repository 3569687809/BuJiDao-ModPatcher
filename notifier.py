# ============================================================
# PlatformPatcher
#
# Windows 系统通知模块
#
# 功能：
# 1. 发送 Windows 系统通知
# 2. 依赖系统托盘(QSystemTrayIcon)
#
# ============================================================

from PySide6.QtWidgets import QSystemTrayIcon


# 当前托盘对象
_tray_icon: QSystemTrayIcon | None = None


def set_tray_icon(tray_icon: QSystemTrayIcon):
    """
    注册系统托盘对象

    tray.py 创建托盘后调用一次即可。
    """
    global _tray_icon
    _tray_icon = tray_icon


def notify(
    title: str,
    message: str,
    timeout: int = 5000
):
    """
    发送 Windows 系统通知

    参数：
        title    通知标题
        message  通知内容
        timeout  显示时间(毫秒)
    """

    if _tray_icon is None:
        return

    _tray_icon.showMessage(
        title,
        message,
        QSystemTrayIcon.MessageIcon.Information,
        timeout
    )


def success(
    message: str,
    timeout: int = 5000
):

    notify(
        "PlatformPatcher",
        message,
        timeout
    )


def warning(message: str):
    notify(
        "PlatformPatcher",
        message
    )


def error(message: str):
    notify(
        "PlatformPatcher",
        message
    )