import sys
sys.path.insert(0, 'C:/Users/ThinkPad/.openclaw/workspace')

from trading.tools.document_learner import DocumentLearner

learner = DocumentLearner()

# 查看支持的格式
print('支持格式:', list(learner.supported_types.keys()))

# 测试学习stock_collector_api.py
result = learner.learn_file('C:/Users/ThinkPad/.openclaw/workspace/trading/tools/stock_collector_api.py')
print(f"\n已学习: {result['filename']}")
print(f"类型: {result['type']}")
print(f"大小: {result['size']} bytes")
print(f"行数: {result.get('line_count', 0)}")

# 查看知识库
learned = learner.list_learned()
print(f"\n知识库共 {len(learned)} 个文档")
for doc in learned:
    print(f"  - {doc['filename']} ({doc['type']})")
