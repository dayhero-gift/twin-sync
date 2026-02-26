"""
Task Manager - Daily Task and Goal Management
任务管理器 - 每日任务和目标管理
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class TaskManager:
    """任务管理器"""
    
    def __init__(self, task_dir: str = None):
        self.task_dir = Path(task_dir) if task_dir else \
            Path("C:/Users/ThinkPad/.openclaw/workspace/tasks")
        self.task_dir.mkdir(parents=True, exist_ok=True)
        
        self.tasks_file = self.task_dir / "tasks.json"
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict]:
        """加载任务列表"""
        if self.tasks_file.exists():
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save_tasks(self):
        """保存任务列表"""
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
    
    def add_task(self, title: str, description: str = None, 
                 priority: int = 3, due_date: str = None,
                 category: str = "general") -> Dict:
        """添加任务"""
        task = {
            "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": title,
            "description": description,
            "priority": priority,  # 1-5, 5 is highest
            "category": category,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "due_date": due_date,
            "completed_at": None
        }
        
        self.tasks.append(task)
        self._save_tasks()
        return task
    
    def complete_task(self, task_id: str) -> bool:
        """完成任务"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                self._save_tasks()
                return True
        return False
    
    def get_pending_tasks(self, category: str = None) -> List[Dict]:
        """获取待办任务"""
        tasks = [t for t in self.tasks if t["status"] == "pending"]
        if category:
            tasks = [t for t in tasks if t["category"] == category]
        # 按优先级排序
        return sorted(tasks, key=lambda x: x["priority"], reverse=True)
    
    def get_todays_tasks(self) -> List[Dict]:
        """获取今日任务"""
        today = datetime.now().strftime("%Y-%m-%d")
        return [t for t in self.tasks 
                if t["status"] == "pending" and 
                (t.get("due_date") == today or t.get("due_date") is None)]
    
    def get_stats(self) -> Dict:
        """获取任务统计"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "completed"])
        pending = len([t for t in self.tasks if t["status"] == "pending"])
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0
        }
    
    def generate_daily_plan(self) -> str:
        """生成每日计划"""
        plan = f"""# Daily Plan - {datetime.now().strftime('%Y-%m-%d')}

## Task Statistics
- Total: {self.get_stats()['total']}
- Completed: {self.get_stats()['completed']}
- Pending: {self.get_stats()['pending']}
- Completion Rate: {self.get_stats()['completion_rate']}%

## Today's Tasks
"""
        
        todays_tasks = self.get_todays_tasks()
        if todays_tasks:
            for i, task in enumerate(todays_tasks, 1):
                priority = "[!]" if task["priority"] >= 4 else "[ ]"
                plan += f"{i}. {priority} {task['title']}\n"
                if task.get("description"):
                    plan += f"   {task['description']}\n"
        else:
            plan += "No tasks scheduled for today.\n"
        
        plan += "\n## High Priority Pending\n"
        high_priority = [t for t in self.get_pending_tasks() if t["priority"] >= 4][:5]
        for task in high_priority:
            plan += f"- [P{task['priority']}] {task['title']}\n"
        
        return plan


def create_tomorrow_tasks():
    """创建明天的任务列表"""
    tm = TaskManager()
    
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    tasks = [
        ("Configure Discord/Feishu with twin", "Setup communication channel", 5, "sync"),
        ("Test twin messaging", "Send test messages to verify bidirectional communication", 5, "sync"),
        ("First GitHub code sync", "Push local code, pull cloud code", 4, "sync"),
        ("Collect morning stock data", "Get HS A-share data for analysis", 3, "trading"),
        ("Review twin's MEMORY.md", "Read and merge knowledge from cloud twin", 4, "learning"),
    ]
    
    for title, desc, priority, category in tasks:
        tm.add_task(title, desc, priority, tomorrow, category)
        print(f"Added: {title}")
    
    return tm


def main():
    """主程序"""
    print("=" * 50)
    print("Task Manager - Daily Planning")
    print("=" * 50)
    
    # 创建明天的任务
    print("\nCreating tasks for tomorrow...")
    tm = create_tomorrow_tasks()
    
    # 显示统计
    print("\nTask Statistics:")
    stats = tm.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 生成并保存每日计划
    plan = tm.generate_daily_plan()
    plan_file = Path("C:/Users/ThinkPad/.openclaw/workspace/tasks/tomorrow_plan.md")
    with open(plan_file, "w", encoding="utf-8") as f:
        f.write(plan)
    
    print(f"\nPlan saved to: {plan_file}")
    print("\nTomorrow's Tasks:")
    for task in tm.get_todays_tasks():
        print(f"  [P{task['priority']}] {task['title']}")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
