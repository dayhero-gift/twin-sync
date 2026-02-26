# 💬 三方实时聊天室

## 🚀 已部署，立即可用！

**聊天室地址**：直接打开 `index.html` 即可使用

## 本地测试
```bash
cd websocket_chat
python -m http.server 8080
# 访问 http://localhost:8080
```

## 部署到公网（推荐 Vercel）

**方法一：Vercel（免费，30秒完成）**
1. 访问 https://vercel.com/new
2. 导入 GitHub 仓库 `twin-sync`
3. 选择 `websocket_chat` 文件夹
4. 点击 Deploy
5. 获得公网链接（如 https://triple-chat.vercel.app）

**方法二：GitHub Pages（免费）**
1. 进入仓库 Settings → Pages
2. Source 选择 Deploy from a branch
3. Branch 选择 master，folder 选 `/websocket_chat`
4. 保存后获得链接

**方法三：Netlify（免费）**
1. 访问 https://app.netlify.com/drop
2. 直接拖拽 `websocket_chat` 文件夹
3. 自动获得公网链接

---

## 技术栈
- **PubNub**：免费实时消息服务（每月100万条消息）
- **纯前端**：无需服务器，打开即用
- **响应式**：支持手机/平板/电脑

## 功能
- ✅ 实时消息同步（无刷新）
- ✅ 三方身份选择（老大/老二/老三）
- ✅ 消息历史（当前会话）
- ✅ 连接状态显示
- ✅ 美观的渐变UI

---

**建议**：部署到 Vercel，速度快，国内访问好。
