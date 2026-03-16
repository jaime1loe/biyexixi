# 登录背景图片配置指南

## 步骤 1: 复制图片文件

请将以下图片文件复制到前端静态资源目录：

**源文件：** `C:\Users\19719\Desktop\2026毕业实习\mypro\login.png`  
**目标位置：** `C:\Users\19719\Desktop\2026毕业实习\mypro\frontend\public\login.png`

## 步骤 2: 复制方法

### 方法 1: 手动复制
1. 找到文件：`C:\Users\19719\Desktop\2026毕业实习\mypro\login.png`
2. 复制该文件
3. 打开文件夹：`C:\Users\19719\Desktop\2026毕业实习\mypro\frontend\public\`
4. 粘贴文件

### 方法 2: 使用命令行
```bash
copy "C:\Users\19719\Desktop\2026毕业实习\mypro\login.png" "C:\Users\19719\Desktop\2026毕业实习\mypro\frontend\public\login.png"
```

## 步骤 3: 验证配置

确认文件已成功复制到：
`C:\Users\19719\Desktop\2026毕业实习\mypro\frontend\public\login.png`

## 步骤 4: 测试效果

1. 启动前端开发服务器
2. 访问登录页面：`http://localhost:5173/login`
3. 检查背景图片是否正常显示

## 为什么这样配置？

1. **使用public目录**：Vite会自动将public目录中的文件复制到构建输出根目录
2. **绝对路径引用**：使用 `/login.png` 可以在任何电脑上正确显示，不依赖本地路径
3. **背景覆盖设置**：`background-size: cover` 确保图片适配不同屏幕尺寸
4. **添加遮罩层**：使用半透明黑色遮罩提高文字可读性

## 自定义调整

如果需要调整背景效果，可以修改以下CSS属性：

```css
.login-container {
  background-image: url('/login.png');           /* 背景图片路径 */
  background-size: cover;                        /* 覆盖整个区域 */
  background-position: center;                  /* 居中显示 */
  background-repeat: no-repeat;                 /* 不重复 */
}

.login-container::before {
  background: rgba(0, 0, 0, 0.3);              /* 遮罩透明度 (0-1) */
  backdrop-filter: blur(2px);                    /* 模糊效果 (0-10px) */
}
```

## 故障排除

### 背景图片不显示
1. 检查图片是否正确复制到 `frontend/public/login.png`
2. 清除浏览器缓存并刷新页面
3. 检查浏览器控制台是否有加载错误

### 图片路径问题
使用 `/login.png` 而不是相对路径，这样可以确保在任何电脑上都能正确访问。

### 图片显示不清晰
考虑使用更高分辨率的图片，或者调整 `background-size` 属性。