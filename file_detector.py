import os


SEARCH_FOLDER = os.path.join(
    os.getenv("APPDATA"),
    "MinecraftPC_Netease_PB",
    "packcache"
)


TARGET_FILE = "HudAddonScript.mcp"



def get_latest_file():

    """
    获取最新 HudAddonScript.mcp 完整路径
    """

    if not os.path.exists(
        SEARCH_FOLDER
    ):
        return None


    result = []


    for root, dirs, files in os.walk(
        SEARCH_FOLDER
    ):

        if TARGET_FILE in files:

            result.append(
                os.path.join(
                    root,
                    TARGET_FILE
                )
            )


    if not result:

        return None



    result.sort(
        key=lambda x:
        os.path.getmtime(x),
        reverse=True
    )


    return result[0]




def get_folder_id(path):

    """
    获取随机目录ID

    例如：

    C:\\...\\packcache\\HUXb0g-AyA8=\\HudAddonScript.mcp

    返回：

    HUXb0g-AyA8=
    """


    if not path:

        return None



    directory = os.path.dirname(
        path
    )


    return os.path.basename(
        directory
    )

def get_target_file():

    """
    普通注入模式使用

    返回当前最新 HudAddonScript.mcp

    不参与监听状态判断
    """

    return get_latest_file()