# ============================================================
# PlatformPatcher
#
# 注入任务线程模块
#
# 功能：
# 1. 后台执行注入
# 2. 不阻塞UI
# 3. 普通模式/监听模式共用
#
# ============================================================


from PySide6.QtCore import (
    QThread,
    Signal
)



from patch_manager import get_patcher



from logger import (
    info,
    error
)





class PatchWorker(QThread):


    # 日志输出

    log_signal = Signal(str)



    # 完成返回

    finished_signal = Signal(dict)




    def __init__(self):


        super().__init__()


        self.patcher = get_patcher()



        self.running = True






    def log(self,message):


        info(
            message
        )


        self.log_signal.emit(
            message
        )







    def run(self):

        """
        在线程中执行
        """


        try:



            self.log(
                "开始执行注入任务..."
            )



            self.log(
                "正在搜索Minecraft资源..."
            )



            result = (

                self.patcher.start_patch()

            )



            if result["success"]:



                self.log(
                    "注入完成"
                )



            else:



                self.log(
                    result["message"]
                )



            self.finished_signal.emit(

                result

            )





        except Exception as e:



            error(
                str(e)
            )



            self.finished_signal.emit(

                {

                    "success":False,

                    "occupied":False,

                    "message":
                    str(e)

                }

            )








    def stop(self):


        """
        停止线程
        """


        self.running = False