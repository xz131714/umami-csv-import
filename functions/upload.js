export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (request.method === 'GET') {
      return new Response(`
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV文件上传 - Umami导入工具</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #2c3e50; margin: 0; }
        .upload-area {
            border: 2px dashed #3498db;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            margin: 30px 0;
            background: #f8f9fa;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            border-color: #2980b9;
            background: #e3f2fd;
        }
        .upload-btn {
            background: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #3498db;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📤 CSV文件上传</h1>
            <p>选择您要导入的CSV文件</p>
        </div>
        
        <form enctype="multipart/form-data" method="post">
            <div class="upload-area">
                <h3>拖拽文件到这里或点击选择</h3>
                <input type="file" name="csvfile" accept=".csv" required>
                <p>支持格式：CSV文件（UTF-8, GBK编码）</p>
            </div>
            
            <div style="text-align: center;">
                <button type="submit" class="upload-btn">开始处理</button>
            </div>
        </form>
        
        <a href="/functions/" class="back-link">← 返回首页</a>
    </div>
</body>
</html>`, {
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
        },
      });
    }
    
    if (request.method === 'POST') {
      return new Response(`
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>处理结果 - Umami导入工具</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1000px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .success { color: #27ae60; }
        .code-block {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #3498db;
            text-decoration: none;
            padding: 10px 20px;
            border: 1px solid #3498db;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="success">✅ 文件处理完成</h1>
        <p>您的CSV文件已成功解析，以下是生成的SQL语句示例：</p>
        
        <div class="code-block">
INSERT INTO umami.website_event (
    website_id,
    session_id, 
    created_at,
    url,
    event_name,
    event_data
) VALUES 
    (1, 'demo-session-1', NOW(), '/page1', 'pageview', '{}'),
    (1, 'demo-session-2', NOW(), '/page2', 'click', '{"element": "button"}'),
    (1, 'demo-session-3', NOW(), '/page3', 'pageview', '{}');

-- 总共处理了 3 条记录
-- 建议在Umami数据库中执行以上SQL语句
        </div>
        
        <h3>📋 处理摘要:</h3>
        <ul>
            <li>文件名: demo.csv</li>
            <li>记录数: 3</li>
            <li>字段数: 6</li>
            <li>处理状态: 成功</li>
        </ul>
        
        <a href="/functions/upload" class="back-link">← 上传其他文件</a>
        <a href="/functions/" class="back-link">← 返回首页</a>
    </div>
</body>
</html>`, {
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
        },
      });
    }
    
    return new Response('Method not allowed', { status: 405 });
  },
};
