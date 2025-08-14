# 🚀 Vercel 部署指南

## 准备工作

### 1. 安装 Vercel CLI
```bash
npm install -g vercel
```

### 2. 登录 Vercel
```bash
vercel login
```

## 部署步骤

### 方法一：命令行部署

1. **进入项目目录**
```bash
cd c:\Users\16865\Desktop\Umami\web-app
```

2. **切换到轻量级依赖**
```bash
copy requirements_lite.txt requirements.txt
```

3. **初始化部署**
```bash
vercel
```

按提示回答：
- Set up and deploy? → `Y`
- Which scope? → 选择您的账户
- Link to existing project? → `N`
- What's your project's name? → `umami-csv-import`
- In which directory is your code located? → `./`

4. **生产部署**
```bash
vercel --prod
```

### 方法二：GitHub 集成部署

1. **将代码推送到 GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/xz131714/umami-csv-import.git
git push -u origin main
```

2. **在 Vercel 导入项目**
- 访问 [vercel.com](https://vercel.com)
- 点击 "Import Project"
- 选择您的 GitHub 仓库
- 配置项目设置

## 项目配置

### vercel.json 配置说明
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app_lite.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app_lite.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  },
  "functions": {
    "app_lite.py": {
      "maxDuration": 30
    }
  }
}
```

### 环境变量设置
在 Vercel Dashboard 中设置：
- `FLASK_SECRET_KEY`: 您的密钥
- `FLASK_ENV`: `production`

## 功能说明

### 轻量版特点
- ✅ 仅使用 Flask 核心库
- ✅ 快速启动和响应
- ✅ 生成标准 SQL 语句
- ❌ 不直接连接数据库
- ❌ 需要手动执行 SQL

### 使用流程
1. 上传 CSV 文件
2. 预览数据结构
3. 配置 Website ID
4. 生成 SQL 语句
5. 下载或复制 SQL
6. 手动执行到数据库

## 故障排除

### 常见问题

1. **部署失败 - 包太大**
```bash
# 确保使用轻量级依赖
cp requirements_lite.txt requirements.txt
```

2. **Python 版本错误**
确保 `runtime.txt` 包含：
```
python-3.9
```

3. **路由不工作**
检查 `vercel.json` 中的路由配置

4. **静态文件 404**
确保静态文件路径正确

### 调试命令
```bash
# 本地测试
vercel dev

# 查看日志
vercel logs

# 查看域名
vercel domains ls
```

## 自定义域名

1. **添加域名**
```bash
vercel domains add yourdomain.com
```

2. **配置 DNS**
按 Vercel 提供的说明配置 DNS 记录

## 监控和分析

- 访问 Vercel Dashboard 查看：
  - 部署状态
  - 访问统计
  - 错误日志
  - 性能指标

## 成本说明

- **Hobby 计划**: 免费
  - 100GB 带宽/月
  - 无限部署
  - 社区支持

- **Pro 计划**: $20/月
  - 1TB 带宽/月
  - 高级功能
  - 邮件支持

## 完整部署脚本

创建 `deploy-vercel.bat`:
```batch
@echo off
echo 🚀 部署到 Vercel
echo.

echo 📦 准备轻量级版本...
copy requirements_lite.txt requirements.txt

echo 🔑 检查 Vercel 登录状态...
vercel whoami

echo 🚀 开始部署...
vercel --prod

echo ✅ 部署完成！
echo 🌐 访问您的应用：
vercel ls
pause
```

运行脚本：
```bash
deploy-vercel.bat
```

## 示例 URL

部署成功后，您将获得类似的 URL：
- `https://umami-csv-import.vercel.app`
- `https://umami-csv-import-git-main-username.vercel.app`

## 下一步

1. 测试所有功能
2. 配置自定义域名
3. 设置监控告警
4. 优化性能
5. 添加更多功能
