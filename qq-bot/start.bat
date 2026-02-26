@echo off
echo ==========================================
echo   启动QQ机器人服务
echo ==========================================

:: 检查文件
if not exist "go-cqhttp.exe" (
    echo 错误: 请先运行 deploy.bat 下载go-cqhttp
    pause
    exit /b
)

:: 启动go-cqhttp
echo 启动 go-cqhttp...
start go-cqhttp.exe

:: 等待
timeout /t 3 /nobreak > nul

:: 启动Python对接服务
echo 启动Python对接服务...
python qq_bridge.py

pause
