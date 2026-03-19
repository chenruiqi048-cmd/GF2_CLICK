@echo off
title GF2_CLICK Bot Launcher
setlocal enabledelayedexpansion

:: 设置编码为 UTF-8 以支持中文显示
chcp 65001 >nul

echo ==========================================
echo       GF2_CLICK 自动点击工具 启动器
echo ==========================================
echo.

:: 检查虚拟环境是否存在
if not exist ".venv\Scripts\python.exe" (
    echo [错误] 未找到虚拟环境 .venv。
    echo 请确保项目根目录下存在 .venv 文件夹。
    pause
    exit /b
)

:: 检查主程序是否存在
if not exist "gf2_bot.py" (
    echo [错误] 未找到主程序 gf2_bot.py。
    pause
    exit /b
)

echo [信息] 正在激活虚拟环境并启动程序...
echo [提示] 按 Ctrl+C 可以停止运行。
echo.

:: 运行程序
".venv\Scripts\python.exe" gf2_bot.py

echo.
echo [信息] 程序已退出。
pause
