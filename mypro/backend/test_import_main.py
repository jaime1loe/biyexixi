# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')

try:
    print("尝试导入main...")
    from main import app
    print("导入成功!")
except Exception as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()
