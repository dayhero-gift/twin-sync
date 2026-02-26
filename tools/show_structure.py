"""
Generate Directory Structure - Workspace Overview
生成目录结构概览
"""
from pathlib import Path


def generate_tree(path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
    """生成树形目录结构"""
    if current_depth > max_depth:
        return []
    
    lines = []
    items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "
        
        lines.append(f"{prefix}{connector}{item.name}")
        
        if item.is_dir():
            extension = "    " if is_last else "│   "
            lines.extend(generate_tree(item, prefix + extension, max_depth, current_depth + 1))
    
    return lines


def main():
    workspace = Path("C:/Users/ThinkPad/.openclaw/workspace")
    
    print("=" * 60)
    print("XiaoTian Workspace Structure")
    print("=" * 60)
    print(f"\nRoot: {workspace}\n")
    
    # 核心目录
    core_dirs = [
        ("brain/", "大脑核心系统"),
        ("trading/tools/", "交易和数据工具"),
        ("trading/data/", "股票数据存储"),
        ("trading/knowledge/", "知识库"),
        ("sync/", "双生AI同步系统"),
        ("tasks/", "任务管理"),
        ("reports/", "日报/报告"),
        ("memory/", "每日记忆"),
    ]
    
    print("Core Directories:")
    for dir_path, desc in core_dirs:
        full_path = workspace / dir_path
        if full_path.exists():
            file_count = len(list(full_path.rglob("*")))
            print(f"  [DIR] {dir_path:<20} {desc:<20} ({file_count} items)")
    
    # 关键文件
    print("\nKey Files:")
    key_files = [
        ("xiaotian.py", "小天完整系统集成"),
        ("MEMORY.md", "长期记忆"),
        ("SOUL.md", "灵魂定义"),
        ("USER.md", "洛君档案"),
    ]
    
    for filename, desc in key_files:
        filepath = workspace / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  [FILE] {filename:<25} {desc:<25} ({size} bytes)")
    
    # 工具统计
    print("\nTools Summary:")
    tools_dirs = [
        ("trading/tools", "Trading"),
        ("brain", "Brain"),
        ("sync", "Sync"),
        ("tasks", "Task"),
    ]
    
    total_tools = 0
    for dir_path, category in tools_dirs:
        path = workspace / dir_path
        if path.exists():
            py_files = list(path.glob("*.py"))
            md_files = list(path.glob("*.md"))
            count = len(py_files) + len(md_files)
            total_tools += count
            print(f"  {category:<15} {count} files")
    
    print(f"\n  Total: {total_tools} tools/modules")
    
    print("\n" + "=" * 60)
    print("Day 1: 15 tools created, 6 core tasks completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
