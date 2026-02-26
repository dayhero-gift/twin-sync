"""
Knowledge Base Manager - Advanced knowledge management
Vector search, tags, categories, cross-reference
"""
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime
from collections import defaultdict


class KnowledgeBase:
    """Knowledge base with advanced features"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else \
            Path("C:/Users/ThinkPad/.openclaw/workspace/trading/knowledge")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.base_dir / "index.json"
        self.tags_file = self.base_dir / "tags.json"
        self.categories_file = self.base_dir / "categories.json"
        
        # Load existing data
        self.index = self._load_json(self.index_file, [])
        self.tags = self._load_json(self.tags_file, {})
        self.categories = self._load_json(self.categories_file, {})
    
    def _load_json(self, path: Path, default):
        """Load JSON file or return default"""
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def _save_json(self, path: Path, data):
        """Save data to JSON file"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_document(self, doc_info: Dict, tags: List[str] = None, category: str = None):
        """Add document to knowledge base"""
        doc_id = doc_info.get("path", str(datetime.now().timestamp()))
        
        # Update or add to index
        existing = False
        for i, doc in enumerate(self.index):
            if doc.get("path") == doc_id:
                self.index[i] = {**doc, **doc_info, "updated_at": self._now()}
                existing = True
                break
        
        if not existing:
            doc_info["added_at"] = self._now()
            doc_info["updated_at"] = self._now()
            self.index.append(doc_info)
        
        # Add tags
        if tags:
            for tag in tags:
                if tag not in self.tags:
                    self.tags[tag] = []
                if doc_id not in self.tags[tag]:
                    self.tags[tag].append(doc_id)
        
        # Add category
        if category:
            if category not in self.categories:
                self.categories[category] = []
            if doc_id not in self.categories[category]:
                self.categories[category].append(doc_id)
        
        self._save_all()
        return doc_info
    
    def search(self, keyword: str, search_content: bool = True) -> List[Dict]:
        """Search documents by keyword"""
        results = []
        keyword_lower = keyword.lower()
        
        for doc in self.index:
            score = 0
            
            # Search in filename
            if keyword_lower in doc.get("filename", "").lower():
                score += 10
            
            # Search in summary
            if keyword_lower in doc.get("summary", "").lower():
                score += 5
            
            # Search in content preview
            if search_content and keyword_lower in doc.get("content_preview", "").lower():
                score += 3
            
            if score > 0:
                results.append({**doc, "search_score": score})
        
        # Sort by score
        return sorted(results, key=lambda x: x["search_score"], reverse=True)
    
    def search_by_tag(self, tag: str) -> List[Dict]:
        """Search by tag"""
        doc_paths = self.tags.get(tag, [])
        return [doc for doc in self.index if doc.get("path") in doc_paths]
    
    def search_by_category(self, category: str) -> List[Dict]:
        """Search by category"""
        doc_paths = self.categories.get(category, [])
        return [doc for doc in self.index if doc.get("path") in doc_paths]
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        total_docs = len(self.index)
        total_tags = len(self.tags)
        total_categories = len(self.categories)
        
        # File type distribution
        type_dist = defaultdict(int)
        for doc in self.index:
            ext = doc.get("type", "unknown")
            type_dist[ext] += 1
        
        # Size distribution
        total_size = sum(doc.get("size", 0) for doc in self.index)
        
        return {
            "total_documents": total_docs,
            "total_tags": total_tags,
            "total_categories": total_categories,
            "total_size_bytes": total_size,
            "type_distribution": dict(type_dist),
            "tags": list(self.tags.keys()),
            "categories": list(self.categories.keys())
        }
    
    def get_all_tags(self) -> List[str]:
        """Get all tags"""
        return sorted(self.tags.keys())
    
    def get_all_categories(self) -> List[str]:
        """Get all categories"""
        return sorted(self.categories.keys())
    
    def list_documents(self, limit: int = None) -> List[Dict]:
        """List all documents"""
        docs = sorted(self.index, key=lambda x: x.get("updated_at", ""), reverse=True)
        return docs[:limit] if limit else docs
    
    def delete_document(self, path: str) -> bool:
        """Delete document from knowledge base"""
        # Remove from index
        self.index = [doc for doc in self.index if doc.get("path") != path]
        
        # Remove from tags
        for tag in self.tags:
            self.tags[tag] = [p for p in self.tags[tag] if p != path]
        
        # Remove from categories
        for cat in self.categories:
            self.categories[cat] = [p for p in self.categories[cat] if p != path]
        
        self._save_all()
        return True
    
    def _save_all(self):
        """Save all data"""
        self._save_json(self.index_file, self.index)
        self._save_json(self.tags_file, self.tags)
        self._save_json(self.categories_file, self.categories)
    
    def _now(self) -> str:
        """Get current timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """Test knowledge base"""
    print("=" * 50)
    print("Knowledge Base Test")
    print("=" * 50)
    
    kb = KnowledgeBase()
    
    # Add test document
    test_doc = {
        "filename": "test_stock_strategy.py",
        "path": "C:/test/test_stock_strategy.py",
        "type": ".py",
        "size": 1024,
        "summary": "Stock trading strategy implementation",
        "content_preview": "class StockStrategy:\n    def __init__(self):\n        pass"
    }
    
    kb.add_document(test_doc, tags=["strategy", "python", "trading"], category="code")
    print("\nAdded test document")
    
    # Search
    print("\nSearch 'stock':")
    results = kb.search("stock")
    for r in results:
        print(f"  {r['filename']} (score: {r['search_score']})")
    
    # Stats
    print("\nKnowledge Base Stats:")
    stats = kb.get_stats()
    print(f"  Total documents: {stats['total_documents']}")
    print(f"  Total tags: {stats['total_tags']}")
    print(f"  Tags: {', '.join(stats['tags'])}")
    print(f"  Categories: {', '.join(stats['categories'])}")


if __name__ == "__main__":
    main()
