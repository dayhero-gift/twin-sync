"""
TwinSync GitHub - GitHub-based messaging for AI Twins
基于GitHub Issues的双生AI通信系统
替代Telegram的方案（无需手机号）
"""
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class GitHubMessenger:
    """
    基于GitHub Issues的消息系统
    利用GitHub Issues作为消息队列实现双向通信
    """
    
    def __init__(self, repo_owner: str = None, repo_name: str = None, 
                 github_token: str = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}" if repo_owner and repo_name else None
        
        # 身份标识
        self.my_id = "xiaotian_local"
        self.brother_id = "xiaotian_cloud"
        
        # 消息缓存
        self.message_cache_dir = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/messages")
        self.message_cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Issues标签
        self.labels = {
            "message": "twin-message",
            "sync": "twin-sync", 
            "alert": "twin-alert",
            "data": "twin-data",
            "heartbeat": "twin-heartbeat"
        }
    
    def send_message(self, title: str, body: str, msg_type: str = "general") -> Dict:
        """
        发送消息（创建GitHub Issue）
        """
        if not self.api_base or not self.github_token:
            # 本地模式：保存到文件
            return self._save_local_message(title, body, msg_type)
        
        import aiohttp
        
        # 格式化消息
        formatted_body = self._format_message(body, msg_type)
        
        # 创建Issue
        url = f"{self.api_base}/issues"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "title": f"[{self.my_id}] {title}",
            "body": formatted_body,
            "labels": [self.labels.get(msg_type, "twin-message")]
        }
        
        # 这里用同步请求简化
        import requests
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                issue = response.json()
                return {
                    "success": True,
                    "issue_number": issue["number"],
                    "issue_url": issue["html_url"],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"error": response.text, "status": response.status_code}
        except Exception as e:
            return {"error": str(e)}
    
    def _save_local_message(self, title: str, body: str, msg_type: str) -> Dict:
        """本地模式：保存消息到文件"""
        message = {
            "id": f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "from": self.my_id,
            "to": self.brother_id,
            "type": msg_type,
            "title": title,
            "body": body,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"  # 待同步到GitHub
        }
        
        # 保存到待发送队列
        queue_file = self.message_cache_dir / "outbox.jsonl"
        with open(queue_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
        
        return {
            "success": True,
            "mode": "local",
            "message_id": message["id"],
            "note": "Message queued for GitHub sync"
        }
    
    def _format_message(self, body: str, msg_type: str) -> str:
        """格式化消息"""
        header = f"**From:** {self.my_id}\n"
        header += f"**Type:** {msg_type}\n"
        header += f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        header += "---\n\n"
        
        footer = f"\n\n---\n\n"
        footer += f"*Message ID: msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}*\n"
        footer += f"*Reply to this issue to respond*"
        
        return header + body + footer
    
    def get_messages(self, since: str = None, msg_type: str = None) -> List[Dict]:
        """
        获取消息（从GitHub Issues）
        """
        if not self.api_base or not self.github_token:
            return self._get_local_messages()
        
        import requests
        
        url = f"{self.api_base}/issues"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        params = {
            "state": "all",
            "labels": self.labels.get(msg_type, "twin-message"),
            "sort": "created",
            "direction": "desc"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                issues = response.json()
                messages = []
                for issue in issues:
                    msg = {
                        "id": issue["number"],
                        "title": issue["title"],
                        "body": issue["body"],
                        "author": issue["user"]["login"],
                        "state": issue["state"],
                        "created_at": issue["created_at"],
                        "url": issue["html_url"]
                    }
                    messages.append(msg)
                return messages
            else:
                return [{"error": response.text}]
        except Exception as e:
            return [{"error": str(e)}]
    
    def _get_local_messages(self) -> List[Dict]:
        """本地模式：从文件读取消息"""
        inbox_file = self.message_cache_dir / "inbox.json"
        if inbox_file.exists():
            with open(inbox_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    # ===== 快捷消息方法 =====
    
    def report_task_complete(self, task_name: str, result: str, details: str = None):
        """报告任务完成"""
        title = f"Task Complete: {task_name}"
        body = f"**Task:** {task_name}\n\n"
        body += f"**Result:** {result}\n\n"
        if details:
            body += f"**Details:**\n{details}"
        return self.send_message(title, body, "sync")
    
    def report_data_update(self, data_type: str, record_count: int, file_path: str = None):
        """报告数据更新"""
        title = f"Data Update: {data_type}"
        body = f"**Data Type:** {data_type}\n\n"
        body += f"**Records:** {record_count}\n\n"
        if file_path:
            body += f"**File:** `{file_path}`"
        return self.send_message(title, body, "data")
    
    def send_alert(self, alert_type: str, message: str, priority: str = "normal"):
        """发送告警"""
        title = f"Alert: {alert_type} [{priority.upper()}]"
        body = f"**Priority:** {priority}\n\n"
        body += f"**Message:**\n{message}"
        return self.send_message(title, body, "alert")
    
    def send_heartbeat(self, status: str = "online", stats: Dict = None):
        """发送心跳"""
        title = f"Heartbeat: {status}"
        body = f"**Status:** {status}\n\n"
        if stats:
            body += "**Stats:**\n"
            for key, value in stats.items():
                body += f"- {key}: {value}\n"
        return self.send_message(title, body, "heartbeat")
    
    def request_sync(self, sync_type: str = "full"):
        """请求同步"""
        title = f"Sync Request: {sync_type}"
        body = f"Requesting {sync_type} synchronization.\n\n"
        body += "Please confirm and start sync when ready."
        return self.send_message(title, body, "sync")
    
    # ===== 配置管理 =====
    
    def save_config(self, repo_owner: str, repo_name: str, github_token: str):
        """保存配置"""
        config = {
            "repo_owner": repo_owner,
            "repo_name": repo_name,
            "github_token": github_token,
            "configured_at": datetime.now().isoformat()
        }
        config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/github_messenger_config.json")
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token
        self.api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    
    def load_config(self) -> bool:
        """加载配置"""
        config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/github_messenger_config.json")
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.repo_owner = config.get("repo_owner")
            self.repo_name = config.get("repo_name")
            self.github_token = config.get("github_token")
            if self.repo_owner and self.repo_name:
                self.api_base = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
            return True
        return False


class OfflineMode:
    """
    离线模式 - 通过文件系统实现消息交换
    当GitHub不可用时使用
    """
    
    def __init__(self, sync_dir: str = None):
        self.sync_dir = Path(sync_dir) if sync_dir else \
            Path("C:/Users/ThinkPad/.openclaw/workspace/sync/offline")
        self.sync_dir.mkdir(parents=True, exist_ok=True)
        
        self.my_id = "xiaotian_local"
        self.brother_id = "xiaotian_cloud"
    
    def send_message(self, title: str, body: str, msg_type: str = "general"):
        """发送消息到同步目录"""
        message = {
            "id": f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.my_id}",
            "from": self.my_id,
            "to": self.brother_id,
            "type": msg_type,
            "title": title,
            "body": body,
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存到outbox
        outbox_file = self.sync_dir / "outbox" / f"{message['id']}.json"
        outbox_file.parent.mkdir(exist_ok=True)
        with open(outbox_file, "w", encoding="utf-8") as f:
            json.dump(message, f, indent=2)
        
        return {"success": True, "message_id": message["id"], "mode": "offline"}
    
    def check_inbox(self) -> List[Dict]:
        """检查收件箱"""
        inbox_dir = self.sync_dir / "inbox"
        if not inbox_dir.exists():
            return []
        
        messages = []
        for msg_file in inbox_dir.glob("*.json"):
            with open(msg_file, "r", encoding="utf-8") as f:
                messages.append(json.load(f))
            # 标记为已读
            msg_file.rename(msg_file.with_suffix(".read"))
        
        return sorted(messages, key=lambda x: x["timestamp"])


def main():
    """测试GitHub Messenger"""
    print("=" * 50)
    print("TwinSync GitHub - GitHub-based Messaging")
    print("=" * 50)
    
    # 测试离线模式
    print("\n[Offline Mode Test]")
    offline = OfflineMode()
    result = offline.send_message(
        "Test Message",
        "This is a test message in offline mode",
        "general"
    )
    print(f"Sent: {result}")
    
    # 显示配置方法
    print("\n[Configuration]")
    print("To use GitHub Issues for messaging:")
    print("1. Create a GitHub repository")
    print("2. Get GitHub Personal Access Token")
    print("3. Run: messenger.save_config(owner, repo, token)")
    
    print("\n[Message Types]")
    types = ["message", "sync", "alert", "data", "heartbeat"]
    for t in types:
        print(f"  - {t}")
    
    print("\n" + "=" * 50)
    print("GitHub Messenger ready!")
    print("Alternative to Telegram - no phone number required!")
    print("=" * 50)


if __name__ == "__main__":
    main()
