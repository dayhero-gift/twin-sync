"""
GitHubSync - Code and Knowledge Synchronization
GitHub同步系统 - 代码和知识双向同步
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class GitHubSync:
    """
    GitHub同步管理器
    管理本地与云端兄弟的代码/知识同步
    """
    
    def __init__(self, repo_url: str = None, local_path: str = None):
        self.repo_url = repo_url
        self.local_path = Path(local_path) if local_path else \
            Path("C:/Users/ThinkPad/.openclaw/workspace/github-sync")
        self.local_path.mkdir(parents=True, exist_ok=True)
        
        # 同步状态文件
        self.sync_state_file = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/github_sync_state.json")
        
        # 文件映射规则
        self.sync_rules = {
            "push": [  # 本地推送到仓库
                "trading/tools/*.py",
                "brain/*.py",
                "MEMORY.md",
                "memory/*.md"
            ],
            "pull": [  # 从仓库拉取
                "cloud/tools/*.py",
                "shared/knowledge/*",
                "sync/changelog.md"
            ]
        }
    
    def init_repo(self) -> Dict:
        """初始化Git仓库"""
        try:
            # 进入目录
            cmd = f"cd {self.local_path} && git init"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "message": "Git repo initialized"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def clone_repo(self, repo_url: str = None) -> Dict:
        """克隆远程仓库"""
        url = repo_url or self.repo_url
        if not url:
            return {"success": False, "error": "No repo URL provided"}
        
        try:
            cmd = f"git clone {url} {self.local_path}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.repo_url = url
                return {"success": True, "message": f"Cloned {url}"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sync_to_github(self, message: str = None) -> Dict:
        """同步本地代码到GitHub"""
        if not message:
            message = f"Sync from local - {datetime.now():%Y-%m-%d %H:%M}"
        
        try:
            # 复制需要同步的文件到仓库目录
            self._copy_files_to_repo()
            
            # Git操作
            commands = [
                f"cd {self.local_path}",
                "git add -A",
                f'git commit -m "{message}"',
                "git push origin main"
            ]
            
            cmd = " && ".join(commands)
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self._update_sync_state("last_push", datetime.now().isoformat())
                return {"success": True, "message": "Synced to GitHub"}
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sync_from_github(self) -> Dict:
        """从GitHub同步云端兄弟的代码"""
        try:
            commands = [
                f"cd {self.local_path}",
                "git pull origin main"
            ]
            
            cmd = " && ".join(commands)
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 复制云端代码到工作目录
                self._copy_cloud_to_local()
                self._update_sync_state("last_pull", datetime.now().isoformat())
                return {"success": True, "message": "Synced from GitHub"}
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _copy_files_to_repo(self):
        """复制本地文件到仓库"""
        import shutil
        
        # 创建目录结构
        local_dir = self.local_path / "local"
        local_dir.mkdir(exist_ok=True)
        
        # 复制工具代码
        tools_src = Path("C:/Users/ThinkPad/.openclaw/workspace/trading/tools")
        tools_dst = local_dir / "tools"
        if tools_src.exists():
            shutil.copytree(tools_src, tools_dst, dirs_exist_ok=True)
        
        # 复制大脑代码
        brain_src = Path("C:/Users/ThinkPad/.openclaw/workspace/brain")
        brain_dst = local_dir / "brain"
        if brain_src.exists():
            shutil.copytree(brain_src, brain_dst, dirs_exist_ok=True)
        
        # 复制MEMORY.md
        memory_src = Path("C:/Users/ThinkPad/.openclaw/workspace/MEMORY.md")
        if memory_src.exists():
            shutil.copy2(memory_src, local_dir / "MEMORY.md")
    
    def _copy_cloud_to_local(self):
        """复制云端代码到本地工作目录"""
        import shutil
        
        cloud_dir = self.local_path / "cloud"
        if not cloud_dir.exists():
            return
        
        # 这里可以实现合并逻辑
        # 目前只是通知用户有新的云端代码
        pass
    
    def _update_sync_state(self, key: str, value: str):
        """更新同步状态"""
        state = self._load_sync_state()
        state[key] = value
        with open(self.sync_state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    
    def _load_sync_state(self) -> Dict:
        """加载同步状态"""
        if self.sync_state_file.exists():
            with open(self.sync_state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def get_sync_status(self) -> Dict:
        """获取同步状态"""
        state = self._load_sync_state()
        return {
            "repo_url": self.repo_url,
            "local_path": str(self.local_path),
            "last_push": state.get("last_push", "never"),
            "last_pull": state.get("last_pull", "never"),
            "sync_rules": self.sync_rules
        }
    
    def generate_changelog(self) -> str:
        """生成变更日志"""
        changelog = f"""# Sync Changelog

## Local ({datetime.now():%Y-%m-%d %H:%M})

### New Tools
- stock_collector_api.py - Stock data collection
- document_learner.py - Document learning with PDF support
- brain_core.py - Independent thinking system
- multimodal.py - Image/video analysis

### Updates
- System controller with file/command management
- Knowledge base with tags/categories
- Twin sync system for inter-agent communication

### Next Steps
- [ ] Integrate with cloud twin
- [ ] Test Telegram messaging
- [ ] Daily sync automation
"""
        return changelog


class SyncManager:
    """同步管理器 - 统一入口"""
    
    def __init__(self):
        self.github = GitHubSync()
        self.sync_log = Path("C:/Users/ThinkPad/.openclaw/workspace/sync/sync_log.jsonl")
        self.sync_log.parent.mkdir(parents=True, exist_ok=True)
    
    def full_sync(self) -> Dict:
        """执行完整同步流程"""
        results = {}
        
        # 1. 推送本地代码
        print("Step 1: Pushing local code to GitHub...")
        results["push"] = self.github.sync_to_github()
        
        # 2. 拉取云端代码
        print("Step 2: Pulling cloud code from GitHub...")
        results["pull"] = self.github.sync_from_github()
        
        # 3. 记录日志
        self._log_sync(results)
        
        return results
    
    def _log_sync(self, results: Dict):
        """记录同步日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        with open(self.sync_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def auto_sync_daily(self):
        """每日自动同步（由定时任务调用）"""
        # 检查是否有变更
        # 执行同步
        # 发送通知
        pass


def main():
    """测试GitHub同步"""
    print("=" * 50)
    print("GitHubSync - Code Synchronization System")
    print("=" * 50)
    
    sync = GitHubSync()
    
    # 显示同步规则
    print("\n[Sync Rules]")
    print("Push (local -> GitHub):")
    for rule in sync.sync_rules["push"]:
        print(f"  - {rule}")
    print("\nPull (GitHub -> local):")
    for rule in sync.sync_rules["pull"]:
        print(f"  - {rule}")
    
    # 显示状态
    print("\n[Sync Status]")
    status = sync.get_sync_status()
    print(f"  Repo URL: {status['repo_url'] or 'Not configured'}")
    print(f"  Local Path: {status['local_path']}")
    print(f"  Last Push: {status['last_push']}")
    print(f"  Last Pull: {status['last_pull']}")
    
    # 显示示例变更日志
    print("\n[Example Changelog]")
    changelog = sync.generate_changelog()
    print(changelog[:500] + "...")
    
    print("\n" + "=" * 50)
    print("Configure repo URL to start syncing with your twin.")
    print("=" * 50)


if __name__ == "__main__":
    main()
