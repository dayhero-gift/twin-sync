#!/bin/bash
# 一键启动QQ机器人服务

echo "启动QQ机器人服务..."

# 检查go-cqhttp
if [ ! -f "go-cqhttp" ]; then
    echo "错误: 请先运行 deploy.sh 下载go-cqhttp"
    exit 1
fi

# 启动go-cqhttp
echo "启动 go-cqhttp..."
./go-cqhttp &

# 等待启动
sleep 3

# 启动Python对接服务
echo "启动Python对接服务..."
python3 qq_bridge.py
