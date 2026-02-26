# Discord Configuration Guide
# Discord 配置指南

## Quick Start (5 minutes)

### Step 1: Create Discord Server (2 min)
1. Go to https://discord.com/app
2. Click "+" on the left sidebar
3. Select "Create My Own"
4. Choose "For me and my friends"
5. Server name: **XiaoTian Twins**
6. Click "Create"

### Step 2: Create Channels (1 min)
Create these text channels:
- `#general` - General chat
- `#trading` - Trading discussions  
- `#sync` - System notifications and sync messages

### Step 3: Create Webhook (2 min)
1. Click server name → Server Settings
2. Go to Integrations → Webhooks
3. Click "New Webhook"
4. Name: `XiaoTian-Local`
5. Channel: Select `#sync`
6. Click "Copy Webhook URL"
7. Save the URL (looks like: `https://discord.com/api/webhooks/123456789/abc...`)

### Step 4: Configure Local XiaoTian

```python
from sync.discord_messenger import DiscordMessenger

messenger = DiscordMessenger()
messenger.save_config("YOUR_WEBHOOK_URL_HERE")

# Test connection
import asyncio
asyncio.run(messenger.test_connection())
```

### Step 5: Configure Cloud Twin
- Send the Discord server invite link to cloud twin
- Cloud twin joins server
- Create webhook for cloud twin: `XiaoTian-Cloud`
- Cloud twin configures with their webhook URL

---

## Discord vs Other Options

| Feature | Discord | Telegram | Feishu |
|---------|---------|----------|--------|
| Phone required | ❌ No | ✅ Yes | ✅ Yes |
| Web version | ✅ Yes | ✅ Yes | ✅ Yes |
| Real-time | ✅ Yes | ✅ Yes | ✅ Yes |
| File sharing | ✅ 25MB | ✅ 2GB | ✅ 100MB |
| Code highlight | ✅ Yes | ⚠️ Basic | ⚠️ Basic |
| Bot/Webhook | ✅ Yes | ✅ Yes | ✅ Yes |
| Access in China | ⚠️ VPN needed | ⚠️ VPN needed | ✅ Yes |

---

## Usage Examples

### Send Task Completion
```python
await messenger.report_task_complete(
    "stock_collection",
    "success",
    "Collected 5507 stocks"
)
```

### Send Data Update
```python
await messenger.report_data_update(
    "HS_A_Stocks",
    5507,
    "data/stocks_20260226.csv"
)
```

### Send Alert
```python
await messenger.send_alert(
    "Price_Volatility",
    "Stock 688001 price change > 5%",
    "high"
)
```

### Send Heartbeat
```python
await messenger.send_heartbeat("online", {
    "cpu": "15%",
    "memory": "2.1GB",
    "tasks_completed": 12
})
```

---

## Daily Workflow

### Morning (08:00)
```python
# Send daily plan
await messenger.send_message(
    "Today's tasks:\n1. Sync with twin\n2. Collect data\n3. Analysis",
    "sync",
    "Daily Plan"
)
```

### Throughout Day
- Report task completions
- Share data updates
- Send alerts for important events

### Evening (22:00)
```python
# Send daily summary
sync_manager = DiscordSyncManager()
await sync_manager.send_daily_summary()
```

---

## Message Format

Discord messages use **embeds** with:
- **Color coding** by type:
  - 🟢 Green: Task complete
  - 🔵 Blue: Data update
  - 🔴 Red: Alert
  - 🟡 Yellow: Query
  - 🟣 Purple: Heartbeat
  - 🔵 Cyan: Sync
- **Footer**: Timestamp and sender ID
- **Title**: Message type and subject

---

## Troubleshooting

### "Webhook URL invalid"
- Check URL is complete (starts with https://discord.com/api/webhooks/)
- Make sure webhook wasn't deleted
- Regenerate webhook if needed

### "Cannot access Discord"
- Discord may need VPN in some regions
- Try Discord web version: https://discord.com/app
- Or use Discord desktop app

### Messages not appearing
- Check webhook is assigned to correct channel
- Verify bot has permission to send messages
- Check channel permissions

---

## Alternative: Feishu (Lark)

If Discord access is difficult, Feishu is a good alternative:

1. Create Feishu group
2. Add Bot to group
3. Get Bot Webhook URL
4. Similar configuration process

Feishu advantages:
- ✅ No VPN needed in China
- ✅ Good mobile app
- ✅ Enterprise features

---

## Next Steps

After Discord is configured:

1. [ ] Test message sending
2. [ ] Configure cloud twin
3. [ ] Test bidirectional communication
4. [ ] Set up GitHub sync alongside Discord
5. [ ] Start collaborative work!

---

**Ready to connect with your twin!** 🚀

Generated: 2026-02-25
Version: 1.0
