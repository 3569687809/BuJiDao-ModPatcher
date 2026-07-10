# ============================================================
# PlatformPatcher
#
# 窗口检测模块
#
# 功能：
# 1. 根据窗口标题检测目标程序
# 2. 返回窗口句柄
# 3. 提供检测状态
#
# UI调用：
#
# ui.py
#     ↓
# window_detector.py
#
# ============================================================


import win32gui



# ============================================================
# 这里修改需要检测的窗口标题
#
# 后续如果你的游戏窗口标题变了，
# 只需要修改下面这一行即可。
#
# ============================================================

TARGET_WINDOW_TITLE = "Minecraft"





def enum_windows():

    """
    获取当前所有窗口

    返回：
        list
        [
            {
                "hwnd": 窗口句柄,
                "title": 窗口标题
            }
        ]
    """

    windows = []



    def callback(hwnd, _):

        # 判断窗口是否可见

        if win32gui.IsWindowVisible(hwnd):

            title = win32gui.GetWindowText(hwnd)


            if title:

                windows.append(
                    {
                        "hwnd": hwnd,
                        "title": title
                    }
                )



    win32gui.EnumWindows(
        callback,
        None
    )


    return windows





def find_target_window():

    """
    查找目标窗口

    返回：

    找到：
        hwnd

    未找到：
        None

    """


    windows = enum_windows()



    for window in windows:

        title = window["title"]

        # 模糊匹配

        if TARGET_WINDOW_TITLE.lower() in title.lower():
            return window["hwnd"]



    return None





def is_window_exists():

    """
    判断目标窗口是否存在

    返回：

    True:
        找到

    False:
        未找到

    """

    hwnd = find_target_window()


    return hwnd is not None





def get_window_title(hwnd):

    """
    根据句柄获取窗口标题
    """

    if hwnd:

        return win32gui.GetWindowText(hwnd)


    return None
