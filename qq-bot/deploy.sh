#!/bin/bash
# QQ机器人快速部署脚本 - 在洛君电脑上运行
# 1. 下载go-cqhttp
# 2. 自动配置
# 3. 启动服务

echo "=========================================="
echo "  QQ机器人快速部署"
echo "=========================================="

# 创建目录
mkdir -p ~/qq-bot
cd ~/qq-bot

# 下载go-cqhttp (根据系统自动选择)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    wget https://github.com/Mrs4s/go-cqhttp/releases/download/v1.2.0/go-cqhttp_linux_amd64.tar.gz
    tar -xzf go-cqhttp_linux_amd64.tar.gz
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    wget https://github.com/Mrs4s/go-cqhttp/releases/download/v1.2.0/go-cqhttp_windows_amd64.zip
    unzip go-cqhttp_windows_amd64.zip
fi

# 首次运行生成配置文件
echo "首次运行，生成配置文件..."
./go-cqhttp

echo "=========================================="
echo "  配置步骤:"
echo "=========================================="
echo "1. 选择通信方式: 输入 0 (HTTP)"
echo "2. 编辑 config.yml 配置QQ号和密码"
echo "3. 重新运行 ./go-cqhttp"
echo "4. 扫码或短信验证登录"
echo ""
echo "配置文件位置: $(pwd)/config.yml"
echo ""
echo "HTTP接口地址: http://127.0.0.1:5700"
echo ""
