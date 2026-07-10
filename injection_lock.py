# ============================================================
# PlatformPatcher
#
# 全局注入锁
#
# 功能：
# 1. 防止重复注入
# 2. UI和后台监听共用
#
# ============================================================


import threading



_lock = threading.Lock()


_running = False



def try_acquire():

    global _running


    with _lock:


        if _running:

            return False



        _running = True


        return True





def release():

    global _running


    with _lock:

        _running = False





def is_running():

    return _running