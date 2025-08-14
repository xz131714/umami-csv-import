# Umami CSV 数据导入工具

一个功能完整的Umami数据库CSV导入工具，提供多种部署方式和用户界面。

## ⚡ 快速开始 - 云端部署

无需本地环境，直接通过GitHub部署到云平台：

### 🚀 一键部署

| 平台 | 版本 | 特点 | 部署 |
|------|------|------|------|
| **Vercel** | 轻量版 | 免费、快速、SQL生成 | [![Deploy](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/xz131714/umami-csv-import) |
| **Railway** | 完整版 | 免费试用、直连数据库 | [![Deploy](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/xz131714/umami-csv-import) |
| **Render** | 完整版 | 免费永久、自动SSL | [![Deploy](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/xz131714/umami-csv-import) |

### 📋 部署步骤
1. **Fork此项目** 到您的GitHub账号
2. **选择平台** 点击上方部署按钮
3. **连接GitHub** 授权访问您的仓库
4. **自动部署** 几分钟即可完成

## � 项目结构

```
├── 📁 .github/                # GitHub配置和模板
├── 📄 CLOUD_DEPLOY.md         # 详细云端部署指南
├── 📄 README.md               # 项目说明
├── 🌐 status.html             # 部署状态监控页面
└── 📁 web-app/                # Web应用核心文件
    ├── app.py                 # 完整版Flask应用 (Railway/Render)
    ├── app_lite.py            # 轻量版应用 (Vercel/Cloudflare)
    ├── requirements.txt       # 完整版依赖
    ├── requirements_lite.txt  # 轻量版依赖
    ├── vercel.json           # Vercel配置
    ├── railway.toml          # Railway配置
    ├── render.yaml           # Render配置
    ├── static/               # CSS/JS静态资源
    └── templates/            # HTML模板
```

## 📚 文档说明

- 📖 **[CLOUD_DEPLOY.md](CLOUD_DEPLOY.md)** - 详细的云端部署指南
- 🌐 **[status.html](status.html)** - 部署状态监控页面
- 🛠️ **[web-app/README.md](web-app/README.md)** - Web应用技术说明

## � 项目统计

- 📝 **总文件数**: 25个核心文件
- 🌐 **支持平台**: 4个主流云平台
- 🎯 **部署方式**: 2种版本（完整版/轻量版）
- ⚡ **部署时间**: 3-5分钟
- 💰 **部署成本**: 完全免费

## 📊 功能特点

### 命令行版本
- ✅ 支持MySQL和PostgreSQL数据库
- ✅ 智能数据清洗和验证
- ✅ 批量导入，支持大文件
- ✅ 重复数据检测和跳过
- ✅ 详细的进度显示和统计
- ✅ 可配置的Website ID替换

### Web版本
- 🌐 直观的Web用户界面
- 📁 拖拽上传CSV文件（最大50MB）
- 🔍 数据预览和结构分析
- ⚡ 实时导入进度显示
- 🔧 可视化数据库配置
- 📱 响应式设计，支持移动设备
- 🛡️ 安全的文件处理和验证

## 📋 CSV文件格式要求

您的CSV文件应包含以下字段（部分或全部）：

**Session表相关字段：**
- `session_id` - 会话ID
- `website_id` - 网站ID（将被替换）
- `hostname` - 主机名
- `browser` - 浏览器
- `os` - 操作系统
- `device` - 设备类型
- `screen` - 屏幕分辨率
- `language` - 语言
- `country` - 国家
- `created_at` - 创建时间

**Website Event表相关字段：**
- `session_id` - 会话ID
- `website_id` - 网站ID（将被替换）
- `url_path` - URL路径
- `url_query` - URL查询参数
- `referrer_path` - 来源路径
- `referrer_query` - 来源查询参数
- `referrer_domain` - 来源域名
- `page_title` - 页面标题
- `event_type` - 事件类型
- `event_name` - 事件名称
- `created_at` - 创建时间

## 🔧 配置说明

### 数据库配置

编辑`umami_universal_import.py`中的配置：

```python
# MySQL配置
MYSQL_CONFIG = {
    'host': 'your-mysql-host.com',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password',
    'database': 'umami'
}

# PostgreSQL配置
POSTGRES_CONFIG = {
    'host': 'your-postgres-host.com',
    'port': 5432,
    'database': 'database',
    'user': 'user',
    'password': 'password',
    'sslmode': 'require'
}
```

### 文件配置

```python
CSV_FILE_PATH = 'file.csv'  # CSV文件路径
REPLACEMENT_WEBSITE_ID = '01923022-a812-4369-b896-862fa37d32b1'  # 目标website_id
```

## 📈 使用统计

导入完成后，工具会显示：
- 处理的总行数
- 成功插入的行数
- 跳过的重复数据行数
- 数据去重率
- 各表的导入统计

## 🛡️ 安全注意事项

1. **数据库凭据**：不要在代码中硬编码密码，使用环境变量
2. **文件安全**：上传的文件会被临时存储，定期清理
3. **输入验证**：所有用户输入都会被验证和清理
4. **备份数据**：导入前建议备份原始数据库

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查网络连接
   - 验证数据库凭据
   - 确认数据库服务运行状态

2. **CSV文件读取错误**
   - 检查文件编码（建议UTF-8）
   - 验证CSV格式
   - 确认文件权限

3. **导入数据为空**
   - 检查CSV列名是否与数据库表字段匹配
   - 验证数据类型兼容性
   - 查看日志文件获取详细错误信息

### 获取帮助

- 查看 `output.log` 文件获取详细日志
- 检查控制台输出的错误信息
- 在GitHub Issues中报告问题

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

### 开发环境设置

1. Fork并克隆仓库
2. 创建虚拟环境
3. 安装开发依赖
4. 运行测试
5. 提交Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- GitHub Issues: [报告问题](https://github.com/your-username/umami-csv-import/issues)
- 邮箱: your-email@example.com

---

⭐ 如果这个项目对您有帮助，请给它一个star！
