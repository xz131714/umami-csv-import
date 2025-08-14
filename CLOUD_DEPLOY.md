# 🌐 云端部署完全指南

纯云端部署，无需本地环境，通过GitHub连接各大平台。

## 🚀 准备工作

### 1. 创建GitHub仓库
1. 登录 [GitHub](https://github.com)
2. 点击 "New repository"
3. 仓库名: `umami-csv-import`
4. 设为公开 (Public)
5. 初始化README

### 2. 上传代码到GitHub
1. 下载项目ZIP文件
2. 解压到本地
3. 通过GitHub网页界面上传文件
4. 或使用GitHub Desktop

## 🎯 平台部署选择

### 方案对比

| 平台 | 版本 | 功能 | 费用 | 推荐度 |
|------|------|------|------|--------|
| **Vercel** | 轻量版 | SQL生成 | 免费 | ⭐⭐⭐⭐⭐ |
| **Railway** | 完整版 | 直连数据库 | 免费试用 | ⭐⭐⭐⭐⭐ |
| **Render** | 完整版 | 直连数据库 | 免费 | ⭐⭐⭐⭐ |
| **Cloudflare Pages** | 轻量版 | SQL生成 | 免费 | ⭐⭐⭐ |

---

## 🚀 Vercel 部署 (推荐新手)

### 特点
- ✅ 完全免费
- ✅ 部署最简单
- ✅ 速度最快
- ❌ 功能受限 (仅生成SQL)

### 部署步骤
1. **访问**: [vercel.com](https://vercel.com)
2. **登录**: 使用GitHub账号
3. **导入项目**: 
   - 点击 "New Project"
   - 选择您的GitHub仓库
   - 点击 "Import"
4. **配置项目**:
   - Project Name: `umami-csv-import`
   - Framework Preset: `Other`
   - Root Directory: `web-app`
   - Build Command: 留空
   - Install Command: `pip install -r requirements_lite.txt`
5. **环境变量**:
   - `FLASK_ENV`: `production`
   - `FLASK_SECRET_KEY`: `your-secret-key`
6. **点击 Deploy**

### 一键部署按钮
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/umami-csv-import/tree/main/web-app)

---

## 🚂 Railway 部署 (推荐完整功能)

### 特点
- ✅ 完整功能
- ✅ 直连数据库
- ✅ 免费试用额度
- ✅ GitHub集成

### 部署步骤
1. **访问**: [railway.app](https://railway.app)
2. **登录**: 使用GitHub账号
3. **新建项目**:
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择您的仓库
4. **配置服务**:
   - 检测到Python应用
   - Root Directory: `web-app`
   - Start Command: `gunicorn app:app`
5. **环境变量**:
   - `FLASK_ENV`: `production`
   - `PORT`: `${{PORT}}`
6. **自动部署**

### 一键部署按钮
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/umami-csv-import&referralCode=YOUR_CODE)

---

## 🎨 Render 部署 (稳定免费)

### 特点
- ✅ 免费层永久
- ✅ 完整功能
- ✅ 自动SSL证书
- ❌ 冷启动较慢

### 部署步骤
1. **访问**: [render.com](https://render.com)
2. **登录**: 使用GitHub账号
3. **新建服务**:
   - 点击 "New +"
   - 选择 "Web Service"
   - 连接GitHub仓库
4. **配置**:
   - Name: `umami-csv-import`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: `Free`
5. **高级设置**:
   - Root Directory: `web-app`
6. **环境变量**:
   - `FLASK_ENV`: `production`
   - `PYTHON_VERSION`: `3.9.18`
7. **创建服务**

### 一键部署按钮
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/umami-csv-import)

---

## ☁️ Cloudflare Pages 部署

### 特点
- ✅ 免费且快速
- ✅ 全球CDN
- ❌ 功能受限
- ❌ 配置复杂

### 部署步骤
1. **访问**: [pages.cloudflare.com](https://pages.cloudflare.com)
2. **登录**: 创建Cloudflare账号
3. **创建项目**:
   - 点击 "Create a project"
   - 连接GitHub
   - 选择仓库
4. **构建设置**:
   - Project name: `umami-csv-import`
   - Production branch: `main`
   - Root directory: `web-app`
   - Build command: `echo "Static build"`
   - Build output: `/`
5. **环境变量**:
   - `PYTHON_VERSION`: `3.9`
   - `FLASK_ENV`: `production`
6. **保存并部署**

---

## 🔧 自动部署配置

### GitHub Actions (推荐)
已配置自动部署，推送代码自动触发：
- ✅ Vercel 自动部署
- ✅ Railway 自动部署  
- ✅ 构建测试

### 所需Secrets
在GitHub仓库设置中添加：

**Vercel**:
- `VERCEL_TOKEN`: 从 Vercel → Settings → Tokens
- `VERCEL_ORG_ID`: 从 `.vercel/project.json`
- `VERCEL_PROJECT_ID`: 从 `.vercel/project.json`

**Railway**:
- `RAILWAY_TOKEN`: 从 Railway → Account → Tokens
- `RAILWAY_SERVICE`: 服务ID

---

## 📋 部署检查清单

### 部署前
- [ ] GitHub仓库已创建
- [ ] 代码已上传
- [ ] README.md已更新
- [ ] 配置文件检查完毕

### 部署后
- [ ] 应用可以访问
- [ ] 文件上传正常
- [ ] 数据预览正确
- [ ] SQL生成功能正常
- [ ] 下载功能正常

### 自定义域名 (可选)
- [ ] DNS记录配置
- [ ] SSL证书自动配置
- [ ] CNAME记录验证

---

## 🎯 推荐路径

### 新手用户
1. **Vercel** (最简单) → 快速体验
2. **Railway** (完整功能) → 生产使用

### 高级用户
1. **Render** (稳定) → 长期运行
2. **Cloudflare** (性能) → 全球访问

### 企业用户
1. **自建VPS** → 完全控制
2. **AWS/GCP** → 企业级

---

## 🆘 故障排除

### 常见问题
1. **构建失败**: 检查依赖文件路径
2. **访问404**: 检查Root Directory设置
3. **功能异常**: 检查环境变量配置
4. **部署超时**: 选择其他平台

### 获取帮助
- 📖 查看平台官方文档
- 🐛 在GitHub Issues提问
- 💬 加入社区讨论

---

## 🎉 成功示例

部署成功后，您将得到类似的URL：
- **Vercel**: `https://umami-csv-import.vercel.app`
- **Railway**: `https://umami-csv-import.railway.app`
- **Render**: `https://umami-csv-import.onrender.com`
- **Cloudflare**: `https://umami-csv-import.pages.dev`

现在您可以：
1. Fork这个项目到您的GitHub
2. 选择适合的平台部署
3. 几分钟内即可使用！
