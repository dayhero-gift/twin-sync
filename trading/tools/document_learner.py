"""
文档学习工具 - PDF/文本解析
用于读取并学习各类文档资料
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Optional

class DocumentLearner:
    """文档学习器 - 支持多种格式"""
    
    def __init__(self, knowledge_base_dir: str = None):
        self.knowledge_base_dir = Path(knowledge_base_dir) if knowledge_base_dir else \
            Path(__file__).parent.parent / "knowledge"
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)
        
        # 支持的文件类型
        self.supported_types = {
            ".txt": self._parse_txt,
            ".md": self._parse_txt,
            ".py": self._parse_code,
            ".json": self._parse_txt,
            ".csv": self._parse_txt,
            ".pdf": self._parse_pdf,  # PDF支持
        }
    
    def learn_file(self, file_path: str) -> Dict:
        """
        学习单个文件
        返回: 文件信息和内容摘要
        """
        path = Path(file_path)
        
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        ext = path.suffix.lower()
        
        if ext not in self.supported_types:
            return {
                "error": f"不支持的文件类型: {ext}",
                "supported": list(self.supported_types.keys())
            }
        
        # 调用对应解析器
        parser = self.supported_types[ext]
        content = parser(path)
        
        # 生成摘要
        summary = self._generate_summary(content)
        
        # 计算页数/行数
        if ext == ".pdf":
            # PDF用页数
            page_count = self._count_pdf_pages(path)
            line_count = len(content.splitlines())
        else:
            page_count = None
            line_count = len(content.splitlines())
        
        # 保存到知识库
        knowledge_entry = {
            "filename": path.name,
            "path": str(path.absolute()),
            "type": ext,
            "size": path.stat().st_size,
            "content_preview": content[:1000] if len(content) > 1000 else content,
            "summary": summary,
            "line_count": line_count,
            "learned_at": self._get_timestamp()
        }
        
        if page_count:
            knowledge_entry["page_count"] = page_count
        
        self._save_to_knowledge_base(knowledge_entry)
        
        return knowledge_entry
    
    def _count_pdf_pages(self, path: Path) -> int:
        """统计PDF页数"""
        try:
            import pdfplumber
            with pdfplumber.open(path) as pdf:
                return len(pdf.pages)
        except:
            return 0
    
    def learn_directory(self, dir_path: str, recursive: bool = True) -> List[Dict]:
        """
        批量学习目录下所有支持的文件
        """
        path = Path(dir_path)
        results = []
        
        if not path.exists():
            return [{"error": f"目录不存在: {dir_path}"}]
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_types:
                print(f"正在学习: {file_path.name}")
                result = self.learn_file(str(file_path))
                results.append(result)
        
        return results
    
    def _parse_txt(self, path: Path) -> str:
        """解析文本文件"""
        encodings = ["utf-8", "gbk", "gb2312", "utf-16"]
        
        for encoding in encodings:
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        
        # 如果都失败，使用二进制读取
        return path.read_bytes().decode("utf-8", errors="ignore")
    
    def _parse_code(self, path: Path) -> str:
        """解析代码文件"""
        content = self._parse_txt(path)
        # 提取注释和函数定义作为学习重点
        return content
    
    def _parse_pdf(self, path: Path) -> str:
        """解析PDF文件 - 使用pdfplumber提取文本"""
        try:
            import pdfplumber
            
            text_parts = []
            with pdfplumber.open(path) as pdf:
                # 提取文档信息
                meta = pdf.metadata or {}
                
                # 遍历所有页面提取文本
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"\n--- 第{i+1}页 ---\n")
                        text_parts.append(page_text)
                    
                    # 限制只处理前20页，避免超大文档
                    if i >= 19:
                        text_parts.append("\n... (文档超过20页，已截断)")
                        break
            
            content = "\n".join(text_parts)
            
            # 如果没有提取到文本，可能是扫描版PDF
            if not content.strip():
                return "[PDF为扫描版或图片，无法提取文本内容]"
            
            return content
            
        except Exception as e:
            return f"[PDF解析错误: {str(e)}]"
    
    def _generate_summary(self, content: str, max_length: int = 500) -> str:
        """生成内容摘要"""
        # 简单摘要：取前N个字符，保留完整句子
        if len(content) <= max_length:
            return content
        
        # 尝试在句子边界截断
        truncated = content[:max_length]
        last_sentence = max(
            truncated.rfind("。"),
            truncated.rfind("."),
            truncated.rfind("\n")
        )
        
        if last_sentence > max_length * 0.5:
            return truncated[:last_sentence + 1] + "..."
        
        return truncated + "..."
    
    def _save_to_knowledge_base(self, entry: Dict):
        """保存到知识库索引"""
        import json
        
        index_file = self.knowledge_base_dir / "index.json"
        
        # 读取现有索引
        index = []
        if index_file.exists():
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    index = json.load(f)
            except:
                index = []
        
        # 更新或添加条目
        existing = False
        for i, item in enumerate(index):
            if item.get("path") == entry["path"]:
                index[i] = entry
                existing = True
                break
        
        if not existing:
            index.append(entry)
        
        # 保存索引
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def search_knowledge(self, keyword: str) -> List[Dict]:
        """搜索已学习的知识"""
        import json
        
        index_file = self.knowledge_base_dir / "index.json"
        
        if not index_file.exists():
            return []
        
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)
        
        results = []
        keyword_lower = keyword.lower()
        
        for entry in index:
            # 在文件名和内容中搜索
            if (keyword_lower in entry.get("filename", "").lower() or
                keyword_lower in entry.get("summary", "").lower() or
                keyword_lower in entry.get("content_preview", "").lower()):
                results.append(entry)
        
        return results
    
    def list_learned(self) -> List[Dict]:
        """列出所有已学习的文档"""
        import json
        
        index_file = self.knowledge_base_dir / "index.json"
        
        if not index_file.exists():
            return []
        
        with open(index_file, "r", encoding="utf-8") as f:
            return json.load(f)


def main():
    """测试文档学习功能"""
    print("=" * 50)
    print("文档学习工具测试")
    print("=" * 50)
    
    learner = DocumentLearner()
    
    # 测试：学习交易目录下的现有文件
    trading_dir = Path(__file__).parent.parent
    
    print(f"\n扫描目录: {trading_dir}")
    results = learner.learn_directory(str(trading_dir), recursive=False)
    
    print(f"\n成功学习 {len(results)} 个文件:")
    for r in results:
        if "error" not in r:
            print(f"  ✅ {r['filename']} ({r['size']} bytes, {r['line_count']} 行)")
        else:
            print(f"  ❌ {r.get('error', '未知错误')}")
    
    # 显示知识库统计
    learned = learner.list_learned()
    print(f"\n知识库统计: 共 {len(learned)} 个文档")
    
    # 测试搜索
    print("\n搜索关键词 'stock':")
    search_results = learner.search_knowledge("stock")
    for r in search_results[:3]:
        print(f"  📄 {r['filename']}")


if __name__ == "__main__":
    main()
