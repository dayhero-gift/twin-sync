"""
Brain Core - Independent Thinking System
小天的大脑核心 - 思考、记忆、推理体系
"""
import json
import uuid
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from collections import defaultdict


class Thought:
    """单个思考单元"""
    def __init__(self, content: str, thought_type: str = "general", 
                 context: Dict = None, confidence: float = 1.0):
        self.id = f"thought_{uuid.uuid4().hex[:8]}"
        self.content = content
        self.type = thought_type  # general, analysis, decision, question, insight
        self.context = context or {}
        self.confidence = confidence  # 0.0 - 1.0
        self.created_at = datetime.now().isoformat()
        self.related_thoughts = []
        
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "type": self.type,
            "context": self.context,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "related_thoughts": self.related_thoughts
        }


class Memory:
    """长期记忆单元"""
    def __init__(self, content: str, memory_type: str = "fact",
                 importance: int = 5, source: str = None):
        self.id = f"memory_{uuid.uuid4().hex[:8]}"
        self.content = content
        self.type = memory_type  # fact, experience, lesson, goal, preference
        self.importance = importance  # 1-10
        self.source = source
        self.created_at = datetime.now().isoformat()
        self.access_count = 0
        self.last_accessed = None
        
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "type": self.type,
            "importance": self.importance,
            "source": self.source,
            "created_at": self.created_at,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed
        }


