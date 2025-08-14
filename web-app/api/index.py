from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Umami CSV导入工具</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2563eb; }
                .success { color: #16a34a; background: #f0fdf4; padding: 10px; border-radius: 5px; }
                .feature { background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px; }
                button { background: #2563eb; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { background: #1d4ed8; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎉 Umami CSV导入工具 - 轻量版</h1>
                
                <div class="success">
                    ✅ Vercel部署成功！应用正在运行中...
                </div>
                
                <h2>功能特性</h2>
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
                
                <h2>使用说明</h2>
                <ol>
                    <li>配置您的数据库连接信息</li>
                    <li>上传CSV数据文件</li>
                    <li>预览数据并确认</li>
                    <li>生成SQL语句或直接导入</li>
                </ol>
                
                <button onclick="window.open('/api/upload', '_blank')">📁 上传文件</button>
                <button onclick="window.open('/api/status', '_blank')" style="background: #059669; margin-left: 10px;">📊 部署状态</button>
                
                <hr style="margin: 30px 0;">
                <small>
                    <strong>部署信息:</strong> Vercel Serverless | 
                    <strong>版本:</strong> Lite v1.0 | 
                    <strong>状态:</strong> 运行中 ✅
                </small>
            </div>
        </body>
        </html>
        '''
        
        self.wfile.write(html.encode())
        return
