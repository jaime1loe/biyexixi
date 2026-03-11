import sys
from pathlib import Path

# 设置输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    print("=" * 60)
    print("启动后端服务器...")
    print("=" * 60)
    
    # 导入应用
    from main import app
    
    # 使用uvicorn启动服务器
    import uvicorn
    
    print("\n服务器配置:")
    print(f"  主机: 0.0.0.0")
    print(f"  端口: 8000")
    print(f"  调试模式: True")
    print(f"  自动重载: True")
    print("\n" + "=" * 60)
    print("服务器正在启动，请访问:")
    print("  http://localhost:8000")
    print("  http://localhost:8000/docs (API文档)")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    
except KeyboardInterrupt:
    print("\n\n服务器已停止")
except Exception as e:
    print(f"\n启动失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
