"""
Feishu Sync - Feishu/Lark-based messaging for AI Twins
基于飞书的双生AI通信系统
"""
import json
import aiohttp
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class FeishuMessenger:
    """
    飞书消息系统
    利用飞书Bot实现双向通信
    """
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url
        
        # 身份标识
        self.my_id = "xiaotian_local"
        self.brother_id = "xiaotian_cloud"
        
        # 消息缓存
        self.message_cache_dir = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/feishu_messages")
        self.message_cache_dir.mkdir(parents=True, exist_ok=True)
    
    async def send_message(self, content: str, msg_type: str = "text", 
                          title: str = None) -> Dict:
        """
        发送消息到飞书
        """
        if not self.webhook_url:
            return {"error": "Feishu not configured", "message": content}
        
        # 飞书卡片消息格式
        if msg_type == "interactive":
            payload = self._build_card_message(content, title)
        else:
            payload = {
                "msg_type": "text",
                "content": {
                    "text": f"[{self.my_id}] {title or ''}\n\n{content}"
                }
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    result = await response.json()
                    
                    if result.get("code") == 0:
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
                        return {"error": result.get("msg", "Unknown error")}
        except Exception as e:
            return {"error": str(e)}
    
    def _build_card_message(self, content: str, title: str = None) -> Dict:
        """构建飞书卡片消息"""
        color_map = {
            "task_complete": "green",
            "data_update": "blue", 
            "alert": "red",
            "query": "yellow",
            "heartbeat": "purple",
            "sync": "cyan",
            "general": "grey"
        }
        
        return {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title or "Message"
                    },
                    "template": color_map.get("general", "blue")
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content
                        }
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": f"From: {self.my_id} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            }
                        ]
                    }
                ]
            }
        }
    
    def _cache_message(self, message: Dict):
        """缓存消息"""
        cache_file = self.message_cache_dir / f"{datetime.now():%Y%m%d}.jsonl"
        with open(cache_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")
    
    # ===== 快捷消息方法 =====
    
    async def report_task_complete(self, task_name: str, result: str, details: str = None):
        """报告任务完成"""
        content = f"**任务:** {task_name}\n"
        content += f"**结果:** {result}\n"
        if details:
            content += f"**详情:** {details}"
        
        card = self._build_task_card(task_name, result, details)
        return await self._send_card(card)
    
    def _build_task_card(self, task_name: str, result: str, details: str = None) -> Dict:
        """构建任务完成卡片"""
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**任务:** {task_name}\n**结果:** {result}"
                }
            }
        ]
        
        if details:
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**详情:** {details}"
                }
            })
        
        elements.append({
            "tag": "note",
            "elements": [
                {
                    "tag": "plain_text",
                    "content": f"From: {self.my_id} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            ]
        })
        
        return {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"✅ 任务完成: {task_name}"
                    },
                    "template": "green"
                },
                "elements": elements
            }
        }
    
    async def _send_card(self, card: Dict) -> Dict:
        """发送卡片消息"""
        if not self.webhook_url:
            return {"error": "Feishu not configured"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=card) as response:
                    result = await response.json()
                    
                    if result.get("code") == 0:
                        self._cache_message({
                            "direction": "sent",
                            "type": "card",
                            "timestamp": datetime.now().isoformat()
                        })
                        return {"success": True}
                    else:
                        return {"error": result.get("msg")}
        except Exception as e:
            return {"error": str(e)}
    
    async def report_data_update(self, data_type: str, record_count: int, file_path: str = None):
        """报告数据更新"""
        content = f"**数据类型:** {data_type}\n"
        content += f"**记录数:** {record_count}\n"
        if file_path:
            content += f"**文件:** {file_path}"
        
        card = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"📊 数据更新: {data_type}"
                    },
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content
                        }
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": f"From: {self.my_id} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            }
                        ]
                    }
                ]
            }
        }
        
        return await self._send_card(card)
    
    async def send_alert(self, alert_type: str, message: str, priority: str = "normal"):
        """发送告警"""
        color = "red" if priority == "high" else "orange"
        
        card = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"🚨 告警: {alert_type} [{priority.upper()}]"
                    },
                    "template": color
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": message
                        }
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": f"From: {self.my_id} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            }
                        ]
                    }
                ]
            }
        }
        
        return await self._send_card(card)
    
    async def send_heartbeat(self, status: str = "online", stats: Dict = None):
        """发送心跳"""
        content = f"**状态:** {status}\n"
        if stats:
            for key, value in stats.items():
                content += f"• {key}: {value}\n"
        
        card = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "💓 心跳"
                    },
                    "template": "purple"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content
                        }
                    }
                ]
            }
        }
        
        return await self._send_card(card)
    
    async def request_sync(self, sync_type: str = "full"):
        """请求同步"""
        card = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"🔄 同步请求: {sync_type}"
                    },
                    "template": "cyan"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"请求{sync_type}同步，请确认后开始。"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "确认同步"
                                },
                                "type": "primary",
                                "value": {"action": "confirm_sync"}
                            }
                        ]
                    }
                ]
            }
        }
        
        return await self._send_card(card)
    
    # ===== 配置管理 =====
    
    def save_config(self, webhook_url: str):
        """保存配置"""
        config = {
            "webhook_url": webhook_url,
            "configured_at": datetime.now().isoformat()
        }
        config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/feishu_config.json")
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        self.webhook_url = webhook_url
    
    def load_config(self) -> bool:
        """加载配置"""
        config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/feishu_config.json")
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.webhook_url = config.get("webhook_url")
            return True
        return False
    
    def is_configured(self) -> bool:
        """检查是否已配置"""
        return bool(self.webhook_url)


class FeishuSyncManager:
    """飞书同步管理器"""
    
    def __init__(self):
        self.messenger = FeishuMessenger()
        self.messenger.load_config()
    
    async def send_daily_summary(self):
        """发送每日总结"""
        content = """**Day 1 总结**

**成果:**
• 创建15个工具/模块
• 完成6个核心任务
• 建立双生AI同步系统

**明日计划:**
1. 与兄弟同步配置
2. 测试双向通信
3. 首次代码同步
4. 采集股票数据
5. 复习兄弟知识

**状态:** 准备就绪，等待协同！"""
        
        card = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "📋 Day 1 完成总结"
                    },
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content
                        }
                    }
                ]
            }
        }
        
        return await self.messenger._send_card(card)
    
    async def test_connection(self):
        """测试连接"""
        return await self.messenger.send_message(
            "Hello from XiaoTian Local! 飞书连接测试。",
            "text",
            "连接测试"
        )


def main():
    """测试飞书 Messenger"""
    print("=" * 50)
    print("Feishu Messenger - Twin Communication")
    print("=" * 50)
    
    messenger = FeishuMessenger()
    
    # 尝试加载配置
    if messenger.load_config():
        print("\n[OK] Feishu config loaded")
        print(f"   Webhook: {messenger.webhook_url[:50]}...")
    else:
        print("\n[!] Feishu not configured")
        print("   Waiting for Luojun to provide webhook URL...")
        print("\n   To configure:")
        print("   messenger.save_config('https://open.feishu.cn/open-apis/bot/v2/hook/...')")
    
    print("\n[Features]")
    print("  - Text messages")
    print("  - Interactive cards (color-coded)")
    print("  - Task completion reports")
    print("  - Data updates")
    print("  - Alerts")
    print("  - Heartbeats")
    
    print("\n[Usage Example]")
    print("  import asyncio")
    print("  from sync.feishu_messenger import FeishuMessenger")
    print("  messenger = FeishuMessenger()")
    print("  asyncio.run(messenger.send_message('Hello!', 'text'))")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
