# ============================================================
# PlatformPatcher
#
# 程序生命周期管理
#
# 统一处理：
# 1. 停止后台线程
# 2. 删除托盘
# 3. 关闭Qt
# 4. 确保Python进程退出
#
# ============================================================


import os
import sys


from PySide6.QtWidgets import QApplication



# 保存需要关闭的对象

_monitor = None

_worker = None

_tray = None



def register_monitor(monitor):

    global _monitor

    _monitor = monitor


    _monitor = monitor





def register_worker(worker):
    """
    注册注入线程
    """

    global _worker

    _worker = worker





def register_tray(tray):
    """
    注册托盘对象
    """

    global _tray

    _tray = tray

def shutdown():

    global _monitor
    global _worker
    global _tray


    print(
        "正在关闭 PlatformPatcher..."
    )


    # ==========================
    # 停止监听线程
    # ==========================

    if _monitor:

        try:

            _monitor.stop_monitor()

        except Exception:

            pass

        _monitor = None



    # ==========================
    # 停止注入线程
    # ==========================

    if _worker:

        try:

            _worker.stop()

        except Exception:

            pass

        _worker = None



    # ==========================
    # 删除托盘
    # ==========================

    if _tray:

        try:

            if hasattr(_tray, "tray"):
                _tray.tray.hide()

        except Exception:

            pass

        _tray = None


    # ==========================
    # 退出 Qt
    # ==========================


    app = QApplication.instance()


    if app:

        app.quit()