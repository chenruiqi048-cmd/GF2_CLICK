@echo off
title GF2 自动点击助手
setlocal enabledelayedexpansion

:: 设置编码为 UTF-8 以支持中文显示
chcp 65001 >nul

echo ==========================================
echo       GF2 自动点击助手 - 一键启动
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
if not exist "gf2_gui.py" (
    echo [错误] 未找到主程序 gf2_gui.py。
    pause
    exit /b
)

echo [信息] 正在启动 GUI...
echo.

:: 运行 GUI 版本
".venv\Scripts\python.exe" gf2_gui.py

echo.
echo [信息] 程序已退出。
pause
