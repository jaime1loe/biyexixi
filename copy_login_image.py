import shutil
import os

source = 'C:/Users/19719/Desktop/2026毕业实习/mypro/login.png'
dest = 'C:/Users/19719/Desktop/2026毕业实习/mypro/frontend/public/login.png'

if os.path.exists(source):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(source, dest)
    print(f"Successfully copied {source} to {dest}")
else:
    print(f"Source file does not exist: {source}")