# ============================================================
# PlatformPatcher
#
# 注入核心模块
#
# 功能：
# 1. 自动寻找网易MC packcache
# 2. 定位 HudAddonScript.mcp
# 3. 替换注入文件
# 4. 文件占用检测
# 5. MD5重复判断
# 6. 错误报告
# 7. 支持PyInstaller单EXE
#
# ============================================================


import os
import hashlib
import shutil


from pathlib import Path


from resource import (
    get_resource_path
)


from injection_lock import (
    try_acquire,
    release
)


from logger import (
    info
)


from error_report import (
    create_error_report
)


from file_detector import (
    get_target_file
)





# ============================================================
# 文件工具
# ============================================================


def is_file_locked(path):


    if not os.path.exists(path):

        return False


    try:

        with open(
            path,
            "a"
        ):

            pass


        return False


    except PermissionError:

        return True





def file_hash(path):


    if not os.path.exists(path):

        return None



    md5 = hashlib.md5()



    with open(
        path,
        "rb"
    ) as f:


        for chunk in iter(
            lambda:f.read(8192),
            b""
        ):

            md5.update(
                chunk
            )


    return md5.hexdigest()





def safe_copy(
        source,
        target
):


    temp = str(target) + ".tmp"



    shutil.copy2(
        source,
        temp
    )


    os.replace(
        temp,
        target
    )






# ============================================================
# Patcher
# ============================================================


class Patcher:



    def __init__(self):


        # ==================================================
        # PyInstaller资源路径
        # ==================================================


        self.source_files = [

            "Script_PlatformPatcher.mcp",

            "xdpatch.mcp"

        ]



        info(
            "Patcher初始化完成"
        )





    # ==================================================
    # 日志
    # ==================================================


    def log(
            self,
            message
    ):


        info(
            message
        )





    # ==================================================
    # 主入口
    # ==================================================


    def start_patch(
            self
    ):


        # 全局注入锁

        if not try_acquire():


            return {

                "success":False,

                "message":
                    "注入任务正在执行，请稍候"

            }




        try:


            return self.do_patch()



        except Exception as e:



            create_error_report(

                e,

                "patcher.py 注入异常"

            )



            return {


                "success":False,


                "message":
                    str(e)

            }



        finally:


            release()





    # ==================================================
    # 注入流程
    # ==================================================


    def do_patch(
            self
    ):


        self.log(
            "开始寻找Minecraft文件..."
        )



        hud_file = get_target_file()



        if not hud_file:



            return {


                "success":False,


                "message":
                    "未找到 HudAddonScript.mcp"

            }




        target_dir = Path(
            hud_file
        ).parent



        self.log(
            f"目标目录:{target_dir}"
        )



        result_files = []





        for filename in self.source_files:



            source = get_resource_path(
                filename
            )



            target = target_dir / filename




            if not os.path.exists(
                source
            ):


                return {


                    "success":False,


                    "message":
                    f"资源不存在:{filename}"

                }





            # ============================
            # 已经相同
            # ============================


            if target.exists():


                if file_hash(source) == file_hash(target):


                    self.log(
                        f"{filename} 已存在，无需替换"
                    )


                    result_files.append(
                        str(target)
                    )


                    continue





            # ============================
            # 文件占用
            # ============================


            if is_file_locked(
                target
            ):


                return {


                    "success":False,


                    "occupied":True,


                    "message":
                    f"{filename} 正在被占用，无需重复注入"

                }






            # ============================
            # 复制
            # ============================



            safe_copy(

                source,

                target

            )



            self.log(
                f"已替换:{filename}"
            )



            result_files.append(

                str(target)

            )





        return {


            "success":True,


            "message":
                "注入完成",



            "files":
                result_files

        }