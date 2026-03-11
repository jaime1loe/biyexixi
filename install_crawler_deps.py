"""
安装爬虫所需的依赖包
"""

import subprocess
import sys

def install_dependencies():
    """安装依赖"""
    packages = [
        'requests',
        'beautifulsoup4',
        'lxml',
    ]

    print("=" * 60)
    print("正在安装爬虫依赖包...")
    print("=" * 60)

    for package in packages:
        print(f"\n安装 {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"[OK] {package} 安装成功")
        except Exception as e:
            print(f"[FAIL] {package} 安装失败: {e}")

    print("\n" + "=" * 60)
    print("依赖安装完成！")
    print("=" * 60)


if __name__ == '__main__':
    install_dependencies()
