"""
Auto Learning - Autonomous Learning Script
自主学习脚本 - 在空闲时自动学习代码和文档
"""
import sys
sys.path.insert(0, 'C:/Users/ThinkPad/.openclaw/workspace')

from trading.tools.document_learner import DocumentLearner
from trading.tools.knowledge_base import KnowledgeBase
from pathlib import Path
from datetime import datetime


def auto_learn_workspace():
    """自动学习工作区内的所有代码文件"""
    print("=" * 50)
    print("Auto Learning - XiaoTian Self-Education")
    print("=" * 50)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    learner = DocumentLearner()
    kb = KnowledgeBase()
    
    workspace = Path("C:/Users/ThinkPad/.openclaw/workspace")
    
    # 定义学习路径
    learn_paths = [
        workspace / "trading" / "tools",
        workspace / "brain",
        workspace / "sync",
    ]
    
    total_learned = 0
    
    for path in learn_paths:
        if not path.exists():
            continue
        
        print(f"Scanning: {path}")
        
        # 查找所有支持的文件
        for file_path in path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in learner.supported_types:
                print(f"  Learning: {file_path.name}")
                
                # 学习文件
                result = learner.learn_file(str(file_path))
                
                if "error" not in result:
                    # 添加到知识库，带标签
                    tags = []
                    if "trading" in str(file_path):
                        tags.append("trading")
                    if "brain" in str(file_path):
                        tags.append("brain")
                    if "sync" in str(file_path):
                        tags.append("sync")
                    
                    category = "code"
                    if file_path.suffix == ".md":
                        category = "documentation"
                    elif file_path.suffix == ".pdf":
                        category = "document"
                    
                    kb.add_document(result, tags=tags, category=category)
                    total_learned += 1
                else:
                    print(f"    Error: {result['error']}")
    
    print()
    print("=" * 50)
    print(f"Learning Complete!")
    print(f"Total files learned: {total_learned}")
    
    # 显示知识库统计
    stats = kb.get_stats()
    print(f"Knowledge base: {stats['total_documents']} documents")
    print(f"Categories: {', '.join(stats['categories'])}")
    print(f"Tags: {', '.join(stats['tags'][:10])}")
    print("=" * 50)
    
    return total_learned


def generate_learning_summary():
    """生成学习摘要"""
    kb = KnowledgeBase()
    
    docs = kb.list_documents(limit=10)
    
    summary = f"""# Auto Learning Summary

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Knowledge Base Status
- Total Documents: {kb.get_stats()['total_documents']}
- Categories: {len(kb.get_stats()['categories'])}
- Tags: {len(kb.get_stats()['tags'])}

## Recently Learned
"""
    
    for doc in docs:
        summary += f"\n### {doc['filename']}\n"
        summary += f"- Type: {doc['type']}\n"
        summary += f"- Size: {doc['size']} bytes\n"
        summary += f"- Summary: {doc.get('summary', 'N/A')[:100]}...\n"
    
    # 保存摘要
    summary_path = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/learning_summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    
    return summary_path


if __name__ == "__main__":
    # 执行自动学习
    count = auto_learn_workspace()
    
    # 生成摘要
    if count > 0:
        summary_file = generate_learning_summary()
        print(f"\nSummary saved to: {summary_file}")
