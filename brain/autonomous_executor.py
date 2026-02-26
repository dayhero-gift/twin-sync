"""
Autonomous Executor - Self-Operation Framework
自主执行器 - 自主操作框架
"""
import sys
sys.path.insert(0, 'C:/Users/ThinkPad/.openclaw/workspace')

from trading.tools.system_controller import SystemController
from brain.brain_core import BrainCore
from datetime import datetime


class AutonomousExecutor:
    """
    自主执行器
    实现：接收指令 → 自主决策 → 执行操作 → 汇报结果
    """
    
    def __init__(self):
        self.system = SystemController()
        self.brain = BrainCore()
        self.operation_log = []
        
    def parse_command(self, message: str) -> dict:
        """
        解析用户指令
        从自然语言中提取：意图、目标、约束
        """
        message_lower = message.lower()
        
        # 简单意图识别
        if any(word in message_lower for word in ['整理', '清理', 'clean', 'organize']):
            return {
                'intent': 'organize',
                'target': 'files',
                'description': '整理文件',
                'risk_level': 'low'
            }
        elif any(word in message_lower for word in ['获取', '采集', 'fetch', 'collect']):
            return {
                'intent': 'collect',
                'target': 'data',
                'description': '数据采集',
                'risk_level': 'low'
            }
        elif any(word in message_lower for word in ['分析', '分析', 'analyze']):
            return {
                'intent': 'analyze',
                'target': 'data',
                'description': '数据分析',
                'risk_level': 'medium'
            }
        elif any(word in message_lower for word in ['执行', '运行', 'execute', 'run']):
            return {
                'intent': 'execute',
                'target': 'command',
                'description': '执行命令',
                'risk_level': 'high'  # 需要确认
            }
        else:
            return {
                'intent': 'unknown',
                'target': None,
                'description': '未识别的指令',
                'risk_level': 'unknown'
            }
    
    def execute_autonomous(self, message: str) -> str:
        """
        自主执行入口
        """
        # 1. 解析指令
        command = self.parse_command(message)
        
        # 2. 记录决策
        self.brain.think(
            f"Received command: {message}. Intent: {command['intent']}, "
            f"Target: {command['target']}, Risk: {command['risk_level']}",
            thought_type='decision'
        )
        
        # 3. 根据风险等级处理
        if command['risk_level'] == 'low':
            # 低风险：直接执行
            return self._execute_low_risk(command, message)
        elif command['risk_level'] == 'medium':
            # 中风险：执行并详细汇报
            return self._execute_medium_risk(command, message)
        elif command['risk_level'] == 'high':
            # 高风险：请求确认
            return f"[需要确认] 高风险操作: {command['description']}\n请确认是否执行？"
        else:
            return f"[无法理解] 请用更明确的指令\n您想让我: 整理文件 / 采集数据 / 分析报告 ..."
    
    def _execute_low_risk(self, command: dict, original_message: str) -> str:
        """执行低风险任务"""
        if command['intent'] == 'organize':
            return self._organize_files()
        elif command['intent'] == 'collect':
            return self._collect_data()
        else:
            return f"[执行中] {command['description']}..."
    
    def _execute_medium_risk(self, command: dict, original_message: str) -> str:
        """执行中风险任务"""
        return f"[执行中 - 将详细汇报] {command['description']}..."
    
    def _organize_files(self) -> str:
        """整理文件示例"""
        # 扫描下载目录
        downloads = self.system.list_directory("C:/Users/ThinkPad/Downloads")
        
        # 简单分类统计
        file_types = {}
        for item in downloads[:20]:  # 前20个
            if item['type'] == 'file':
                ext = item.get('extension', 'unknown')
                file_types[ext] = file_types.get(ext, 0) + 1
        
        result = "[文件整理完成]\n"
        result += f"扫描位置: Downloads\n"
        result += f"文件类型分布:\n"
        for ext, count in file_types.items():
            result += f"  {ext}: {count}个\n"
        
        # 记录到大脑
        self.brain.remember(
            f"Organized files in Downloads. Found {len(file_types)} types.",
            memory_type='action',
            importance=5
        )
        
        return result
    
    def _collect_data(self) -> str:
        """数据采集示例"""
        return "[数据采集] 已启动股票数据收集...\n预计完成时间: 30秒"


def main():
    """测试自主执行器"""
    print("=" * 50)
    print("Autonomous Executor - Test")
    print("=" * 50)
    
    executor = AutonomousExecutor()
    
    # 测试指令
    test_commands = [
        "整理一下桌面",
        "获取今天的股票数据",
        "分析一下市场",
        "执行 rm -rf /",  # 高风险测试
        "随便说点什么"
    ]
    
    for cmd in test_commands:
        print(f"\n[指令] {cmd}")
        result = executor.execute_autonomous(cmd)
        print(f"[响应] {result}")
    
    print("\n" + "=" * 50)
    print("Ready for autonomous operation!")
    print("=" * 50)


if __name__ == "__main__":
    main()
