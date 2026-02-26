#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
"""
定时任务调度系统
"""

import schedule
import time
import subprocess
from datetime import datetime

def run_task(name, cmd, cwd=None):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 执行任务: {name}")
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300)
        print(f"  退出码: {result.returncode}")
    except Exception as e:
        print(f"  错误: {e}")

def job_hourly():
    print(f"\n{'='*50}")
    print(f"每小时任务 - {datetime.now()}")
    run_task("技能安装", ["python", "auto_install_skills.py"])

def job_daily_morning():
    print(f"\n{'='*50}")
    print(f"晨间任务 - {datetime.now()}")
    run_task("每日进化", ["python", "daily_evolution.py"], "C:/Users/ThinkPad/trading/tools")
    run_task("自主学习", ["python", "self_learning.py"], "C:/Users/ThinkPad/trading/tools")

print("定时任务系统")
schedule.every().hour.do(job_hourly)
schedule.every().day.at("08:00").do(job_daily_morning)

job_hourly()

while True:
    schedule.run_pending()
    time.sleep(60)
