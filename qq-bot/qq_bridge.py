#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ机器人对接服务
接收go-cqhttp消息，转发给小天/老三处理
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# 配置
GO_CQHTTP_URL = "http://192.168.0.238:5700"  # go-cqhttp地址（洛君本地IP）
QQ_GROUP_ID = ""  # 群号（可选）
QQ_USER_ID = ""   # 指定用户QQ号（可选）

# 消息记录
LOG_FILE = Path("qq_messages.jsonl")

def log_message(data):
    """记录消息"""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        json.dump({
            "time": datetime.now().isoformat(),
            "data": data
        }, f, ensure_ascii=False)
        f.write('\n')

def send_qq_message(message, user_id=None, group_id=None):
    """
    发送QQ消息
    
    Args:
        message: 消息内容
        user_id: 私聊用户QQ号
        group_id: 群号
    """
    url = f"{GO_CQHTTP_URL}/send_msg"
    
    if group_id:
        data = {
            "message_type": "group",
            "group_id": group_id,
            "message": message
        }
    else:
        data = {
            "message_type": "private",
            "user_id": user_id,
            "message": message
        }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"发送消息失败: {e}")
        return None

def process_message(data):
    """
    处理接收到的消息
    这里对接小天/老三的处理逻辑
    """
    message_type = data.get('message_type')  # private/group
    user_id = data.get('user_id')
    group_id = data.get('group_id')
    message = data.get('raw_message', '')
    sender = data.get('sender', {})
    nickname = sender.get('nickname', '未知')
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {nickname}({user_id}): {message}")
    
    # 只处理@机器人或私聊
    if message_type == 'private' or '@小天' in message or '@老三' in message:
        # 去掉@标记
        clean_msg = message.replace('@小天', '').replace('@老三', '').strip()
        
        # 调用处理逻辑（这里对接小天/老三）
        reply = handle_command(clean_msg, nickname)
        
        if reply:
            if group_id:
                send_qq_message(reply, group_id=group_id)
            else:
                send_qq_message(reply, user_id=user_id)

def handle_command(message, sender_name):
    """
    处理指令
    这里可以调用小天/老三的功能
    """
    message = message.strip()
    
    # 帮助指令
    if message in ['帮助', 'help', '菜单']:
        return """🤖 可用指令：
• 分析 股票代码 - 分析股票
• 行情 - 查看今日行情
• 策略 - 运行策略回测
• 同步 - 同步到老三/小天
• 状态 - 查看系统状态
• 帮助 - 显示本菜单"""
    
    # 分析股票
    if message.startswith('分析'):
        stock = message.replace('分析', '').strip()
        return f"正在分析 {stock}...\n(这里调用分析功能)"
    
    # 今日行情
    if message in ['行情', '市场', '大盘']:
        return "今日A股行情...\n(这里调用行情功能)"
    
    # 状态
    if message in ['状态', 'status']:
        return """📊 系统状态：
• 小天（本地）: 在线 ✅
• 老三（云端）: 在线 ✅
• QQ连接: 正常 ✅
• 策略运行: 待机中"""
    
    # 默认回复
    return f"收到消息: {message}\n(处理中...)"

@app.route('/qq/callback', methods=['POST'])
def qq_callback():
    """
    go-cqhttp消息回调
    """
    data = request.json
    
    # 只处理消息类型
    if data.get('post_type') == 'message':
        log_message(data)
        process_message(data)
    
    return jsonify({"status": "ok"})

@app.route('/send', methods=['POST'])
def send_message():
    """
    主动发送消息接口
    供小天/老三调用
    """
    data = request.json
    message = data.get('message')
    user_id = data.get('user_id')
    group_id = data.get('group_id')
    
    result = send_qq_message(message, user_id, group_id)
    return jsonify(result or {"status": "error"})

@app.route('/status', methods=['GET'])
def status():
    """状态检查"""
    return jsonify({
        "status": "running",
        "time": datetime.now().isoformat(),
        "go-cqhttp": GO_CQHTTP_URL
    })

if __name__ == '__main__':
    print("="*50)
    print("QQ机器人对接服务")
    print("="*50)
    print(f"接收地址: http://127.0.0.1:8080/qq/callback")
    print(f"go-cqhttp地址: {GO_CQHTTP_URL}")
    print("="*50)
    
    app.run(host='0.0.0.0', port=8080, debug=False)
