# ============================================================
# PlatformPatcher
#
# 全局 Patcher 管理
#
# 保证整个程序只有一个 Patcher 实例
#
# ============================================================


from patcher import Patcher


_patcher = None



def get_patcher():

    global _patcher


    if _patcher is None:

        _patcher = Patcher()


    return _patcher