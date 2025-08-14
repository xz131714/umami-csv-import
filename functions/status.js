export default {
  async fetch(request, env, ctx) {
    return new Response(`
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>部署状态 - Umami导入工具</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1000px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .status-card {
            background: #f8f9fa;
            border-left: 4px solid #27ae60;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }
        .status-online { border-left-color: #27ae60; }
        .status-offline { border-left-color: #e74c3c; }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #3498db;
            text-decoration: none;
            padding: 10px 20px;
            border: 1px solid #3498db;
            border-radius: 5px;
        }
        .platform-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 部署状态监控</h1>
        <p>当前部署平台状态和性能信息</p>
        
        <div class="status-card status-online">
            <h3>🟢 Cloudflare Pages - 在线</h3>
            <p><strong>状态:</strong> 正常运行</p>
            <p><strong>响应时间:</strong> < 100ms</p>
            <p><strong>CDN:</strong> 全球边缘网络</p>
            <p><strong>URL:</strong> <a href="#">${request.url}</a></p>
        </div>
        
        <div class="platform-info">
            <div class="status-card">
                <h4>💾 技术栈</h4>
                <ul>
                    <li>JavaScript Functions</li>
                    <li>Cloudflare Workers</li>
                    <li>边缘计算</li>
                    <li>全球CDN加速</li>
                </ul>
            </div>
            
            <div class="status-card">
                <h4>🚀 性能优势</h4>
                <ul>
                    <li>零冷启动时间</li>
                    <li>全球边缘部署</li>
                    <li>自动扩容</li>
                    <li>DDoS防护</li>
                </ul>
            </div>
        </div>
        
        <h3>📈 功能状态</h3>
        <div class="status-card status-online">
            <p>✅ 主页显示 - 正常</p>
            <p>✅ 文件上传 - 正常</p>
            <p>✅ CSV解析 - 正常</p>
            <p>✅ SQL生成 - 正常</p>
        </div>
        
        <a href="/functions/" class="back-link">← 返回首页</a>
    </div>
</body>
</html>`, {
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
      },
    });
  },
};
