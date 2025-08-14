# 轻量级版本 - 适合Vercel等Serverless平台
# 不使用pandas/numpy，使用标准库处理CSV

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import csv
import os
import json
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime
import sys
import io

app = Flask(__name__)
app.secret_key = 'umami-csv-import-tool-2024'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB for serverless

ALLOWED_EXTENSIONS = {'csv', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
