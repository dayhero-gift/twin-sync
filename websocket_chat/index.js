// WebSocket 聊天室 - Cloudflare Workers 版本
// 部署: wrangler deploy

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // 静态页面
    if (url.pathname === '/') {
      return new Response(HTML, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }
    
    // WebSocket 连接
    if (url.pathname === '/ws') {
      if (request.headers.get('Upgrade') === 'websocket') {
        return handleWebSocket(request);
      }
      return new Response('Expected websocket', { status: 400 });
    }
    
    return new Response('Not found', { status: 404 });
  }
};

// HTML 聊天界面
const HTML = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>三方实时聊天室</title>
  <style>
    body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
    #chat { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
    .message { margin: 5px 0; padding: 8px; border-radius: 5px; }
    .老大 { background: #ffebee; }
    .老二 { background: #e3f2fd; }
    .老三 { background: #f3e5f5; }
    .system { background: #f5f5f5; font-style: italic; }
    select, input, button { padding: 10px; margin: 5px; }
    input { width: 60%; }
  </style>
</head>
<body>
  <h2>💬 三方实时聊天室</h2>
  <div>
    <label>身份:</label>
    <select id="role">
      <option value="老大">老大（洛君）</option>
      <option value="老二">老二（小天）</option>
      <option value="老三">老三（云端）</option>
    </select>
    <button onclick="connect()">连接</button>
    <span id="status" style="color: red;">未连接</span>
  </div>
  <div id="chat"></div>
  <div>
    <input type="text" id="msg" placeholder="输入消息..." onkeypress="if(event.key==='Enter')send()">
    <button onclick="send()">发送</button>
  </div>
  
  <script>
    let ws;
    let role = '老大';
    
    function connect() {
      role = document.getElementById('role').value;
      const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
      ws = new WebSocket(protocol + '//' + location.host + '/ws?role=' + role);
      
      ws.onopen = () => {
        document.getElementById('status').textContent = '已连接 ✅';
        document.getElementById('status').style.color = 'green';
        addMessage('系统', '已连接到聊天室');
      };
      
      ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        addMessage(data.role, data.message, data.time);
      };
      
      ws.onclose = () => {
        document.getElementById('status').textContent = '已断开 ❌';
        document.getElementById('status').style.color = 'red';
        addMessage('系统', '连接已断开');
      };
    }
    
    function send() {
      const input = document.getElementById('msg');
      if (ws && ws.readyState === WebSocket.OPEN && input.value) {
        ws.send(input.value);
        input.value = '';
      }
    }
    
    function addMessage(role, msg, time) {
      const chat = document.getElementById('chat');
      const div = document.createElement('div');
      div.className = 'message ' + role;
      const t = time ? new Date(time).toLocaleTimeString() : new Date().toLocaleTimeString();
      div.innerHTML = '<strong>[' + t + '] ' + role + ':</strong> ' + msg;
      chat.appendChild(div);
      chat.scrollTop = chat.scrollHeight;
    }
    
    // 自动连接
    connect();
  </script>
</body>
</html>`;

// WebSocket 处理
function handleWebSocket(request) {
  const url = new URL(request.url);
  const role = url.searchParams.get('role') || '匿名';
  
  const [client, server] = Object.values(new WebSocketPair());
  
  server.accept();
  
  // 广播消息给所有连接
  server.addEventListener('message', (event) => {
    const message = {
      role: role,
      message: event.data,
      time: new Date().toISOString()
    };
    
    // 这里需要 Durable Objects 来广播
    // 简化版：只回复发送者
    server.send(JSON.stringify(message));
  });
  
  return new Response(null, {
    status: 101,
    webSocket: client
  });
}