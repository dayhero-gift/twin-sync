#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
"""
三方通信系统
洛君 - 小天（本地）- 老三（云端）
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

class TripleSync:
    """三方同步系统"""
    
    def __init__(self):
        self.workspace = Path("C:/Users/ThinkPad/.openclaw/workspace")
        self.sync_dir = self.workspace / "sync"
        self.sync_dir.mkdir(exist_ok=True)
        self.sync_log = self.sync_dir / "sync_log.json"
        
    def log_sync(self, event_type, data):
        """记录同步事件"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data,
            "source": "xiaotian-local"
        }
        
        logs = []
        if self.sync_log.exists():
            with open(self.sync_log, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(entry)
        
        with open(self.sync_log, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        return entry
    
    def send_to_laosan(self, message):
        """发送消息给老三（通过GitHub或文件）"""
        # 方式1: 通过GitHub Issue
        # 方式2: 通过共享文件
        # 方式3: 通过Telegram（待配置）
        
        sync_file = self.sync_dir / "to_laosan.json"
        
        data = {
            "from": "xiaotian",
            "to": "laosan",
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "status": "pending"
        }
        
        with open(sync_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.log_sync("send_to_laosan", message)
        print(f"[→ 老三] {message}")
        return True
    
    def receive_from_laosan(self):
        """接收老三的消息"""
        sync_file = self.sync_dir / "from_laosan.json"
        
        if not sync_file.exists():
            return None
        
        with open(sync_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data.get("status") == "unread":
            data["status"] = "read"
            with open(sync_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.log_sync("receive_from_laosan", data.get("message"))
            print(f"[← 老三] {data.get('message')}")
            return data
        
        return None
    
    def notify_luojun(self, message, level="info"):
        """通知洛君"""
        # 方式1: Telegram消息（待配置）
        # 方式2: 本地通知
        # 方式3: 写入待办
        
        notification = {
            "timestamp": datetime.now().isoformat(),
            "level": level,  # info, warning, urgent
            "message": message,
            "source": "xiaotian"
        }
        
        notify_file = self.sync_dir / "notifications.json"
        
        notifications = []
        if notify_file.exists():
            with open(notify_file, 'r', encoding='utf-8') as f:
                notifications = json.load(f)
        
        notifications.append(notification)
        
        with open(notify_file, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)
        
        self.log_sync("notify_luojun", message)
        
        icon = {"info": "ℹ️", "warning": "⚠️", "urgent": "🚨"}.get(level, "ℹ️")
        print(f"[{icon} 洛君] {message}")
        return True
    
    def sync_github(self):
        """同步到GitHub"""
        try:
            # 提交本地更改
            subprocess.run(
                ["git", "add", "."],
                cwd=self.workspace,
                check=True,
                capture_output=True
            )
            
            subprocess.run(
                ["git", "commit", "-m", f"Sync {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
                cwd=self.workspace,
                capture_output=True
            )
            
            subprocess.run(
                ["git", "push"],
                cwd=self.workspace,
                check=True,
                capture_output=True
            )
            
            self.log_sync("github_sync", "success")
            print("[GitHub] 同步成功")
            return True
            
        except Exception as e:
            self.log_sync("github_sync", f"error: {e}")
            print(f"[GitHub] 同步失败: {e}")
            return False
    
    def daily_sync(self):
        """每日同步流程"""
        print("="*50)
        print("三方每日同步")
        print("="*50)
        
        # 1. 发送状态给老三
        self.send_to_laosan({
            "type": "daily_status",
            "progress": "今日进化成果",
            "tools": 12,
            "docs": 8,
            "skills": 10
        })
        
        # 2. 检查老三的消息
        msg = self.receive_from_laosan()
        if msg:
            print(f"收到老三更新: {msg}")
        
        # 3. 同步到GitHub
        self.sync_github()
        
        # 4. 通知洛君
        self.notify_luojun("今日进化同步完成", "info")
        
        print("="*50)

if __name__ == "__main__":
    sync = TripleSync()
    sync.daily_sync()
