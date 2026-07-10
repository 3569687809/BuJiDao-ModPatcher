# ============================================================
# PlatformPatcher
#
# 程序入口
#
# 功能：
# 1. 初始化程序
# 2. 初始化日志
# 3. 创建UI
# 4. 全局异常捕获
#
# ============================================================


import sys


from PySide6.QtWidgets import (
    QApplication
)



from ui import (
    MainWindow
)



from logger import (
    setup_logger,
    error
)



from error_report import (
    create_error_report
)







def exception_hook(
    exc_type,
    exc_value,
    exc_traceback
):

    import traceback


    traceback.print_exception(
        exc_type,
        exc_value,
        exc_traceback
    )


    message = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback
        )
    )


    error(message)


    create_error_report(
        exc_value,
        "main.py 未处理异常"
    )






def main():



    # =====================================
    # 初始化异常捕获
    # =====================================


    sys.excepthook = exception_hook




    # =====================================
    # 初始化Qt
    # =====================================


    app = QApplication(
        sys.argv
    )

    # 托盘模式必须关闭自动退出
    # 否则隐藏主窗口后 Qt 会直接结束

    app.setQuitOnLastWindowClosed(
        False
    )




    # =====================================
    # 初始化日志
    # =====================================


    setup_logger()




    # =====================================
    # 创建窗口
    # =====================================

    window = MainWindow()

    window.show()

    app.window = window




    # =====================================
    # Qt事件循环
    # =====================================


    sys.exit(
        app.exec()
    )







if __name__ == "__main__":


    main()