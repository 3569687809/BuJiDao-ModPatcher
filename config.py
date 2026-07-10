# ============================================================
# PlatformPatcher
#
# 全局状态管理模块
#
# 功能：
# 1. 管理监听模式
# 2. 管理注入状态
# 3. 管理程序运行状态
#
# ============================================================



# ============================================================
# 程序状态
# ============================================================


# 程序是否正在运行

app_running = True



# ============================================================
# 托盘监听状态
# ============================================================


# 是否开启后台监听

monitor_enabled = False



# 监听线程是否运行

monitor_running = False





# ============================================================
# Minecraft 状态
# ============================================================


# 是否已经注入过

already_injected = False



# 当前是否正在等待 Minecraft 关闭

watching_close = False






# ============================================================
# 状态修改函数
# ============================================================



def enable_monitor():

    """
    开启监听模式
    """

    global monitor_enabled

    monitor_enabled = True





def disable_monitor():

    """
    关闭监听模式
    """

    global monitor_enabled

    monitor_enabled = False






def is_monitor_enabled():

    """
    获取监听状态
    """

    return monitor_enabled





def set_injected(value: bool):

    """
    设置注入状态
    """

    global already_injected

    already_injected = value





def is_injected():

    """
    获取注入状态
    """

    return already_injected






def reset_game_state():

    """
    Minecraft关闭后重置状态
    """

    global already_injected
    global watching_close


    already_injected = False

    watching_close = False





def start_monitor_thread():

    """
    标记监听线程启动
    """

    global monitor_running

    monitor_running = True





def stop_monitor_thread():

    """
    标记监听线程停止
    """

    global monitor_running

    monitor_running = False