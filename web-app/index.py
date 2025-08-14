import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from app_lite import app

# Vercel WSGI兼容性
application = app

if __name__ == "__main__":
    app.run(debug=False)
