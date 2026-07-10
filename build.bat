@echo off
chcp 65001 >nul

title PlatformPatcher Build


echo.
echo ==============================
echo 布吉岛ModPC补丁注入器 打包工具
echo ==============================
echo.



REM ==============================
REM 清理旧文件
REM ==============================


echo 正在清理旧构建文件...


if exist build (
    rmdir /s /q build
)


if exist dist (
    rmdir /s /q dist
)


if exist PlatformPatcher.spec (
    del /f /q PlatformPatcher.spec
)



echo 清理完成


echo.



REM ==============================
REM 检查环境
REM ==============================


echo 检查 PyInstaller...


pyinstaller --version


if errorlevel 1 (

    echo.
    echo 未找到 PyInstaller
    echo 请执行:
    echo pip install pyinstaller

    pause
    exit /b

)



echo.



REM ==============================
REM 开始打包
REM ==============================


echo 开始生成 EXE...


pyinstaller ^
-F ^
-w ^
--name 布吉岛ModPC补丁注入器 ^
--icon resources\app.ico ^
--add-data "resources;resources" ^
--hidden-import PySide6.QtCore ^
--hidden-import PySide6.QtGui ^
--hidden-import PySide6.QtWidgets ^
--hidden-import tray ^
--hidden-import monitor ^
--hidden-import notifier ^
--hidden-import file_detector ^
--hidden-import patch_manager ^
--hidden-import injection_lock ^
--hidden-import error_report ^
--hidden-import PySide6.QtCore ^
--hidden-import PySide6.QtGui ^
--hidden-import PySide6.QtWidgets ^
--collect-all PySide6 ^
main.py



if errorlevel 1 (

    echo.
    echo ==============================
    echo 打包失败
    echo ==============================

    pause
    exit /b

)



echo.



REM ==============================
REM 完成
REM ==============================


echo ==============================
echo 打包成功
echo ==============================

echo.

echo 输出位置:

echo dist\PlatformPatcher.exe


echo.


pause