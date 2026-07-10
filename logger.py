# ============================================================
# PlatformPatcher
#
# 日志模块
#
# 功能：
# 1. 每次启动生成新的 txt 日志
# 2. 保存运行过程
# 3. 提供统一日志接口
#
# ============================================================


import os
import logging
from datetime import datetime



# 日志目录

LOG_DIR = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "logs"
)



# 当前日志文件

LOG_FILE = None





def setup_logger():

    """
    初始化日志

    每次启动创建新的 txt 文件
    """


    global LOG_FILE



    # 创建日志目录

    if not os.path.exists(
        LOG_DIR
    ):

        os.makedirs(
            LOG_DIR
        )



    # 当前时间作为文件名

    filename = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S.txt"
    )



    LOG_FILE = os.path.join(
        LOG_DIR,
        filename
    )



    # 创建日志配置

    logging.basicConfig(

        level=logging.INFO,


        format=(
            "%(asctime)s "
            "[%(levelname)s] "
            "%(message)s"
        ),


        handlers=[

            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8"
            )

        ],

        force=True

    )



    info(
        "日志系统初始化完成"
    )



def get_logger():

    return logging.getLogger(
        "布吉岛ModPC补丁注入器"
    )





def info(message):

    get_logger().info(
        message
    )





def warning(message):

    get_logger().warning(
        message
    )





def error(message):

    get_logger().error(
        message
    )