@echo off
chcp 65001
echo ==========================================
echo   QQ机器人快速部署 (Windows)
echo ==========================================

:: 创建目录
mkdir C:\qq-bot 2>nul
cd C:\qq-bot

echo 正在下载 go-cqhttp...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/Mrs4s/go-cqhttp/releases/download/v1.2.0/go-cqhttp_windows_amd64.exe' -OutFile 'go-cqhttp.exe'"

echo 首次运行生成配置文件...
go-cqhttp.exe

echo ==========================================
echo   配置步骤:
echo ==========================================
echo 1. 选择通信方式: 输入 0 (HTTP)
echo 2. 编辑 config.yml 配置QQ号和密码
echo 3. 重新运行 go-cqhttp.exe
echo 4. 扫码或短信验证登录
echo.
echo 配置文件位置: C:\qq-bot\config.yml
echo.
echo HTTP接口地址: http://127.0.0.1:5700
echo.
pause
