# ============================================================
# PlatformPatcher
#
# 文件状态缓存
#
# old:
# 上一次完整游戏启动路径
#
# pending:
# 当前正在使用的新路径
#
# ============================================================


import os
import json
import time



CACHE_DIR = os.path.join(
    os.getenv("APPDATA"),
    "PlatformPatcher"
)


CACHE_FILE = os.path.join(
    CACHE_DIR,
    "file_state.json"
)




def load_state():

    if not os.path.exists(
        CACHE_FILE
    ):
        return {}


    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    except Exception:

        return {}





def save_state(data):

    os.makedirs(
        CACHE_DIR,
        exist_ok=True
    )


    data["update_time"] = time.time()


    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )





# ============================================================
# 旧路径
# ============================================================


def load_old_path():

    data = load_state()

    return data.get(
        "old_hud_path"
    )





def save_old_path(path):

    data = load_state()


    data["old_hud_path"] = path


    save_state(
        data
    )





# ============================================================
# 当前新路径
# ============================================================


def load_new_path():

    data = load_state()

    return data.get(
        "new_hud_path"
    )





def save_new_path(path):

    data = load_state()


    data["new_hud_path"] = path


    save_state(
        data
    )





def clear_new_path():

    data = load_state()


    if "new_hud_path" in data:

        del data["new_hud_path"]


    save_state(
        data
    )





# ============================================================
# 路径标准化
# ============================================================


def normalize(path):

    if path:

        return os.path.abspath(
            path
        )


    return None