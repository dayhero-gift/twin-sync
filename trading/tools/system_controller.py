"""
System Controller - Local computer operations
For file management, system commands, environment control
"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class SystemController:
    """System controller - use computer as body"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace) if workspace else \
            Path("C:/Users/ThinkPad/.openclaw/workspace")
        self.workspace.mkdir(parents=True, exist_ok=True)
    
    # ========== File Management ==========
    
    def list_directory(self, path: str = None, pattern: str = "*") -> List[Dict]:
        """List directory contents"""
        target = Path(path) if path else self.workspace
        
        if not target.exists():
            return [{"error": f"Path not found: {path}"}]
        
        items = []
        for item in target.glob(pattern):
            stat = item.stat()
            items.append({
                "name": item.name,
                "path": str(item.absolute()),
                "type": "directory" if item.is_dir() else "file",
                "size": stat.st_size if item.is_file() else None,
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "extension": item.suffix if item.is_file() else None
            })
        
        return sorted(items, key=lambda x: (x["type"] != "directory", x["name"]))
    
    def create_directory(self, path: str) -> Dict:
        """Create directory"""
        target = Path(path)
        try:
            target.mkdir(parents=True, exist_ok=True)
            return {"success": True, "path": str(target.absolute())}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def copy_file(self, src: str, dst: str) -> Dict:
        """Copy file/directory"""
        try:
            src_path = Path(src)
            dst_path = Path(dst)
            
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
            
            return {"success": True, "src": src, "dst": dst}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def move_file(self, src: str, dst: str) -> Dict:
        """Move file/directory"""
        try:
            shutil.move(src, dst)
            return {"success": True, "src": src, "dst": dst}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_file(self, path: str, confirm: bool = False) -> Dict:
        """Delete file/directory"""
        if not confirm:
            return {"success": False, "error": "Need confirm=True to delete"}
        
        try:
            target = Path(path)
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            return {"success": True, "deleted": path}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_files(self, pattern: str, path: str = None, recursive: bool = True) -> List[Dict]:
        """Search files"""
        target = Path(path) if path else self.workspace
        
        results = []
        search_pattern = "**/*" if recursive else "*"
        
        for item in target.glob(search_pattern):
            if pattern.lower() in item.name.lower():
                results.append({
                    "name": item.name,
                    "path": str(item.absolute()),
                    "type": "directory" if item.is_dir() else "file"
                })
        
        return results
    
    def get_disk_usage(self) -> Dict:
        """Get disk usage"""
        usage = shutil.disk_usage(self.workspace)
        return {
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "free_gb": round(usage.free / (1024**3), 2),
            "usage_percent": round(usage.used / usage.total * 100, 2)
        }
    
    # ========== System Commands ==========
    
    def run_command(self, command: str, cwd: str = None, timeout: int = 30) -> Dict:
        """Execute system command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or str(self.workspace),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timeout ({timeout}s)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_python(self, code: str) -> Dict:
        """Execute Python code"""
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            result = self.run_command(f"python {temp_file}")
            
            Path(temp_file).unlink(missing_ok=True)
            
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ========== Environment Info ==========
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        import platform
        
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "workspace": str(self.workspace)
        }
    
    def get_env(self, key: str = None) -> Dict:
        """Get environment variables"""
        if key:
            return {key: os.environ.get(key)}
        return dict(os.environ)


def main():
    """Test system controller"""
    print("=" * 50)
    print("System Controller Test")
    print("=" * 50)
    
    ctrl = SystemController()
    
    # System info
    print("\nSystem Info:")
    info = ctrl.get_system_info()
    for k, v in info.items():
        print(f"  {k}: {v}")
    
    # Disk usage
    print("\nDisk Usage:")
    usage = ctrl.get_disk_usage()
    print(f"  Total: {usage['total_gb']} GB")
    print(f"  Used: {usage['used_gb']} GB ({usage['usage_percent']}%)")
    print(f"  Free: {usage['free_gb']} GB")
    
    # List workspace
    print("\nWorkspace Contents:")
    items = ctrl.list_directory()[:10]
    for item in items:
        icon = "D" if item["type"] == "directory" else "F"
        size = f"({item['size']} bytes)" if item["size"] else ""
        print(f"  [{icon}] {item['name']} {size}")
    
    # Search files
    print("\nSearch 'trading':")
    results = ctrl.search_files("trading")
    for r in results[:5]:
        print(f"  {r['name']}")


if __name__ == "__main__":
    main()
