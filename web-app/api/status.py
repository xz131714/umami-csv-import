from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>部署状态 - Umami CSV导入工具</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border-radius: 16px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .platform { 
            background: #f8fafc; 
            padding: 24px; 
            margin: 20px 0; 
            border-radius: 12px; 
            border-left: 4px solid #2563eb; 
        }
        .status-ok { border-left-color: #16a34a; }
        .status-limited { border-left-color: #f59e0b; }
        .badge { 
            padding: 6px 12px; 
            border-radius: 20px; 
            font-size: 12px; 
            font-weight: bold; 
            color: white; 
        }
        .badge-ok { background: #16a34a; }
        .badge-limited { background: #f59e0b; }
        .badge-full { background: #2563eb; }
        .back-link { 
            color: #2563eb; 
            text-decoration: none; 
            margin-bottom: 20px;
            display: inline-block;
        }
        .back-link:hover { text-decoration: underline; }
        .recommendation {
            background: #f0fdf4;
            color: #16a34a;
            padding: 24px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid #16a34a;
        }
        code {
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 部署状态监控</h1>
        
        <a href="/api/index" class="back-link">← 返回首页</a>
        
        <h2>云平台部署状态</h2>
        
        <div class="platform status-ok">
            <h3>Vercel - 轻量版 <span class="badge badge-ok">✅ 运行中</span></h3>
            <p><strong>功能:</strong> 基础文件上传、SQL生成演示</p>
            <p><strong>技术:</strong> Python标准库 + API路由</p>
            <p><strong>限制:</strong> 无数据库直连，仅生成SQL</p>
            <p><strong>访问:</strong> 当前页面 (已部署)</p>
        </div>
        
        <div class="platform status-limited">
            <h3>Railway - 完整版 <span class="badge badge-full">⏳ 待部署</span></h3>
            <p><strong>功能:</strong> 完整数据库连接、实时导入</p>
            <p><strong>技术:</strong> Flask + pandas + 数据库驱动</p>
            <p><strong>限制:</strong> 免费500小时/月</p>
            <p><strong>配置:</strong> railway.toml</p>
        </div>
        
        <div class="platform status-limited">
            <h3>Render - 完整版 <span class="badge badge-full">⏳ 待部署</span></h3>
            <p><strong>功能:</strong> 完整数据库连接、实时导入</p>
            <p><strong>技术:</strong> Flask + pandas + 数据库驱动</p>
            <p><strong>限制:</strong> 免费版15分钟休眠</p>
            <p><strong>配置:</strong> render.yaml</p>
        </div>
        
        <div class="recommendation">
            <h4>🎯 推荐使用方案</h4>
            <ol>
                <li><strong>Vercel (轻量版)</strong> - 快速预览和SQL生成</li>
                <li><strong>Railway/Render (完整版)</strong> - 生产环境直连数据库</li>
            </ol>
        </div>
        
        <h2>📋 部署说明</h2>
        
        <h3>⚡ Vercel部署 (当前版本)</h3>
        <ul>
            <li>✅ 自动识别 <code>api/*.py</code> 文件</li>
            <li>✅ 无需外部依赖</li>
            <li>✅ 访问路径: <code>/api/index</code>, <code>/api/upload</code>, <code>/api/status</code></li>
        </ul>
        
        <h3>🚄 Railway部署 (完整版)</h3>
        <ul>
            <li>支持完整的Flask应用</li>
            <li>需要 <code>requirements_full.txt</code></li>
            <li>自动启动命令: <code>gunicorn app:app</code></li>
        </ul>
        
        <h3>🎨 Render部署 (完整版)</h3>
        <ul>
            <li>支持完整的Flask应用</li>
            <li>需要 <code>requirements_full.txt</code></li>
            <li>配置文件: <code>render.yaml</code></li>
        </ul>
        
        <hr style="margin: 30px 0; border: none; border-top: 1px solid #e2e8f0;">
        <small style="color: #6b7280;">
            最后更新: 2025年8月14日 | 版本: v1.0 | 平台: Vercel Serverless
        </small>
    </div>
</body>
</html>"""
        
        self.wfile.write(html.encode('utf-8'))
        return
