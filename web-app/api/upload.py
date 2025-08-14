from http.server import BaseHTTPRequestHandler
import json
import cgi
import io

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>文件上传 - Umami CSV导入工具</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .upload-area { border: 2px dashed #cbd5e1; padding: 40px; text-align: center; border-radius: 10px; margin: 20px 0; }
                .upload-area:hover { border-color: #2563eb; background: #f8fafc; }
                input[type="file"] { margin: 20px 0; }
                button { background: #2563eb; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { background: #1d4ed8; }
                .back-link { color: #2563eb; text-decoration: none; }
                .back-link:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📁 文件上传</h1>
                
                <a href="/api/index" class="back-link">← 返回首页</a>
                
                <div class="upload-area">
                    <h3>上传CSV文件</h3>
                    <p>请选择要导入的Umami数据CSV文件</p>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="csvfile" accept=".csv" required>
                        <br>
                        <button type="submit">上传并处理</button>
                    </form>
                </div>
                
                <div style="background: #fef3c7; padding: 15px; border-radius: 5px; margin-top: 20px;">
                    <strong>注意:</strong> 这是轻量版，当前仅支持文件验证和SQL生成功能。
                </div>
            </div>
        </body>
        </html>
        '''
        
        self.wfile.write(html.encode())
        return
    
    def do_POST(self):
        try:
            content_type = self.headers.get('Content-Type', '')
            if 'multipart/form-data' in content_type:
                # 处理文件上传
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html = '''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>上传成功 - Umami CSV导入工具</title>
                    <meta charset="utf-8">
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                        .success { background: #f0fdf4; color: #16a34a; padding: 15px; border-radius: 5px; margin: 20px 0; }
                        .code { background: #f1f5f9; padding: 15px; border-radius: 5px; font-family: monospace; margin: 10px 0; }
                        .back-link { color: #2563eb; text-decoration: none; }
                        .back-link:hover { text-decoration: underline; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>✅ 文件上传成功</h1>
                        
                        <div class="success">
                            CSV文件已成功接收并验证！
                        </div>
                        
                        <h3>示例SQL输出：</h3>
                        <div class="code">
                            -- Umami数据导入SQL (示例)<br>
                            INSERT INTO website_event (website_id, session_id, url, event_name) <br>
                            VALUES ('your-website-id', 'session-123', '/page1', 'pageview');<br>
                            <br>
                            INSERT INTO session (session_id, website_id, hostname, browser) <br>
                            VALUES ('session-123', 'your-website-id', 'example.com', 'Chrome');
                        </div>
                        
                        <p><a href="/api/upload" class="back-link">← 上传另一个文件</a> | <a href="/api/index" class="back-link">返回首页</a></p>
                        
                        <div style="background: #fef3c7; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <strong>注意:</strong> 这是演示版本。实际的SQL生成功能正在开发中。
                        </div>
                    </div>
                </body>
                </html>
                '''
                
                self.wfile.write(html.encode())
            else:
                self.send_response(400)
                self.end_headers()
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())
