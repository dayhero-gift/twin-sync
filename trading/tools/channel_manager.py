"""
Multi-Channel Messenger - Multi-platform message integration
Supports Telegram, WhatsApp, and other platforms
"""
import json
from pathlib import Path
from typing import List, Dict, Optional


class ChannelManager:
    """Multi-channel message manager"""
    
    def __init__(self, config_dir: str = None):
        self.config_dir = Path(config_dir) if config_dir else \
            Path("C:/Users/ThinkPad/.openclaw/workspace/config")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "channels.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load channel configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "channels": {
                "telegram": {"enabled": False, "bot_token": None, "chat_id": None},
                "whatsapp": {"enabled": False, "phone": None, "api_key": None},
                "discord": {"enabled": False, "webhook_url": None},
                "email": {"enabled": False, "smtp_server": None, "username": None}
            }
        }
    
    def _save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_channel_status(self) -> Dict:
        """Get all channel status"""
        return {
            channel: {
                "enabled": info.get("enabled", False),
                "configured": self._is_configured(channel, info)
            }
            for channel, info in self.config["channels"].items()
        }
    
    def _is_configured(self, channel: str, info: Dict) -> bool:
        """Check if channel is properly configured"""
        if channel == "telegram":
            return bool(info.get("bot_token") and info.get("chat_id"))
        elif channel == "whatsapp":
            return bool(info.get("phone") and info.get("api_key"))
        elif channel == "discord":
            return bool(info.get("webhook_url"))
        elif channel == "email":
            return bool(info.get("smtp_server") and info.get("username"))
        return False
    
    def configure_telegram(self, bot_token: str, chat_id: str):
        """Configure Telegram channel"""
        self.config["channels"]["telegram"] = {
            "enabled": True,
            "bot_token": bot_token,
            "chat_id": chat_id
        }
        self._save_config()
        return {"success": True, "channel": "telegram", "status": "configured"}
    
    def configure_whatsapp(self, phone: str, api_key: str):
        """Configure WhatsApp channel"""
        self.config["channels"]["whatsapp"] = {
            "enabled": True,
            "phone": phone,
            "api_key": api_key
        }
        self._save_config()
        return {"success": True, "channel": "whatsapp", "status": "configured"}
    
    def configure_discord(self, webhook_url: str):
        """Configure Discord channel"""
        self.config["channels"]["discord"] = {
            "enabled": True,
            "webhook_url": webhook_url
        }
        self._save_config()
        return {"success": True, "channel": "discord", "status": "configured"}
    
    def enable_channel(self, channel: str):
        """Enable a channel"""
        if channel in self.config["channels"]:
            self.config["channels"][channel]["enabled"] = True
            self._save_config()
            return {"success": True, "channel": channel, "enabled": True}
        return {"success": False, "error": f"Unknown channel: {channel}"}
    
    def disable_channel(self, channel: str):
        """Disable a channel"""
        if channel in self.config["channels"]:
            self.config["channels"][channel]["enabled"] = False
            self._save_config()
            return {"success": True, "channel": channel, "enabled": False}
        return {"success": False, "error": f"Unknown channel: {channel}"}
    
    def get_setup_guide(self, channel: str) -> str:
        """Get setup guide for a channel"""
        guides = {
            "telegram": """
=== Telegram Setup Guide ===
1. Talk to @BotFather on Telegram
2. Create a new bot with /newbot
3. Copy the bot token (format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)
4. Get your chat ID by messaging @userinfobot
5. Configure with: configure_telegram(bot_token, chat_id)

Install skill: npx skills add composiohq/awesome-claude-skills@telegram-automation
""",
            "whatsapp": """
=== WhatsApp Setup Guide ===
1. Use WhatsApp Business API or third-party service (like Twilio)
2. Get your phone number and API key
3. Configure with: configure_whatsapp(phone, api_key)

Install skill: npx skills add composiohq/awesome-claude-skills@whatsapp-automation
""",
            "discord": """
=== Discord Setup Guide ===
1. Go to your Discord server settings
2. Integrations -> Webhooks
3. Create a new webhook and copy the URL
4. Configure with: configure_discord(webhook_url)
"""
        }
        return guides.get(channel, f"No guide available for {channel}")


def main():
    """Test channel manager"""
    print("=" * 50)
    print("Multi-Channel Messenger Test")
    print("=" * 50)
    
    manager = ChannelManager()
    
    # Show current status
    print("\nChannel Status:")
    status = manager.get_channel_status()
    for channel, info in status.items():
        icon = "OK" if info["configured"] else "NO"
        status_text = "ON" if info["enabled"] else "OFF"
        print(f"  [{icon}] {channel}: {status_text} ({'configured' if info['configured'] else 'not configured'})")
    
    # Show setup guide
    print("\n" + manager.get_setup_guide("telegram"))


if __name__ == "__main__":
    main()
