"""
Multimodal Understanding - Image and Video Analysis
多模态理解模块 - 图片、视频、音频等非文本内容处理
"""
import os
import base64
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime


class ImageAnalyzer:
    """图片分析器"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    def analyze_image(self, image_path: str) -> Dict:
        """
        分析图片内容
        返回: 图片描述、文字识别、图表检测等
        """
        path = Path(image_path)
        
        if not path.exists():
            return {"error": f"Image not found: {image_path}"}
        
        if path.suffix.lower() not in self.supported_formats:
            return {"error": f"Unsupported format: {path.suffix}"}
        
        # 获取图片基本信息
        try:
            from PIL import Image
            with Image.open(path) as img:
                width, height = img.size
                format_type = img.format
                mode = img.mode
                
                analysis = {
                    "path": str(path),
                    "filename": path.name,
                    "format": format_type,
                    "mode": mode,
                    "width": width,
                    "height": height,
                    "aspect_ratio": round(width / height, 2),
                    "size_bytes": path.stat().st_size,
                    "is_chart": self._detect_chart(img),
                    "dominant_colors": self._extract_colors(img),
                    "has_text": self._detect_text_region(img),
                    "timestamp": datetime.now().isoformat()
                }
                
                return analysis
                
        except ImportError:
            # 如果没有PIL，返回基本信息
            return {
                "path": str(path),
                "filename": path.name,
                "size_bytes": path.stat().st_size,
                "error": "PIL not installed, basic info only"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _detect_chart(self, img) -> bool:
        """检测是否为图表"""
        # 简单启发式：检查是否包含大量连续线条
        try:
            from PIL import ImageStat
            stat = ImageStat.Stat(img)
            # 如果颜色变化较大，可能是图表
            return len(stat.count) > 100 if hasattr(stat, 'count') else False
        except:
            return False
    
    def _extract_colors(self, img, n_colors: int = 5) -> List[str]:
        """提取主导颜色"""
        try:
            # 缩小图片以加速处理
            small = img.resize((50, 50))
            pixels = list(small.getdata())
            
            # 简单的颜色统计
            color_counts = {}
            for pixel in pixels[:1000]:  # 采样前1000个像素
                if isinstance(pixel, tuple):
                    # 量化颜色到粗粒度
                    quantized = tuple((c // 32) * 32 for c in pixel[:3])
                    color_counts[quantized] = color_counts.get(quantized, 0) + 1
            
            # 获取最常见的颜色
            top_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:n_colors]
            return [f"#{r:02x}{g:02x}{b:02x}" for (r, g, b), count in top_colors]
        except:
            return []
    
    def _detect_text_region(self, img) -> bool:
        """检测图片中是否包含文字区域"""
        # 简化检测：检查是否有大量灰度/黑白像素
        try:
            gray = img.convert('L')
            stat = ImageStat.Stat(gray)
            std = stat.stddev[0] if stat.stddev else 0
            # 高对比度区域可能包含文字
            return std > 50
        except:
            return False
    
    def extract_text(self, image_path: str) -> Dict:
        """
        从图片中提取文字 (OCR)
        """
        try:
            import pytesseract
            from PIL import Image
            
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            
            return {
                "success": True,
                "text": text,
                "text_length": len(text),
                "has_chinese": any('\u4e00' <= char <= '\u9fff' for char in text)
            }
        except ImportError:
            return {"error": "OCR not available. Install pytesseract and tesseract-ocr"}
        except Exception as e:
            return {"error": str(e)}
    
    def compare_images(self, image1: str, image2: str) -> Dict:
        """比较两张图片的相似度"""
        try:
            from PIL import Image
            
            img1 = Image.open(image1).convert('RGB')
            img2 = Image.open(image2).convert('RGB')
            
            # 统一尺寸
            img1 = img1.resize((100, 100))
            img2 = img2.resize((100, 100))
            
            # 计算像素差异
            pixels1 = list(img1.getdata())
            pixels2 = list(img2.getdata())
            
            diff = sum(abs(p1 - p2) for px1, px2 in zip(pixels1, pixels2) 
                      for p1, p2 in zip(px1, px2))
            max_diff = 255 * 3 * 100 * 100
            similarity = 1 - (diff / max_diff)
            
            return {
                "similarity": round(similarity, 4),
                "is_similar": similarity > 0.95,
                "image1": image1,
                "image2": image2
            }
        except Exception as e:
            return {"error": str(e)}


class VideoAnalyzer:
    """视频分析器"""
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    
    def analyze_video(self, video_path: str) -> Dict:
        """分析视频基本信息"""
        path = Path(video_path)
        
        if not path.exists():
            return {"error": f"Video not found: {video_path}"}
        
        if path.suffix.lower() not in self.supported_formats:
            return {"error": f"Unsupported format: {path.suffix}"}
        
        try:
            import cv2
            cap = cv2.VideoCapture(str(path))
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                "path": str(path),
                "filename": path.name,
                "format": path.suffix.lower(),
                "width": width,
                "height": height,
                "fps": round(fps, 2),
                "frame_count": frame_count,
                "duration_seconds": round(duration, 2),
                "duration_formatted": self._format_duration(duration),
                "size_bytes": path.stat().st_size,
                "bitrate_mbps": round((path.stat().st_size * 8) / (duration * 1024 * 1024), 2) if duration > 0 else 0
            }
            
        except ImportError:
            return {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "error": "OpenCV not installed, basic info only"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _format_duration(self, seconds: float) -> str:
        """格式化时长"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"
    
    def extract_frames(self, video_path: str, output_dir: str, 
                       interval_seconds: int = 5) -> List[str]:
        """从视频中提取关键帧"""
        try:
            import cv2
            
            path = Path(video_path)
            output = Path(output_dir)
            output.mkdir(parents=True, exist_ok=True)
            
            cap = cv2.VideoCapture(str(path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * interval_seconds)
            
            frames = []
            frame_count = 0
            saved_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    frame_path = output / f"frame_{saved_count:04d}.jpg"
                    cv2.imwrite(str(frame_path), frame)
                    frames.append(str(frame_path))
                    saved_count += 1
                
                frame_count += 1
            
            cap.release()
            return frames
            
        except ImportError:
            return []
        except Exception as e:
            return [{"error": str(e)}]


class MultimodalProcessor:
    """多模态处理器 - 统一接口"""
    
    def __init__(self):
        self.image_analyzer = ImageAnalyzer()
        self.video_analyzer = VideoAnalyzer()
    
    def process(self, file_path: str) -> Dict:
        """自动识别并处理文件"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext in self.image_analyzer.supported_formats:
            return {
                "type": "image",
                "result": self.image_analyzer.analyze_image(file_path)
            }
        elif ext in self.video_analyzer.supported_formats:
            return {
                "type": "video",
                "result": self.video_analyzer.analyze_video(file_path)
            }
        else:
            return {"error": f"Unsupported file type: {ext}"}
    
    def batch_process(self, directory: str, recursive: bool = False) -> List[Dict]:
        """批量处理目录中的多媒体文件"""
        path = Path(directory)
        results = []
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in path.glob(pattern):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in self.image_analyzer.supported_formats or \
                   ext in self.video_analyzer.supported_formats:
                    result = self.process(str(file_path))
                    results.append(result)
        
        return results


def main():
    """测试多模态理解"""
    print("=" * 50)
    print("Multimodal Understanding Test")
    print("=" * 50)
    
    processor = MultimodalProcessor()
    
    # 检查已有截图
    workspace = Path("C:/Users/ThinkPad/.openclaw/workspace")
    screenshots = list(workspace.glob("**/screenshot*.png"))
    
    print(f"\nFound {len(screenshots)} screenshot(s)")
    
    if screenshots:
        # 分析第一张截图
        img_path = str(screenshots[0])
        print(f"\nAnalyzing: {screenshots[0].name}")
        
        result = processor.image_analyzer.analyze_image(img_path)
        
        print("\nImage Analysis Result:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    
    # 显示支持格式
    print("\nSupported Image Formats:")
    print(f"  {', '.join(processor.image_analyzer.supported_formats)}")
    
    print("\nSupported Video Formats:")
    print(f"  {', '.join(processor.video_analyzer.supported_formats)}")
    
    print("\nMultimodal understanding is ready!")


if __name__ == "__main__":
    main()
