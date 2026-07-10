# ============================================================
# PlatformPatcher
#
# 错误报告模块
#
# 功能：
# 1. 自动生成错误报告
# 2. 保存到用户文档
# 3. 记录异常堆栈
#
# ============================================================


import os

import traceback

from datetime import datetime



from pathlib import Path


MAX_REPORT = 10



def get_report_directory():

    """
    获取错误报告目录

    用户文档目录:
    Documents/布吉岛ModPC补丁注入器_Error
    """


    documents = Path.home() / "Documents"


    report_dir = (
        documents /
        "布吉岛ModPC补丁注入器_Error"
    )


    if not report_dir.exists():

        report_dir.mkdir(
            parents=True
        )

    files = sorted(
        report_dir.glob(
            "*.txt"
        ),
        key=lambda x: x.stat().st_mtime
    )

    while len(files) >= MAX_REPORT:
        files[0].unlink()

        files.pop(0)

    return report_dir





def create_error_report(
    error,
    extra_info=None
):

    """
    创建错误报告

    参数：

    error:
        异常对象或者错误文本


    extra_info:
        额外信息

    返回：
        报告路径
    """



    try:


        report_dir = get_report_directory()



        filename = datetime.now().strftime(
            "error_%Y-%m-%d_%H-%M-%S.txt"
        )



        report_file = (
            report_dir /
            filename
        )



        # 获取异常堆栈

        if isinstance(
            error,
            Exception
        ):

            traceback_info = traceback.format_exc()


        else:

            traceback_info = str(error)




        content = f"""
==============================
PlatformPatcher 错误报告
==============================


时间：

{datetime.now()}


错误信息：

{error}



异常堆栈：

{traceback_info}



其他信息：

{extra_info}



==============================
报告结束
==============================
"""



        with open(
            report_file,
            "w",
            encoding="utf-8"
        ) as f:


            f.write(
                content
            )



        return str(
            report_file
        )



    except Exception:


        return None