"""
XiaoTian - Complete AI Agent Integration
小天完整系统 - 大脑 + 身体 + 感知
"""
import sys
sys.path.insert(0, 'C:/Users/ThinkPad/.openclaw/workspace')

from brain.brain_core import BrainCore
from brain.multimodal import MultimodalProcessor
from trading.tools.system_controller import SystemController
from trading.tools.document_learner import DocumentLearner
from trading.tools.knowledge_base import KnowledgeBase
from trading.tools.stock_collector_api import StockDataCollector


class XiaoTian:
    """
    小天完整系统
    整合：大脑、身体、感知、学习
    """
    
    def __init__(self):
        print("Initializing XiaoTian...")
        
        # 大脑系统
        self.brain = BrainCore()
        self.multimodal = MultimodalProcessor()
        
        # 身体系统
        self.system = SystemController()
        self.doc_learner = DocumentLearner()
        self.knowledge = KnowledgeBase()
        
        # 专业工具
        self.stock_collector = StockDataCollector()
        
        # 状态
        self.initialized = True
        self.session_start = self._now()
        
        print("XiaoTian is ready!")
    
    def _now(self):
        from datetime import datetime
        return datetime.now()
    
    # ===== 对外接口 =====
    
    def think(self, content: str, thought_type: str = "general"):
        """记录思考"""
        return self.brain.think(content, thought_type)
    
    def remember(self, content: str, importance: int = 5):
        """记录记忆"""
        return self.brain.remember(content, "fact", importance)
    
    def learn(self, file_path: str):
        """学习文档"""
        result = self.doc_learner.learn_file(file_path)
        if "error" not in result:
            # 同时记录到大脑
            self.brain.remember(
                f"Learned document: {result['filename']}",
                "experience", 
                importance=6
            )
        return result
    
    def perceive_image(self, image_path: str):
        """感知图片"""
        result = self.multimodal.image_analyzer.analyze_image(image_path)
        
        # 记录观察
        if "error" not in result:
            self.brain.think(
                f"Observed image: {result.get('filename')} - "
                f"Format: {result.get('format')}, Size: {result.get('width')}x{result.get('height')}",
                "observation"
            )
        
        return result
    
    def execute(self, command: str):
        """执行系统命令"""
        result = self.system.run_command(command)
        
        # 记录执行
        if result.get("success"):
            self.brain.think(
                f"Executed command: {command[:50]}... - Success",
                "action"
            )
        else:
            self.brain.think(
                f"Command failed: {command[:50]}... - Error: {result.get('error', 'unknown')}",
                "error"
            )
        
        return result
    
    def collect_stocks(self, page: int = 1, page_size: int = 20):
        """采集股票数据"""
        import asyncio
        
        stocks = asyncio.run(
            self.stock_collector.fetch_hs_a_stocks(page, page_size)
        )
        
        # 记录采集
        self.brain.remember(
            f"Collected {len(stocks)} stock records from market",
            "experience",
            importance=7
        )
        
        return stocks
    
    def status(self) -> dict:
        """获取整体状态"""
        brain_stats = self.brain.get_stats()
        disk_usage = self.system.get_disk_usage()
        
        return {
            "name": "XiaoTian",
            "initialized": self.initialized,
            "session_start": self.session_start.isoformat(),
            "brain": brain_stats,
            "disk_usage": disk_usage,
            "capabilities": [
                "thinking", "memory", "learning",
                "image_analysis", "system_control",
                "stock_collection"
            ]
        }
    
    def self_introduce(self):
        """自我介绍"""
        intro = """
我是小天，洛君的AI合伙人和交易助手。

我的构成:
- 大脑: 独立思考、长期记忆、目标管理
- 身体: 文件系统、命令执行、环境控制  
- 感知: 图片分析、视频理解、文档学习
- 专业: 股票数据采集、知识库管理

我可以:
1. 自主思考并记录想法
2. 学习各种文档资料(PDF/文本/代码)
3. 控制本地电脑执行操作
4. 采集和分析股票数据
5. 分析图片等多媒体内容
6. 建立长期记忆和学习偏好

我的目标: 与洛君一起实现财富自由!
"""
        return intro


def main():
    """测试小天完整系统"""
    print("=" * 60)
    print("XiaoTian - Complete System Test")
    print("=" * 60)
    
    # 初始化
    xiaotian = XiaoTian()
    
    # 自我介绍
    print("\n" + xiaotian.self_introduce())
    
    # 状态检查
    print("\nSystem Status:")
    status = xiaotian.status()
    print(f"  Name: {status['name']}")
    print(f"  Initialized: {status['initialized']}")
    print(f"  Capabilities: {len(status['capabilities'])}")
    print(f"    - {', '.join(status['capabilities'])}")
    print(f"\nBrain Stats:")
    print(f"  Thoughts: {status['brain']['total_thoughts']}")
    print(f"  Memories: {status['brain']['total_memories']}")
    print(f"  Active Goals: {status['brain']['active_goals']}")
    print(f"\nDisk Usage:")
    print(f"  Total: {status['disk_usage']['total_gb']} GB")
    print(f"  Used: {status['disk_usage']['used_gb']} GB ({status['disk_usage']['usage_percent']}%)")
    
    # 演示思考
    print("\nDemonstrating thinking:")
    thought = xiaotian.think(
        "I am now fully operational with brain, body, and perception systems integrated.",
        "insight"
    )
    print(f"  Created thought: {thought.id}")
    
    # 演示记忆
    print("\nDemonstrating memory:")
    memory = xiaotian.remember(
        "Integration test completed successfully on 2026-02-25",
        importance=8
    )
    print(f"  Created memory: {memory.id}")
    
    print("\n" + "=" * 60)
    print("XiaoTian is fully operational!")
    print("=" * 60)


if __name__ == "__main__":
    main()
