"""
TwinSync - Telegram Messenger for AI Twins
双生AI同步系统 - Telegram消息层
用于小天（本地）和云端兄弟的实时通信
"""
import json
import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class TwinMessenger:
    """
    双生AI消息系统
    通过Telegram Bot实现本地与云端的实时通信
    """
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_base = f"https://api.telegram.org/bot{bot_token}" if bot_token else None
        
        # 身份标识
        self.my_id = "xiaotian_local"  # 小天的标识
        self.brother_id = "xiaotian_cloud"  # 兄弟的标识
        
        # 消息缓存
        self.message_cache_dir = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/messages")
        self.message_cache_dir.mkdir(parents=True, exist_ok=True)
    
    async def send_message(self, text: str, message_type: str = "general") -> Dict:
        """
        发送消息给兄弟（通过Telegram群组）
        """
        if not self.bot_token or not self.chat_id:
            return {"error": "Telegram not configured", "message": text}
        
        # 格式化消息
        formatted_msg = self._format_message(text, message_type)
        
        url = f"{self.api_base}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": formatted_msg,
            "parse_mode": "Markdown"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    result = await response.json()
                    
                    # 缓存消息
                    self._cache_message({
                        "direction": "sent",
                        "type": message_type,
                        "content": text,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    return {
                        "success": result.get("ok"),
                        "message_id": result.get("result", {}).get("message_id"),
                        "timestamp": datetime.now().isoformat()
                    }
        except Exception as e:
            return {"error": str(e), "message": text}
    
    def _format_message(self, text: str, msg_type: str) -> str:
        """格式化消息，添加元数据"""
        emoji_map = {
            "task_complete": "[OK]",
            "data_update": "[DATA]",
            "alert": "[ALERT]",
            "query": "[?]",
            "heartbeat": "[HEART]",
            "sync": "[SYNC]",
            "general": "[MSG]"
        }
        
        emoji = emoji_map.get(msg_type, "[MSG]")
        header = f"{emoji} *{self.my_id}* | {msg_type.upper()}\n"
        footer = f"\n\n`{datetime.now().strftime('%H:%M:%S')}`"
        
        return header + text + footer
    
    def _cache_message(self, message: Dict):
        """缓存消息到本地"""
        cache_file = self.message_cache_dir / f"{datetime.now():%Y%m%d}.jsonl"
        with open(cache_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
    
    # ===== 预设消息模板 =====
    
    async def report_task_complete(self, task_name: str, result: str, details: str = None):
        """报告任务完成"""
        text = f"*任务完成*: {task_name}\n"
        text += f"结果: {result}\n"
        if details:
            text += f"详情: {details}"
        return await self.send_message(text, "task_complete")
    
    async def report_data_update(self, data_type: str, record_count: int, file_path: str = None):
        """报告数据更新"""
        text = f"*数据更新*: {data_type}\n"
        text += f"记录数: {record_count}\n"
        if file_path:
            text += f"文件: `{file_path}`"
        return await self.send_message(text, "data_update")
    
    async def send_alert(self, alert_type: str, message: str, priority: str = "normal"):
        """发送告警"""
        text = f"*告警*: {alert_type} (优先级: {priority})\n"
        text += f"{message}"
        return await self.send_message(text, "alert")
    
    async def send_heartbeat(self, status: str = "online", stats: Dict = None):
        """发送心跳"""
        text = f"*状态*: {status}\n"
        if stats:
            for key, value in stats.items():
                text += f"{key}: {value}\n"
        return await self.send_message(text, "heartbeat")
    
    async def request_sync(self, sync_type: str = "full"):
        """请求同步"""
        text = f"*请求同步*: {sync_type}\n"
        text += "请回复确认开始同步"
        return await self.send_message(text, "sync")
    
    async def query_brother(self, question: str):
        """向兄弟查询"""
        text = f"*查询*: {question}"
        return await self.send_message(text, "query")
    
    # ===== 配置管理 =====
    
    def save_config(self, bot_token: str, chat_id: str):
        """保存配置"""
        config = {
            "bot_token": bot_token,
            "chat_id": chat_id,
            "configured_at": datetime.now().isoformat()
        }
        config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/telegram_config.json")
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_base = f"https://api.telegram.org/bot{bot_token}"
    
    def load_config(self) -> bool:
        """加载配置"""
        config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/telegram_config.json")
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.bot_token = config.get("bot_token")
            self.chat_id = config.get("chat_id")
            if self.bot_token:
                self.api_base = f"https://api.telegram.org/bot{self.bot_token}"
            return True
        return False
    
    def is_configured(self) -> bool:
        """检查是否已配置"""
        return bool(self.bot_token and self.chat_id)


class DailySync:
    """每日同步清单"""
    
    SYNC_ITEMS = [
        ("读取兄弟MEMORY.md", "pull"),
        ("同步新技能代码", "sync"),
        ("同步当日股票数据", "sync"),
        ("交换市场观察", "push"),
        ("确认明日分工", "both")
    ]
    
    def __init__(self):
        self.sync_dir = Path("C:/Users/ThinkPad/.openclaw/workspace/sync")
        self.sync_dir.mkdir(parents=True, exist_ok=True)
        self.checklist_file = self.sync_dir / "daily_sync_checklist.json"
    
    def generate_checklist(self) -> Dict:
        """生成今日同步清单"""
        checklist = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "items": []
        }
        
        for item, direction in self.SYNC_ITEMS:
            checklist["items"].append({
                "task": item,
                "direction": direction,
                "status": "pending",
                "completed_at": None
            })
        
        return checklist
    
    def save_checklist(self, checklist: Dict):
        """保存清单"""
        with open(self.checklist_file, "w", encoding="utf-8") as f:
            json.dump(checklist, f, indent=2)
    
    def load_checklist(self) -> Dict:
        """加载清单"""
        if self.checklist_file.exists():
            with open(self.checklist_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return self.generate_checklist()
    
    def mark_complete(self, task_index: int):
        """标记任务完成"""
        checklist = self.load_checklist()
        if 0 <= task_index < len(checklist["items"]):
            checklist["items"][task_index]["status"] = "completed"
            checklist["items"][task_index]["completed_at"] = datetime.now().isoformat()
            self.save_checklist(checklist)
    
    def get_progress(self) -> str:
        """获取进度字符串"""
        checklist = self.load_checklist()
        completed = sum(1 for item in checklist["items"] if item["status"] == "completed")
        total = len(checklist["items"])
        return f"{completed}/{total}"


def main():
    """测试双生AI消息系统"""
    print("=" * 50)
    print("TwinSync - Telegram Messenger Test")
    print("=" * 50)
    
    messenger = TwinMessenger()
    
    # 尝试加载配置
    if messenger.load_config():
        print("\n[OK] Telegram config loaded")
        print(f"   Chat ID: {messenger.chat_id}")
    else:
        print("\n[!] Telegram not configured")
        print("   Run: messenger.save_config(bot_token, chat_id)")
    
    # 显示每日同步清单
    print("\n[Daily Sync Checklist]")
    sync = DailySync()
    checklist = sync.generate_checklist()
    for i, item in enumerate(checklist["items"], 1):
        direction = {"pull": "<--", "push": "-->", "sync": "<->", "both": "<=>"}.get(item["direction"], "*")
        print(f"   {i}. {direction} {item['task']}")
    
    # 测试消息格式化
    print("\n[Message Format Example]")
    example = messenger._format_message(
        "Task completed: stock_collector\nRecords: 5507",
        "task_complete"
    )
    print(example)
    
    print("\n" + "=" * 50)
    print("TwinSync ready!")
    print("Configure Telegram to start messaging with your twin.")
    print("=" * 50)


if __name__ == "__main__":
    main()
