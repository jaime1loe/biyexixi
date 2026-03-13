import http.server
import socketserver
import os

PORT = 5173

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.path.dirname(__file__), 'frontend', 'dist'), **kwargs)
    
    def do_GET(self):
        # 如果请求根路径，返回index.html
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def main():
    # 检查是否有dist目录
    dist_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
    if not os.path.exists(dist_dir):
        print(f"[ERROR] 找不到dist目录: {dist_dir}")
        print("请先构建前端项目: cd frontend && npm run build")
        return
    
    print(f"在端口 {PORT} 启动HTTP服务器...")
    print(f"访问: http://localhost:{PORT}")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"服务器已启动，按 Ctrl+C 停止")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    main()