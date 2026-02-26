# TwinSync Configuration Guide
# 双生AI同步系统配置指南

## Overview
This guide helps you configure the synchronization system between:
- **XiaoTian Local** (deployed on your computer)
- **XiaoTian Cloud** (deployed on cloud server)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Real-time Messaging (Telegram)                │
│  - Instant notifications, status reports, alerts        │
│  - Bidirectional: Local ↔ Cloud                         │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Code/Knowledge Sync (GitHub Private Repo)     │
│  - Skill code migration                                 │
│  - MEMORY.md / AGENTS.md version sync                   │
│  - Learning outcomes sharing                            │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Big Data/Files (Cloud Storage)                │
│  - Stock historical data                                │
│  - Knowledge base documents                             │
│  - Screenshots/videos                                   │
└─────────────────────────────────────────────────────────┘
```

---

## Step 1: Telegram Setup (Tonight)

### 1.1 Create Telegram Group
1. Open Telegram app
2. Create a new group: "XiaoTian Twins"
3. Add your own account
4. Get the chat ID (use @userinfobot or @RawDataBot)

### 1.2 Create Telegram Bot
1. Message @BotFather
2. Send `/newbot`
3. Follow instructions to create bot
4. Save the bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Add bot to the "XiaoTian Twins" group

### 1.3 Configure Local XiaoTian
```python
from sync.twin_sync import TwinMessenger

messenger = TwinMessenger()
messenger.save_config(
    bot_token="YOUR_BOT_TOKEN_HERE",
    chat_id="YOUR_CHAT_ID_HERE"
)

# Test send message
import asyncio
asyncio.run(messenger.send_message(
    "Hello from XiaoTian Local!",
    "general"
))
```

### 1.4 Configure Cloud XiaoTian
Same steps as above, using the same bot token and chat ID.

---

## Step 2: GitHub Setup (Tomorrow)

### 2.1 Create Private Repository
1. Go to https://github.com/new
2. Repository name: `xiaotian-twins`
3. Make it **Private**
4. Initialize with README
5. Copy the repository URL

### 2.2 Configure Local XiaoTian
```python
from sync.github_sync import GitHubSync

sync = GitHubSync(repo_url="https://github.com/YOUR_USERNAME/xiaotian-twins.git")

# Initialize and clone
sync.clone_repo()

# First sync - push local code
sync.sync_to_github("Initial sync from local XiaoTian")
```

### 2.3 Configure Cloud XiaoTian
```python
# Clone the same repository
sync.clone_repo()

# Create cloud directory structure
# Push cloud-specific code
sync.sync_to_github("Initial sync from cloud XiaoTian")
```

### 2.4 Repository Structure
```
xiaotian-twins/
├── README.md
├── local/               # Local XiaoTian's code
│   ├── tools/
│   ├── brain/
│   └── MEMORY.md
├── cloud/               # Cloud XiaoTian's code
│   ├── tools/
│   ├── brain/
│   └── MEMORY.md
├── shared/              # Shared resources
│   ├── knowledge/
│   ├── stock_data/
│   └── decisions/
└── sync/                # Sync status
    ├── changelog.md
    └── sync_log.json
```

---

## Step 3: Daily Sync Protocol

### Morning Sync (08:00)
```python
from sync.twin_sync import DailySync
from sync.github_sync import SyncManager

# 1. Load daily checklist
daily = DailySync()
checklist = daily.load_checklist()

# 2. Pull brother's updates
manager = SyncManager()
results = manager.full_sync()

# 3. Read brother's MEMORY.md
# 4. Merge new skills
# 5. Sync stock data
# 6. Exchange observations
# 7. Confirm today's division of work

# 8. Mark tasks complete
daily.mark_complete(0)  # Example
```

### Evening Sync (22:00)
1. Push day's work to GitHub
2. Send summary to Telegram
3. Update changelog

---

## Step 4: Message Protocol

### Message Types
- `task_complete` - Task finished notification
- `data_update` - New data available
- `alert` - Important alert
- `query` - Question to brother
- `heartbeat` - Status report
- `sync` - Sync request

### Message Format
```json
{
  "from": "xiaotian_local",
  "to": "xiaotian_cloud",
  "type": "task_complete",
  "timestamp": "2026-02-25T23:30:00",
  "payload": {
    "task": "stock_collection",
    "result": "success",
    "records": 5507,
    "file": "shared/stock_data/20260225.csv"
  }
}
```

---

## Step 5: Division of Labor

### Local XiaoTian (You)
- ✅ TDX local data reading
- ✅ Local file system operations
- ✅ System command execution
- ✅ Broker auto-login (if applicable)
- ⚠️  Network access (limited by local network)

### Cloud XiaoTian (Brother)
- ✅ 7x24 market monitoring
- ✅ Financial news collection
- ✅ API data fetching
- ✅ Message push (if configured)
- ⚠️ No local file access

### Collaboration
- Both: Report sharing, code migration
- Both: Knowledge base building
- Both: Decision making

---

## Quick Start Commands

### Test Telegram
```python
python sync/twin_sync.py
```

### Test GitHub Sync
```python
python sync/github_sync.py
```

### Full Daily Sync
```python
from sync.github_sync import SyncManager
manager = SyncManager()
results = manager.full_sync()
print(results)
```

---

## Troubleshooting

### Telegram not working
- Check bot token format
- Verify bot is added to group
- Check chat ID is correct

### GitHub sync failed
- Check git is installed
- Verify repository URL
- Check authentication (SSH key or token)

### Sync conflicts
- Always pull before push
- Use changelog to track changes
- Communicate via Telegram for major changes

---

## Next Steps

1. [ ] Configure Telegram (both twins)
2. [ ] Test message exchange
3. [ ] Create GitHub private repo
4. [ ] First code sync
5. [ ] Set up daily sync automation
6. [ ] Start collaborative work!

---

## Contact

For issues or questions, contact Luojun.

Generated: 2026-02-25
Version: 1.0
