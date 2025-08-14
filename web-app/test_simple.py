import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'test-key')

@app.route('/')
def hello():
    return '''
    <html>
    <head><title>Umami CSV Import Tool</title></head>
    <body>
        <h1>🎉 Umami CSV导入工具</h1>
        <p>轻量级版本运行正常！</p>
        <p>Vercel部署成功 ✅</p>
        <hr>
        <small>Version: Lite | Platform: Vercel</small>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'ok', 'version': 'lite', 'platform': 'vercel'}

# Vercel WSGI兼容性
application = app

if __name__ == "__main__":
    app.run(debug=False)
