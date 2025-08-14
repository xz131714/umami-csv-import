# 轻量级版本 - 适合Vercel等Serverless平台
# 不使用pandas/numpy，使用标准库处理CSV

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import csv
import os
import json
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime
import sys
import io

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'umami-csv-import-tool-2024-vercel-dev')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB for serverless

ALLOWED_EXTENSIONS = {'csv', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config')
def config():
    """数据库配置页面"""
    return render_template('config.html')

@app.route('/test_connection', methods=['POST'])
def test_connection():
    """模拟测试数据库连接 - 轻量版只做基本验证"""
    try:
        data = request.get_json()
        
        # 基本参数验证
        required_fields = ['db_type', 'host', 'port', 'username', 'password', 'database']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'缺少必需参数: {field}'})
        
        # 轻量版不进行实际连接测试，只做格式验证
        if data['db_type'] not in ['mysql', 'postgresql']:
            return jsonify({'success': False, 'error': '不支持的数据库类型'})
        
        port = int(data['port'])
        if port < 1 or port > 65535:
            return jsonify({'success': False, 'error': '端口号无效'})
        
        return jsonify({'success': True, 'message': '配置验证通过（轻量版不进行实际连接测试）'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/save_db_config', methods=['POST'])
def save_db_config():
    """保存数据库配置"""
    try:
        # 获取表单数据
        config = {
            'db_type': request.form.get('db_type'),
            'host': request.form.get('host'),
            'port': int(request.form.get('port')),
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'database': request.form.get('database'),
            'website_id': request.form.get('website_id'),
            'clear_tables': bool(request.form.get('clear_tables'))
        }
        
        # 验证配置
        if not all([config['host'], config['username'], config['password'], config['database'], config['website_id']]):
            flash('请填写所有必需的配置信息', 'error')
            return redirect(url_for('config'))
        
        # 保存到session
        session['db_config'] = config
        flash('数据库配置保存成功！', 'success')
        
        return redirect(url_for('upload_file'))
        
    except Exception as e:
        flash(f'保存配置失败: {str(e)}', 'error')
        return redirect(url_for('config'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查数据库配置
        db_config = session.get('db_config')
        if not db_config:
            flash('请先配置数据库连接信息', 'warning')
            return redirect(url_for('config'))
        
        if 'file' not in request.files:
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            try:
                # 读取CSV文件内容到内存
                file_content = file.read().decode('utf-8')
                csv_reader = csv.DictReader(io.StringIO(file_content))
                
                # 获取列名
                columns = csv_reader.fieldnames or []
                
                # 读取前5行作为样本
                sample_data = []
                for i, row in enumerate(csv_reader):
                    if i >= 5:
                        break
                    sample_data.append(row)
                
                file_info = {
                    'filename': filename,
                    'file_content': file_content,  # 存储在内存中
                    'columns': columns,
                    'sample_data': sample_data,
                    'upload_time': datetime.now().isoformat()
                }
                
                return render_template('preview_lite.html', file_info=file_info)
                
            except Exception as e:
                flash(f'读取CSV文件失败: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('不支持的文件类型，请上传CSV文件', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/import-lite', methods=['POST'])
def import_lite():
    """简化版数据导入 - 仅生成SQL语句"""
    try:
        data = request.get_json()
        file_content = data.get('file_content')
        website_id = data.get('website_id')
        db_type = data.get('db_type', 'mysql')
        
        if not file_content or not website_id:
            return jsonify({'success': False, 'message': '缺少必要参数'})
        
        # 解析CSV
        csv_reader = csv.DictReader(io.StringIO(file_content))
        
        sql_statements = []
        session_count = 0
        event_count = 0
        
        # 定义表字段映射
        session_fields = ['session_id', 'website_id', 'hostname', 'browser', 'os', 'device', 'screen', 'language', 'country', 'created_at']
        event_fields = ['session_id', 'website_id', 'url_path', 'url_query', 'referrer_path', 'referrer_query', 'referrer_domain', 'page_title', 'event_type', 'event_name', 'created_at']
        
        for row in csv_reader:
            # 替换website_id
            row['website_id'] = website_id
            
            # 生成session表SQL
            session_data = {k: row.get(k, '') for k in session_fields if k in row}
            if session_data:
                if db_type == 'mysql':
                    sql = generate_mysql_insert('session', session_data)
                else:
                    sql = generate_postgres_insert('session', session_data)
                sql_statements.append(sql)
                session_count += 1
            
            # 生成website_event表SQL
            event_data = {k: row.get(k, '') for k in event_fields if k in row}
            if event_data:
                if db_type == 'mysql':
                    sql = generate_mysql_insert('website_event', event_data)
                else:
                    sql = generate_postgres_insert('website_event', event_data)
                sql_statements.append(sql)
                event_count += 1
        
        return jsonify({
            'success': True,
            'message': f'SQL语句生成完成',
            'sql_statements': sql_statements,
            'stats': {
                'session_count': session_count,
                'event_count': event_count,
                'total_statements': len(sql_statements)
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'})

def generate_mysql_insert(table, data):
    """生成MySQL INSERT语句"""
    columns = ', '.join([f"`{k}`" for k in data.keys()])
    values = ', '.join([f"'{v}'" if v else 'NULL' for v in data.values()])
    return f"INSERT IGNORE INTO `{table}` ({columns}) VALUES ({values});"

def generate_postgres_insert(table, data):
    """生成PostgreSQL INSERT语句"""
    columns = ', '.join([f'"{k}"' for k in data.keys()])
    values = ', '.join([f"'{v}'" if v else 'NULL' for v in data.values()])
    return f'INSERT INTO "{table}" ({columns}) VALUES ({values}) ON CONFLICT DO NOTHING;'

if __name__ == '__main__':
    app.run(debug=True)

# Vercel entry point
application = app
