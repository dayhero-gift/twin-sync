"""
Feishu App Bot - Connect using App ID and Secret
使用飞书应用凭证连接
"""
import json
import aiohttp
import asyncio
from datetime import datetime
from pathlib import Path


class FeishuAppBot:
    """飞书应用机器人"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self.tenant_access_token = None
        
    async def get_tenant_access_token(self) -> str:
        """获取租户访问令牌"""
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    result = await response.json()
                    
                    if result.get("code") == 0:
                        self.tenant_access_token = result["tenant_access_token"]
                        return self.tenant_access_token
                    else:
                        print(f"Error: {result}")
                        return None
        except Exception as e:
            print(f"Exception: {e}")
            return None
    
    async def send_message_to_group(self, group_chat_id: str, content: str):
        """发送消息到群组"""
        if not self.tenant_access_token:
            await self.get_tenant_access_token()
        
        url = f"{self.base_url}/im/v1/messages"
        
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": group_chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": content})
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    result = await response.json()
                    return result
        except Exception as e:
            return {"error": str(e)}
    
    async def get_group_list(self):
        """获取群组列表"""
        if not self.tenant_access_token:
            await self.get_tenant_access_token()
        
        url = f"{self.base_url}/im/v1/chats"
        
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    result = await response.json()
                    return result
        except Exception as e:
            return {"error": str(e)}


async def test_connection():
    """测试连接"""
    # 加载配置
    config_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/feishu_app_config.json")
    with open(config_file, "r") as f:
        config = json.load(f)
    
    bot = FeishuAppBot(config["app_id"], config["app_secret"])
    
    print("Getting tenant access token...")
    token = await bot.get_tenant_access_token()
    
    if token:
        print(f"[OK] Success! Token: {token[:20]}...")
        
        # 获取群组列表
        print("\nGetting group list...")
        groups = await bot.get_group_list()
        print(json.dumps(groups, indent=2, ensure_ascii=False))
        
        return True
    else:
        print("[ERR] Failed to get token")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_connection())
