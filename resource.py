# ============================================================
# PlatformPatcher
#
# 资源管理模块
#
# 功能：
# 1. 获取内置资源路径
# 2. 兼容 PyInstaller 单文件 EXE
# 3. 统一管理 resources 文件夹
#
# 开发环境：
#     项目目录/resources
#
# EXE环境：
#     _MEIPASS/resources
#
# ============================================================


import os
import sys





def get_base_path():

    """
    获取程序基础路径

    PyInstaller -F 打包后：
        使用 sys._MEIPASS

    普通运行：
        使用当前文件目录

    """


    if hasattr(
        sys,
        "_MEIPASS"
    ):

        return sys._MEIPASS


    return os.path.dirname(
        os.path.abspath(__file__)
    )





def get_resource_path(filename):

    """
    获取 resources 内文件路径

    示例：

    get_resource_path(
        "xdpatch.mcp"
    )

    返回：

    resources/xdpatch.mcp
    """


    resource_dir = os.path.join(
        get_base_path(),
        "resources"
    )


    return os.path.join(
        resource_dir,
        filename
    )





def resource_exists(filename):

    """
    判断资源是否存在
    """


    path = get_resource_path(
        filename
    )


    return os.path.exists(
        path
    )





def get_mcp_files():

    """
    获取所有 mcp 文件

    返回：

    [
        "xxx.mcp",
        "xxx.mcp"
    ]

    """


    resource_dir = os.path.join(
        get_base_path(),
        "resources"
    )


    if not os.path.exists(
        resource_dir
    ):

        return []



    files = []


    for file in os.listdir(
        resource_dir
    ):

        if file.lower().endswith(
            ".mcp"
        ):

            files.append(
                file
            )


    return files