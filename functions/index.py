def on_request(context):
    """Cloudflare Pages主页函数"""
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Umami CSV导入工具</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 30px;
        }
        .header h1 { 
            color: #2c3e50; 
            margin: 0;
            font-size: 2.5em;
            font-weight: 700;
        }
        .header p { 
            color: #7f8c8d; 
            margin: 10px 0 0 0;
            font-size: 1.2em;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            border-left: 4px solid #3498db;
            transition: all 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        .feature-card h3 {
            color: #2c3e50;
            margin-top: 0;
            font-size: 1.3em;
        }
        .feature-card p {
            color: #5a6c7d;
            line-height: 1.6;
        }
        .nav-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 40px;
            flex-wrap: wrap;
        }
        .nav-link {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-block;
        }
        .nav-link:hover {
            background: linear-gradient(45deg, #2980b9, #1c6ea4);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        .info-section {
            background: #ecf0f1;
            padding: 25px;
            border-radius: 10px;
            margin: 30px 0;
        }
        .info-section h3 {
            color: #2c3e50;
            margin-top: 0;
        }
        .info-section ul {
            color: #5a6c7d;
            line-height: 1.8;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid #ecf0f1;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍜 Umami CSV导入工具</h1>
            <p>轻松将CSV数据导入到Umami分析平台</p>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <h3>📊 CSV数据解析</h3>
                <p>智能解析CSV文件，自动识别字段类型和格式，支持多种编码格式。</p>
            </div>
            <div class="feature-card">
                <h3>🔄 数据转换</h3>
                <p>将CSV数据转换为Umami兼容的SQL格式，确保数据完整性和准确性。</p>
            </div>
            <div class="feature-card">
                <h3>🚀 一键导入</h3>
                <p>生成标准化的SQL语句，可直接在Umami数据库中执行导入。</p>
            </div>
        </div>
        
        <div class="info-section">
            <h3>🎯 支持的功能</h3>
            <ul>
                <li>多种CSV格式支持（UTF-8, GBK等编码）</li>
                <li>智能字段映射和类型识别</li>
                <li>数据验证和清洗</li>
                <li>SQL语句生成和预览</li>
                <li>批量数据处理</li>
            </ul>
        </div>
        
        <div class="nav-links">
            <a href="/functions/upload" class="nav-link">📤 开始上传</a>
            <a href="/functions/status" class="nav-link">📊 查看状态</a>
        </div>
        
        <div class="footer">
            <p>Powered by Cloudflare Pages | 部署在边缘计算网络</p>
        </div>
    </div>
</body>
</html>"""
    
    return html
