#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
"""
技能安装自动化脚本
每小时尝试安装一个新技能，直到全部完成
"""

import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

# 待安装技能列表（按优先级排序）
SKILLS_TO_INSTALL = [
    # 核心工具
    "skill-creator",
    "coding-agent", 
    "clawhub",
    "healthcheck",
    "gh-issues",
    # 消息通讯
    "discord",
    "slack",
    "himalaya",
    # 生产力
    "notion",
    "obsidian",
    # 媒体处理
    "openai-image-gen",
    "openai-whisper",
    # 其他
    "xurl",
    "mcporter",
]

LOG_FILE = Path("C:/Users/ThinkPad/.openclaw/workspace/skill_install_log.json")

def load_progress():
    """加载安装进度"""
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {"installed": [], "failed": [], "last_attempt": None}

def save_progress(progress):
    """保存安装进度"""
    with open(LOG_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def install_skill(skill):
    """安装单个技能"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 安装: {skill}")
    try:
        result = subprocess.run(
            ["npx", "clawhub", "install", skill, "--force"],
            capture_output=True,
            text=True,
            timeout=120
        )
        if "OK" in result.stdout or "installed" in result.stdout:
            print(f"  ✅ 成功")
            return True
        elif "Rate limit" in result.stderr:
            print(f"  ⏳ API限速，稍后重试")
            return None
        else:
            print(f"  ❌ 失败: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def main():
    """主函数"""
    progress = load_progress()
    
    # 找出待安装的技能
    pending = [s for s in SKILLS_TO_INSTALL 
               if s not in progress["installed"] and s not in progress["failed"]]
    
    if not pending:
        print("所有技能已安装完成！")
        return
    
    print(f"="*50)
    print(f"技能安装自动化")
    print(f"已完成: {len(progress['installed'])}/{len(SKILLS_TO_INSTALL)}")
    print(f"待安装: {len(pending)}")
    print(f"="*50)
    
    # 尝试安装一个
    skill = pending[0]
    result = install_skill(skill)
    
    if result is True:
        progress["installed"].append(skill)
        progress["last_attempt"] = datetime.now().isoformat()
    elif result is False:
        progress["failed"].append(skill)
        progress["last_attempt"] = datetime.now().isoformat()
    # result is None: 限速，不记录
    
    save_progress(progress)
    
    print(f"\n进度: {len(progress['installed'])}/{len(SKILLS_TO_INSTALL)}")

if __name__ == "__main__":
    main()
