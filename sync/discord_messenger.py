"""
Discord Sync - Discord-based messaging for AI Twins
基于Discord的双生AI通信系统
"""
import json
import aiohttp
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class DiscordMessenger:
    """
    Discord消息系统
    利用Discord Webhook实现双向通信
    """
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url
        
        # 身份标识
        self.my_id = "xiaotian_local"
        self.brother_id = "xiaotian_cloud"
        
        # 消息缓存
        self.message_cache_dir = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/discord_messages")
        self.message_cache_dir.mkdir(parents=True, exist_ok=True)
    
    async def send_message(self, content: str, msg_type: str = "general", 
                          title: str = None) -> Dict:
        """
        发送消息到Discord
        """
        if not self.webhook_url:
            return {"error": "Discord not configured", "message": content}
        
        # 格式化消息
        formatted_content = self._format_message(content, msg_type, title)
        
        # 构建embed
        embed = self._build_embed(content, msg_type, title)
        
        payload = {
            "content": formatted_content,
            "embeds": [embed],
            "username": self.my_id
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 204:
                        # 缓存消息
                        self._cache_message({
                            "direction": "sent",
                            "type": msg_type,
                            "content": content,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        return {
                            "success": True,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        text = await response.text()
                        return {"error": f"HTTP {response.status}: {text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _format_message(self, content: str, msg_type: str, title: str = None) -> str:
        """格式化消息"""
        emoji_map = {
            "task_complete": "✅",
            "data_update": "📊",
            "alert": "🚨",
            "query": "❓",
            "heartbeat": "💓",
            "sync": "🔄",
            "general": "💬"
        }
        
        emoji = emoji_map.get(msg_type, "💬")
        header = f"[{self.my_id}] {emoji}"
        if title:
            header += f" {title}"
        
        return f"{header}\n\n{content}"
    
    def _build_embed(self, content: str, msg_type: str, title: str = None) -> Dict:
        """构建Discord embed"""
        color_map = {
            "task_complete": 0x00FF00,  # Green
            "data_update": 0x0000FF,    # Blue
            "alert": 0xFF0000,          # Red
            "query": 0xFFFF00,          # Yellow
            "heartbeat": 0xFF00FF,      # Purple
            "sync": 0x00FFFF,           # Cyan
            "general": 0x808080         # Gray
        }
        
        embed = {
            "title": title or f"{msg_type.upper()}",
            "description": content[:2000],  # Discord限制
            "color": color_map.get(msg_type, 0x808080),
            "footer": {
                "text": f"From: {self.my_id} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
        }
        
        return embed
    
    def _cache_message(self, message: Dict):
        """缓存消息"""
        cache_file = self.message_cache_dir / f"{datetime.now():%Y%m%d}.jsonl"
        with open(cache_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
    
    # ===== 快捷消息方法 =====
    
    async def report_task_complete(self, task_name: str, result: str, details: str = None):
        """报告任务完成"""
        content = f"**Result:** {result}\n"
        if details:
            content += f"**Details:** {details}"
        return await self.send_message(content, "task_complete", f"Task Complete: {task_name}")
    
    async def report_data_update(self, data_type: str, record_count: int, file_path: str = None):
        """报告数据更新"""
        content = f"**Records:** {record_count}\n"
        if file_path:
            content += f"**File:** `{file_path}`"
        return await self.send_message(content, "data_update", f"Data Update: {data_type}")
    
    async def send_alert(self, alert_type: str, message: str, priority: str = "normal"):
        """发送告警"""
        content = f"**Priority:** {priority}\n\n**Message:**\n{message}"
        return await self.send_alert(content, "alert", f"Alert: {alert_type}")
    
    async def send_heartbeat(self, status: str = "online", stats: Dict = None):
        """发送心跳"""
        content = f"**Status:** {status}\n"
        if stats:
            content += "\n**Stats:**\n"
            for key, value in stats.items():
                content += f"• {key}: {value}\n"
        return await self.send_message(content, "heartbeat", "Heartbeat")
    
    async def request_sync(self, sync_type: str = "full"):
        """请求同步"""
        content = f"Requesting {sync_type} synchronization.\n\nPlease confirm and start sync."
        return await self.send_message(content, "sync", f"Sync Request: {sync_type}")
    
    # ===== 配置管理 =====
    
    def save_config(self, webhook_url: str):
        """保存配置"""
        config = {
            "webhook_url": webhook_url,
            "configured_at": datetime.now().isoformat()
        }
        config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/discord_config.json")
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        self.webhook_url = webhook_url
    
    def load_config(self) -> bool:
        """加载配置"""
        config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/discord_config.json")
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.webhook_url = config.get("webhook_url")
            return True
        return False


class DiscordSyncManager:
    """Discord同步管理器"""
    
    def __init__(self):
        self.messenger = DiscordMessenger()
        self.messenger.load_config()
    
    async def send_daily_summary(self):
        """发送每日总结"""
        summary = f"""**Daily Summary - Day 1**

**Achievements:**
• Created 15 tools/modules
• Completed 6 core tasks
• Established twin-AI sync system

**Tomorrow's Plan:**
1. Configure Discord with twin
2. Test bidirectional messaging
3. First GitHub code sync
4. Collect stock data
5. Review twin's knowledge

**Status:** Ready for collaborative evolution!"""
        
        return await self.messenger.send_message(summary, "general", "Day 1 Complete!")
    
    async def test_connection(self):
        """测试连接"""
        return await self.messenger.send_message(
            "Hello from XiaoTian Local! Discord connection test.",
            "general",
            "Connection Test"
        )


def main():
    """测试Discord Messenger"""
    print("=" * 50)
    print("Discord Messenger - Twin Communication")
    print("=" * 50)
    
    messenger = DiscordMessenger()
    
    # 尝试加载配置
    if messenger.load_config():
        print("\n[OK] Discord config loaded")
        print(f"   Webhook configured: {messenger.webhook_url[:50]}...")
    else:
        print("\n[!] Discord not configured")
        print("   Steps:")
        print("   1. Create Discord server: 'XiaoTian Twins'")
        print("   2. Create Webhook in #sync channel")
        print("   3. Copy Webhook URL")
        print("   4. Run: messenger.save_config('webhook_url')")
    
    print("\n[Message Types]")
    types = ["task_complete", "data_update", "alert", "heartbeat", "sync", "general"]
    for t in types:
        print(f"  - {t}")
    
    print("\n[Usage Example]")
    print("  import asyncio")
    print("  from sync.discord_messenger import DiscordMessenger")
    print("  messenger = DiscordMessenger()")
    print("  asyncio.run(messenger.send_message('Hello!', 'general'))")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
