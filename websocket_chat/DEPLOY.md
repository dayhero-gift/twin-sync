# 🚀 三方实时聊天室 - 部署指南

## 方案：Vercel + Firebase（免费）

### 快速部署（3分钟）

**步骤1：创建 Firebase 项目**
1. 访问 https://console.firebase.google.com/
2. 创建新项目（如：triple-chat）
3. 进入 Realtime Database
4. 创建数据库，选择位置（asia-southeast1 新加坡）
5. 规则设为测试模式：
```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```
6. 复制数据库URL（如：https://triple-chat-xxxxx-default-rtdb.asia-southeast1.firebasedatabase.app）

**步骤2：部署到 Vercel**
1. 访问 https://vercel.com/new
2. 导入 GitHub 仓库（twin-sync/websocket_chat）
3. 直接部署
4. 复制生成的域名（如：https://triple-chat.vercel.app）

**步骤3：更新 Firebase 配置**
1. 修改 index.html 中的 databaseURL
2. 重新部署

---

## 备选：直接运行本地服务器

```bash
cd websocket_chat
python -m http.server 8080
```

访问 http://localhost:8080

---

## 功能特点
- ✅ 实时消息同步
- ✅ 三方身份选择（老大/老二/老三）
- ✅ 消息历史记录
- ✅ 响应式设计
- ✅ 免费托管

---

## 需要老大操作
1. 创建 Firebase 项目（2分钟）
2. 复制数据库 URL 给我
3. 我更新配置并部署

**预计总时间：5分钟**
