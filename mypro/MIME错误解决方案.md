# MIME类型错误解决方案

## 错误信息
```
Failed to load module script: Expected a JavaScript-or-Wasm module script
but the server responded with a MIME type of "text/html".
Strict MIME type checking is enforced for module scripts per HTML spec.
```

## 问题原因
这个错误通常由以下几个原因造成：

1. **Vite缓存问题** - Vite的缓存文件损坏或过期
2. **MIME类型配置错误** - 服务器返回了错误的Content-Type头
3. **浏览器缓存问题** - 浏览器缓存了旧的响应
4. **端口冲突** - 其他服务占用了5173端口
5. **依赖问题** - node_modules中的文件损坏

## 解决方案

### 方案1：使用修复脚本（推荐）
```bash
双击运行 "修复乱码.bat"
```

该脚本会自动：
- 清除Vite缓存目录
- 清除dist目录
- 重新启动开发服务器
- 自动打开浏览器

### 方案2：手动清除缓存

**步骤1：停止前端服务**
在前端命令窗口按 `Ctrl + C` 停止服务

**步骤2：删除缓存目录**
```bash
cd frontend

# Windows
rmdir /s /q node_modules\.vite
rmdir /s /q dist

# PowerShell
Remove-Item -Recurse -Force node_modules\.vite
Remove-Item -Recurse -Force dist
```

**步骤3：重新启动**
```bash
npm run dev
```

### 方案3：清除浏览器缓存

**Chrome/Edge浏览器：**
1. 按 `Ctrl + Shift + Delete`
2. 选择"缓存的图片和文件"
3. 时间范围选择"全部时间"
4. 点击"清除数据"
5. 按 `Ctrl + Shift + R` 强制刷新

**Firefox浏览器：**
1. 按 `Ctrl + Shift + Delete`
2. 选择"缓存"
3. 时间范围选择"全部时间"
4. 点击"立即清除"
5. 按 `Ctrl + F5` 强制刷新

### 方案4：检查端口占用

**查看端口占用：**
```bash
netstat -ano | findstr :5173
```

**如果端口被占用，选择以下方案之一：**

**方案A：结束占用进程**
```bash
# 使用查到的PID（进程ID）
taskkill /F /PID <进程ID>
```

**方案B：修改Vite端口**
编辑 `vite.config.ts`：
```typescript
server: {
  port: 5174,  // 改成其他端口
  // ...
}
```

### 方案5：重新安装依赖（最彻底）

**步骤1：停止服务**
在前端和后端命令窗口按 `Ctrl + C` 停止所有服务

**步骤2：删除node_modules**
```bash
cd frontend

# Windows
rmdir /s /q node_modules

# PowerShell
Remove-Item -Recurse -Force node_modules

# 或者使用Git Bash
rm -rf node_modules
```

**步骤3：清除npm缓存**
```bash
npm cache clean --force
```

**步骤4：重新安装依赖**
```bash
npm install --registry=https://registry.npmmirror.com
```

**步骤5：重新启动**
```bash
npm run dev
```

## 已实施的修复

### 1. 修复Vite配置
移除了错误的headers配置，该配置会强制所有响应为text/html：
```typescript
// ❌ 错误配置（已移除）
server: {
  headers: {
    'Content-Type': 'text/html; charset=utf-8'  // 这会导致模块加载失败
  }
}

// ✅ 正确配置
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

### 2. 添加favicon
创建了 `public/favicon.svg` 文件，消除404错误：
```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
```

### 3. 更新启动脚本
启动脚本现在会自动检查并安装依赖：
```bash
if not exist "node_modules" (
    echo 正在安装依赖...
    call npm install --registry=https://registry.npmmirror.com
)
```

## 验证修复成功

修复后，打开浏览器开发者工具（F12）：
1. **Console标签** - 不应该有MIME类型错误
2. **Network标签** - `/src/main.ts` 的Content-Type应该是 `application/javascript` 或 `text/javascript`
3. **页面显示** - 应该能看到登录页面，中文正常显示

## 预防措施

### 1. 定期清理Vite缓存
在项目根目录添加脚本：
```bash
@echo off
cd frontend
rmdir /s /q node_modules\.vite
echo Vite缓存已清除
```

### 2. 使用.gitignore
确保 `.vite` 目录不被提交：
```
# .gitignore
node_modules/.vite
dist
```

### 3. 使用稳定的Vite版本
```json
{
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

## 常见问题

### Q1: 清除缓存后还是报错？
A: 尝试重新安装依赖（方案5），这是最彻底的方法

### Q2: 修改了配置文件但没生效？
A: 需要停止并重新启动开发服务器，配置才会生效

### Q3: 可以直接改用其他端口吗？
A: 可以，但需要同时更新启动脚本中的浏览器URL和API代理配置

### Q4: 生产环境也会出现这个问题吗？
A: 不会，生产构建后的文件使用标准MIME类型，不会有这个问题

## 获取更多帮助

如果以上方法都无法解决问题，请：
1. 查看浏览器开发者工具的Console和Network标签
2. 查看命令窗口的完整错误信息
3. 记录你的操作系统和浏览器版本
4. 提供截图和错误堆栈信息

## 成功标志

当问题解决后，你应该看到：
- ✅ 浏览器控制台没有MIME类型错误
- ✅ Network标签中main.ts的类型是application/javascript
- ✅ 页面正常加载并显示登录界面
- ✅ 没有favicon的404错误
