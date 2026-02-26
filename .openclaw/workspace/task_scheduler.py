#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度系统
自动执行日常维护和学习任务
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import schedule
import time
import subprocess
from datetime import datetime
from pathlib import Path

# 任务列表
TASKS = {
    "hourly": [
        {
            "name": "技能安装尝试",
            "cmd": ["python", "auto_install_skills.py"],
            "cwd": "C:/Users/ThinkPad/.openclaw/workspace"
        }
    ],
    "daily_8am": [
        {
            "name": "每日进化任务",
            "cmd": ["python", "daily_evolution.py"],
            "cwd": "C:/Users/ThinkPad/trading/tools"
        },
        {
            "name": "自主学习",
            "cmd": ["python", "self_learning.py"],
            "cwd": "C:/Users/ThinkPad/trading/tools"
        }
    ],
    "daily_9pm": [
        {
            "name": "学习总结",
            "cmd": ["echo", "今日学习总结"],
            "cwd": "C:/Users/ThinkPad/.openclaw/workspace"
        }
    ]
}

def run_task(task):
    """执行单个任务"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 执行任务: {task['name']}")
    try:
        result = subprocess.run(
            task['cmd'],
            cwd=task.get('cwd'),
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"  ✅ 成功")
            if result.stdout:
                print(f"  输出: {result.stdout[:200]}")
        else:
            print(f"  ⚠️ 退出码: {result.returncode}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

def job_hourly():
    """每小时任务"""
    print(f"\n{'='*50}")
    print(f"每小时任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    for task in TASKS['hourly']:
        run_task(task)

def job_daily_8am():
    """每日8点任务"""
    print(f"\n{'='*50}")
    print(f"每日晨间任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    for task in TASKS['daily_8am']:
        run_task(task)

def job_daily_9pm():
    """每日21点任务"""
    print(f"\n{'='*50}")
    print(f"每日晚间任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    for task in TASKS['daily_9pm']:
        run_task(task)

def main():
    """主函数"""
    print(f"{'='*50}")
    print("定时任务调度系统启动")
    print(f"{'='*50}")
    print("\n已注册任务:")
    print("  每小时: 技能安装尝试")
    print("  每日08:00: 每日进化 + 自主学习")
    print("  每日21:00: 学习总结")
    print("\n按 Ctrl+C 停止\n")
    
    # 注册任务
    schedule.every().hour.do(job_hourly)
    schedule.every().day.at("08:00").do(job_daily_8am)
    schedule.every().day.at("21:00").do(job_daily_9pm)
    
    # 运行一次测试
    job_hourly()
    
    # 主循环
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main()
