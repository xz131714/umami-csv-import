from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 重定向到主页面
        self.send_response(302)
        self.send_header('Location', '/api/index')
        self.end_headers()
        return
