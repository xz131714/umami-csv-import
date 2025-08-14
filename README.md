# Umami CSV 导入工具

🍜 一个基于 Cloudflare Pages 的完整 Umami CSV 数据导入解决方案

## 📋 项目概述

本工具提供了完整的 CSV 数据导入到 Umami 分析平台的解决方案，支持从简单的文件上传演示到高级的数据库配置和批量导入。

## 🚀 功能特性

### 📤 简单上传 (`upload.html`)
- 快速演示 CSV 转 SQL 功能
- 实时预览生成的 SQL 语句
- 支持文件拖拽上传
- 数据处理统计显示

### 🔧 高级配置 (`advanced.html`)
- **完整数据库支持**: MySQL 和 PostgreSQL
- **智能表单配置**: 数据库连接参数
- **批处理设置**: 可配置批处理大小
- **Python 脚本生成**: 自动生成完整的导入脚本
- **高级选项**: 清空表、验证结果等

### 📊 系统监控 (`status.html`)
- 实时系统状态监控
- 运行时间和性能指标
- 功能模块状态检查
- 实时操作日志
- 系统信息展示

### 🏠 主界面 (`main.html`, `index.html`)
- 功能导航和介绍
- 响应式设计
- 统一的用户界面

## 🛠️ 技术架构

- **前端**: HTML5, CSS3, JavaScript (原生)
- **部署**: Cloudflare Pages (静态托管)
- **样式**: 现代化响应式设计
- **后端逻辑**: Python 脚本生成 (客户端执行)

### ⚠️ 重要说明
- **Cloudflare Pages 限制**: 只支持静态网站，无法运行 Python 代码
- **工作流程**: 网页工具生成 Python 脚本 → 用户下载到本地 → 本地执行
- **网络要求**: 本地计算机需要能连接到目标数据库服务器
- **环境要求**: 用户本地需要安装 Python 3.6+ 环境

## 📂 项目结构

```
├── index.html          # 首页和导航
├── main.html           # 主功能页面
├── upload.html         # 简单上传演示
├── advanced.html       # 高级配置工具
├── status.html         # 系统状态监控
├── file.csv           # 示例 CSV 文件
├── hello.py           # Python 示例脚本
└── umami_universal_import.py # 完整导入脚本
```

## 💡 使用方法

### 快速开始
1. 访问首页 (`index.html`)
2. 选择所需功能:
   - **简单演示**: 点击"📤 简单上传"
   - **完整导入**: 点击"🔧 高级配置"
   - **系统监控**: 点击"📊 查看状态"

### 高级导入流程
1. 进入高级配置页面
2. 填写数据库连接信息:
   - 选择数据库类型 (MySQL/PostgreSQL)
   - 输入连接参数 (主机、端口、用户名、密码等)
   - 设置目标 Website ID
3. 上传 CSV 文件
4. 配置高级选项 (批处理大小、清空表等)
5. 生成 Python 脚本
6. 下载并在本地执行脚本

### 本地执行要求
```bash
# 确保本地已安装 Python 3.6+
python --version

# 安装依赖 (MySQL)
pip install pandas numpy pymysql

# 安装依赖 (PostgreSQL)  
pip install pandas numpy psycopg2-binary

# 运行生成的脚本
python umami_import.py
```

### 🔄 工作流程
1. **在线配置**: 在 Cloudflare Pages 上填写数据库配置
2. **脚本生成**: JavaScript 在浏览器中生成 Python 脚本
3. **本地下载**: 将生成的脚本下载到本地计算机
4. **本地执行**: 在本地 Python 环境中运行脚本进行数据导入

## 🌟 核心特性

### 数据库支持
- **MySQL**: 完整的 pymysql 支持
- **PostgreSQL**: psycopg2 驱动支持
- **自动配置**: 根据数据库类型自动调整连接参数

### 数据处理
- **智能编码检测**: 支持 UTF-8 和 GBK 编码
- **批量处理**: 可配置批处理大小优化性能
- **数据验证**: 导入前后数据验证
- **错误处理**: 完善的异常处理机制

### 用户体验
- **响应式设计**: 适配各种设备屏幕
- **实时反馈**: 进度条和状态更新
- **直观界面**: 现代化的用户界面设计
- **中文支持**: 完全中文化界面

## 🔧 部署说明

### Cloudflare Pages 部署
1. 将项目文件上传到 Git 仓库
2. 在 Cloudflare Pages 中连接仓库
3. 配置构建设置:
   - 构建命令: (无需构建)
   - 输出目录: `/`
4. 部署完成后即可访问

### 本地开发
```bash
# 使用简单的 HTTP 服务器
python -m http.server 8000
# 或
npx serve .
```

## 📝 更新日志

### v2.0.0 (最新版本)
- ✅ 新增高级配置页面
- ✅ 完整的数据库支持 (MySQL/PostgreSQL)
- ✅ Python 脚本自动生成
- ✅ 系统状态监控页面
- ✅ 响应式界面优化
- ✅ 实时日志和状态更新

### v1.0.0
- ✅ 基础 CSV 上传功能
- ✅ SQL 生成演示
- ✅ Cloudflare Pages 部署

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📄 许可证

本项目采用 MIT 许可证。

## 🔗 相关链接

- [Umami 官网](https://umami.is/)
- [Cloudflare Pages](https://pages.cloudflare.com/)
- [项目演示](#) (请替换为实际部署地址)

---

⚡ **提示**: 这是一个完全基于静态页面的解决方案，所有数据处理都在客户端完成，确保数据安全性。生成的 Python 脚本需要在您的本地环境中执行。
