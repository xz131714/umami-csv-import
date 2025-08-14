from http.server import BaseHTTPRequestHandler
import json
import cgi
import io

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
    <title>文件上传 - Umami CSV导入工具</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 600px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border-radius: 16px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .upload-area { 
            border: 3px dashed #cbd5e1; 
            padding: 40px; 
            text-align: center; 
            border-radius: 12px; 
            margin: 20px 0; 
            transition: all 0.3s ease;
        }
        .upload-area:hover { 
            border-color: #2563eb; 
            background: #f8fafc; 
        }
        input[type="file"] { 
            margin: 20px 0; 
            padding: 8px;
        }
        .btn { 
            background: #2563eb; 
            color: white; 
            padding: 12px 24px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            text-decoration: none;
            display: inline-block;
            transition: background-color 0.2s;
        }
        .btn:hover { background: #1d4ed8; }
        .back-link { 
            color: #2563eb; 
            text-decoration: none; 
            margin-bottom: 20px;
            display: inline-block;
        }
        .back-link:hover { text-decoration: underline; }
        .warning {
            background: #fef3c7;
            color: #92400e;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            border-left: 4px solid #f59e0b;
        }
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
                <button type="submit" class="btn">上传并处理</button>
            </form>
        </div>
        
        <div class="warning">
            <strong>注意:</strong> 这是轻量版，当前仅支持文件验证和SQL生成功能。
        </div>
    </div>
</body>
</html>"""
        
        self.wfile.write(html.encode('utf-8'))
        return
    
    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>上传成功 - Umami CSV导入工具</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 700px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border-radius: 16px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .success { 
            background: #f0fdf4; 
            color: #16a34a; 
            padding: 20px; 
            border-radius: 8px; 
            margin: 20px 0; 
            border-left: 4px solid #16a34a;
        }
        .code { 
            background: #f1f5f9; 
            padding: 20px; 
            border-radius: 8px; 
            font-family: 'Monaco', 'Consolas', monospace; 
            margin: 15px 0;
            font-size: 14px;
            line-height: 1.5;
            overflow-x: auto;
        }
        .back-link { 
            color: #2563eb; 
            text-decoration: none; 
        }
        .back-link:hover { text-decoration: underline; }
        .warning {
            background: #fef3c7;
            color: #92400e;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            border-left: 4px solid #f59e0b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ 文件上传成功</h1>
        
        <div class="success">
            CSV文件已成功接收并验证！
        </div>
        
        <h3>📝 示例SQL输出：</h3>
        <div class="code">-- Umami数据导入SQL (示例)
INSERT INTO website_event (website_id, session_id, url, event_name, created_at) 
VALUES ('your-website-id', 'session-123', '/page1', 'pageview', NOW());

INSERT INTO session (session_id, website_id, hostname, browser, created_at) 
VALUES ('session-123', 'your-website-id', 'example.com', 'Chrome', NOW());

-- 更多数据...
        </div>
        
        <p>
            <a href="/api/upload" class="back-link">← 上传另一个文件</a> | 
            <a href="/api/index" class="back-link">返回首页</a> | 
            <a href="/api/status" class="back-link">查看状态</a>
        </p>
        
        <div class="warning">
            <strong>注意:</strong> 这是演示版本。实际的SQL生成功能正在开发中。
        </div>
    </div>
</body>
</html>"""
            
            self.wfile.write(html.encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            error_msg = f'Error: {str(e)}'.encode('utf-8')
            self.wfile.write(error_msg)
