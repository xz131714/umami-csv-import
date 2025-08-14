from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 设置响应头
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Umami CSV导入工具</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border-radius: 16px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { color: #2563eb; margin-bottom: 20px; }
        .success { 
            color: #16a34a; 
            background: #f0fdf4; 
            padding: 16px; 
            border-radius: 8px; 
            border-left: 4px solid #16a34a;
            margin: 20px 0;
        }
        .feature { 
            background: #f8fafc; 
            padding: 20px; 
            margin: 15px 0; 
            border-radius: 8px; 
            border-left: 4px solid #e2e8f0;
        }
        .btn {
            display: inline-block;
            background: #2563eb; 
            color: white; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 8px; 
            text-decoration: none;
            cursor: pointer;
            margin: 5px;
            transition: background-color 0.2s;
        }
        .btn:hover { background: #1d4ed8; }
        .btn-green { background: #059669; }
        .btn-green:hover { background: #047857; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Umami CSV导入工具 - 轻量版</h1>
        
        <div class="success">
            ✅ Vercel部署成功！应用正在运行中...
        </div>
        
        <h2>🚀 功能特性</h2>
        <div class="feature">
            <h3>📁 CSV文件处理</h3>
            <p>支持上传和处理CSV格式的Umami数据文件</p>
        </div>
        
        <div class="feature">
            <h3>🗄️ 数据库支持</h3>
            <p>支持MySQL和PostgreSQL数据库连接</p>
        </div>
        
        <div class="feature">
            <h3>🔄 SQL生成</h3>
            <p>自动生成INSERT SQL语句，便于手动执行</p>
        </div>
        
        <h2>📋 使用说明</h2>
        <ol>
            <li>配置您的数据库连接信息</li>
            <li>上传CSV数据文件</li>
            <li>预览数据并确认</li>
            <li>生成SQL语句或直接导入</li>
        </ol>
        
        <div style="margin: 30px 0;">
            <a href="/api/upload" class="btn">📁 上传文件</a>
            <a href="/api/status" class="btn btn-green">📊 部署状态</a>
        </div>
        
        <hr style="margin: 30px 0; border: none; border-top: 1px solid #e2e8f0;">
        <small style="color: #6b7280;">
            <strong>部署信息:</strong> Vercel Serverless | 
            <strong>版本:</strong> Lite v1.0 | 
            <strong>状态:</strong> 运行中 ✅
        </small>
    </div>
</body>
</html>"""
        
        # 写入响应
        self.wfile.write(html.encode('utf-8'))
        return
        return
