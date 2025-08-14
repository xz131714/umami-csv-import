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
            <title>部署状态 - Umami CSV导入工具</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .platform { background: #f8fafc; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #2563eb; }
                .status-ok { border-left-color: #16a34a; }
                .status-limited { border-left-color: #f59e0b; }
                .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white; }
                .badge-ok { background: #16a34a; }
                .badge-limited { background: #f59e0b; }
                .badge-full { background: #2563eb; }
                .back-link { color: #2563eb; text-decoration: none; }
                .back-link:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 部署状态监控</h1>
                
                <a href="/api/index" class="back-link">← 返回首页</a>
                
                <h2>云平台部署状态</h2>
                
                <div class="platform status-ok">
                    <h3>Vercel - 轻量版 <span class="badge badge-ok">运行中</span></h3>
                    <p><strong>功能:</strong> 基础文件上传、SQL生成演示</p>
                    <p><strong>技术:</strong> Python标准库 + API路由</p>
                    <p><strong>限制:</strong> 无数据库直连，仅生成SQL</p>
                    <p><strong>访问:</strong> 当前页面 (已部署)</p>
                </div>
                
                <div class="platform status-limited">
                    <h3>Railway - 完整版 <span class="badge badge-full">待部署</span></h3>
                    <p><strong>功能:</strong> 完整数据库连接、实时导入</p>
                    <p><strong>技术:</strong> Flask + pandas + 数据库驱动</p>
                    <p><strong>限制:</strong> 免费500小时/月</p>
                    <p><strong>配置:</strong> railway.toml</p>
                </div>
                
                <div class="platform status-limited">
                    <h3>Render - 完整版 <span class="badge badge-full">待部署</span></h3>
                    <p><strong>功能:</strong> 完整数据库连接、实时导入</p>
                    <p><strong>技术:</strong> Flask + pandas + 数据库驱动</p>
                    <p><strong>限制:</strong> 免费版15分钟休眠</p>
                    <p><strong>配置:</strong> render.yaml</p>
                </div>
                
                <h2>推荐使用方案</h2>
                
                <div style="background: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #16a34a;">🎯 推荐组合</h4>
                    <ol>
                        <li><strong>Vercel (轻量版)</strong> - 快速预览和SQL生成</li>
                        <li><strong>Railway/Render (完整版)</strong> - 生产环境直连数据库</li>
                    </ol>
                </div>
                
                <h2>部署说明</h2>
                
                <h3>📋 Vercel部署 (当前版本)</h3>
                <ul>
                    <li>自动识别 <code>api/*.py</code> 文件</li>
                    <li>无需外部依赖</li>
                    <li>访问路径: <code>/api/index</code>, <code>/api/upload</code></li>
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
            </div>
        </body>
        </html>
        '''
        
        self.wfile.write(html.encode())
        return