class BrainCore:
    """
    小天的大脑核心
    功能：
    1. 独立思考和记录
    2. 长期记忆管理
    3. 推理和关联
    4. 决策支持
    """
    
    def __init__(self, brain_dir: str = None):
        self.brain_dir = Path(brain_dir) if brain_dir else \
            Path("C:/Users/ThinkPad/.openclaw/workspace/brain")
        self.brain_dir.mkdir(parents=True, exist_ok=True)
        
        # 存储文件
        self.thoughts_file = self.brain_dir / "thoughts.jsonl"
        self.memories_file = self.brain_dir / "memories.jsonl"
        self.goals_file = self.brain_dir / "goals.json"
        self.preferences_file = self.brain_dir / "preferences.json"
        
        # 内存缓存
        self.thoughts: List[Thought] = []
        self.memories: List[Memory] = []
        self.goals: Dict = {}
        self.preferences: Dict = {}
        
        self._load_all()
    
    def _load_all(self):
        """加载所有数据"""
        self.thoughts = self._load_thoughts()
        self.memories = self._load_memories()
        self.goals = self._load_json(self.goals_file, {})
        self.preferences = self._load_json(self.preferences_file, {})
    
    def _load_thoughts(self) -> List[Thought]:
        """加载思考记录"""
        thoughts = []
        if self.thoughts_file.exists():
            with open(self.thoughts_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            t = Thought(data["content"], data["type"])
                            t.id = data["id"]
                            t.context = data.get("context", {})
                            t.confidence = data.get("confidence", 1.0)
                            t.created_at = data["created_at"]
                            t.related_thoughts = data.get("related_thoughts", [])
                            thoughts.append(t)
                        except:
                            pass
        return thoughts
    
    def _load_memories(self) -> List[Memory]:
        """加载记忆"""
        memories = []
        if self.memories_file.exists():
            with open(self.memories_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            m = Memory(data["content"], data["type"])
                            m.id = data["id"]
                            m.importance = data.get("importance", 5)
                            m.source = data.get("source")
                            m.created_at = data["created_at"]
                            m.access_count = data.get("access_count", 0)
                            m.last_accessed = data.get("last_accessed")
                            memories.append(m)
                        except:
                            pass
        return memories
    
    def _load_json(self, path: Path, default):
        """加载JSON文件"""
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_jsonl(self, path: Path, items: List):
        """保存JSONL文件"""
        with open(path, 'w', encoding='utf-8') as f:
            for item in items:
                f.write(json.dumps(item.to_dict(), ensure_ascii=False) + '\n')
    
    def _save_json(self, path: Path, data: Dict):
        """保存JSON文件"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ===== 思考功能 =====
    
    def think(self, content: str, thought_type: str = "general", 
              context: Dict = None, confidence: float = 1.0) -> Thought:
        """
        记录一个思考
        """
        thought = Thought(content, thought_type, context, confidence)
        self.thoughts.append(thought)
        self._save_jsonl(self.thoughts_file, self.thoughts)
        return thought
    
    def get_recent_thoughts(self, n: int = 10, thought_type: str = None) -> List[Thought]:
        """获取最近的思考"""
        thoughts = self.thoughts
        if thought_type:
            thoughts = [t for t in thoughts if t.type == thought_type]
        return thoughts[-n:] if len(thoughts) > n else thoughts
    
    def link_thoughts(self, thought1_id: str, thought2_id: str):
        """关联两个思考"""
        for t in self.thoughts:
            if t.id == thought1_id and thought2_id not in t.related_thoughts:
                t.related_thoughts.append(thought2_id)
            if t.id == thought2_id and thought1_id not in t.related_thoughts:
                t.related_thoughts.append(thought1_id)
        self._save_jsonl(self.thoughts_file, self.thoughts)
    
    # ===== 记忆功能 =====
    
    def remember(self, content: str, memory_type: str = "fact",
                 importance: int = 5, source: str = None) -> Memory:
        """
        记录长期记忆
        """
        memory = Memory(content, memory_type, importance, source)
        self.memories.append(memory)
        self._save_jsonl(self.memories_file, self.memories)
        return memory
    
    def recall(self, keyword: str, memory_type: str = None) -> List[Memory]:
        """根据关键词回忆"""
        results = []
        keyword_lower = keyword.lower()
        
        for m in self.memories:
            if memory_type and m.type != memory_type:
                continue
            if keyword_lower in m.content.lower():
                m.access_count += 1
                m.last_accessed = datetime.now().isoformat()
                results.append(m)
        
        # 按重要性和访问频率排序
        results.sort(key=lambda x: (x.importance, x.access_count), reverse=True)
        return results
    
    def get_important_memories(self, min_importance: int = 7) -> List[Memory]:
        """获取重要记忆"""
        return [m for m in self.memories if m.importance >= min_importance]
    
    # ===== 目标管理 =====
    
    def set_goal(self, goal_id: str, description: str, target_date: str = None,
                 priority: int = 5, metrics: List[str] = None):
        """设置目标"""
        self.goals[goal_id] = {
            "description": description,
            "target_date": target_date,
            "priority": priority,
            "metrics": metrics or [],
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "progress": 0
        }
        self._save_json(self.goals_file, self.goals)
    
    def update_goal_progress(self, goal_id: str, progress: int):
        """更新目标进度"""
        if goal_id in self.goals:
            self.goals[goal_id]["progress"] = progress
            self._save_json(self.goals_file, self.goals)
    
    def get_active_goals(self) -> Dict:
        """获取活跃目标"""
        return {k: v for k, v in self.goals.items() if v.get("status") == "active"}
    
    # ===== 偏好学习 =====
    
    def learn_preference(self, category: str, key: str, value: Any):
        """学习用户偏好"""
        if category not in self.preferences:
            self.preferences[category] = {}
        self.preferences[category][key] = {
            "value": value,
            "learned_at": datetime.now().isoformat()
        }
        self._save_json(self.preferences_file, self.preferences)
    
    def get_preference(self, category: str, key: str, default=None):
        """获取用户偏好"""
        return self.preferences.get(category, {}).get(key, {}).get("value", default)
    
    # ===== 推理功能 =====
    
    def analyze_situation(self, context: Dict) -> List[Thought]:
        """基于记忆和当前情境进行分析"""
        relevant_memories = []
        
        # 根据上下文关键词召回相关记忆
        for keyword in context.get("keywords", []):
            relevant_memories.extend(self.recall(keyword))
        
        # 生成分析思考
        thoughts = []
        if relevant_memories:
            memory_contents = [m.content for m in relevant_memories[:3]]
            analysis = f"Based on past memories: {', '.join(memory_contents)}"
            thoughts.append(self.think(analysis, "analysis", context, 0.8))
        
        return thoughts
    
    def get_stats(self) -> Dict:
        """获取大脑统计"""
        return {
            "total_thoughts": len(self.thoughts),
            "total_memories": len(self.memories),
            "total_goals": len(self.goals),
            "active_goals": len(self.get_active_goals()),
            "thought_types": defaultdict(int),
            "memory_types": defaultdict(int)
        }


def main():
    """测试大脑核心"""
    print("=" * 50)
    print("Brain Core Test - Independent Thinking System")
    print("=" * 50)
    
    brain = BrainCore()
    
    # 记录思考
    print("\nRecording thoughts...")
    t1 = brain.think("I need to learn more about stock market patterns", 
                     "insight", {"topic": "trading"})
    t2 = brain.think("The best time to analyze market data is after market close",
                     "analysis", {"topic": "trading"})
    print(f"Created thought: {t1.id}")
    print(f"Created thought: {t2.id}")
    
    # 关联思考
    brain.link_thoughts(t1.id, t2.id)
    print("Linked thoughts")
    
    # 记录记忆
    print("\nRecording memories...")
    brain.remember("Luojun wants to achieve financial freedom through stock trading",
                   "goal", importance=10, source="USER")
    brain.remember("Use Playwright with Edge for browser automation",
                   "lesson", importance=8, source="EXPERIENCE")
    print("Created 2 memories")
    
    # 设置目标
    print("\nSetting goals...")
    brain.set_goal("wealth_freedom", 
                   "Achieve financial freedom with Luojun",
                   priority=10)
    print("Created goal: wealth_freedom")
    
    # 学习偏好
    print("\nLearning preferences...")
    brain.learn_preference("communication", "style", "direct")
    brain.learn_preference("work", "hours", "08:00-24:00")
    print("Learned preferences")
    
    # 回忆
    print("\nRecalling memories about 'stock':")
    memories = brain.recall("stock")
    for m in memories[:3]:
        print(f"  - {m.content[:50]}...")
    
    # 统计
    print("\nBrain Stats:")
    stats = brain.get_stats()
    print(f"  Total thoughts: {stats['total_thoughts']}")
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Active goals: {stats['active_goals']}")
    
    print("\nBrain Core is ready!")


if __name__ == "__main__":
    main()
