#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Umami CSV 数据导入工具 - Web版本
基于Flask的Web应用程序，提供友好的用户界面
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import pandas as pd
import os
import json
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime
import sys

# 导入原始的数据库连接和处理函数
sys.path.append('..')
from umami_universal_import import (
    connect_to_mysql, connect_to_postgres, clean_dataframe_for_db,
    get_table_columns, insert_data_batch, truncate_tables
)

app = Flask(__name__)
app.secret_key = 'umami-csv-import-tool-2024'  # 在生产环境中请更改此密钥
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB最大文件大小

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'csv', 'txt'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """文件上传页面"""
    if request.method == 'POST':
        # 检查是否有文件被上传
        if 'file' not in request.files:
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # 检查文件名
        if file.filename == '':
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # 保存文件到临时目录
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, filename)
            file.save(file_path)
            
            try:
                # 读取CSV文件预览
                df = pd.read_csv(file_path, nrows=5)  # 只读取前5行用于预览
                
                # 获取文件信息
                file_info = {
                    'filename': filename,
                    'filepath': file_path,
                    'columns': list(df.columns),
                    'sample_data': df.to_dict('records'),
                    'upload_time': datetime.now().isoformat()
                }
                
                # 保存文件信息到session（在实际应用中可能需要使用数据库）
                return render_template('preview.html', file_info=file_info)
                
            except Exception as e:
                flash(f'读取CSV文件失败: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('不支持的文件类型，请上传CSV文件', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/configure', methods=['POST'])
def configure_import():
    """配置导入参数"""
    try:
        data = request.get_json()
        
        # 获取配置参数
        db_type = data.get('db_type')
        db_config = data.get('db_config')
        website_id = data.get('website_id')
        clear_tables = data.get('clear_tables', False)
        file_path = data.get('file_path')
        
        # 验证必需参数
        if not all([db_type, db_config, website_id, file_path]):
            return jsonify({'success': False, 'message': '缺少必需的配置参数'})
        
        # 保存配置（在实际应用中应该使用更安全的存储方式）
        config = {
            'db_type': db_type,
            'db_config': db_config,
            'website_id': website_id,
            'clear_tables': clear_tables,
            'file_path': file_path,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({'success': True, 'config': config})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'配置保存失败: {str(e)}'})

@app.route('/import', methods=['POST'])
def start_import():
    """开始数据导入"""
    try:
        data = request.get_json()
        config = data.get('config')
        
        if not config:
            return jsonify({'success': False, 'message': '缺少导入配置'})
        
        # 连接数据库
        connection = None
        if config['db_type'] == 'mysql':
            connection = connect_to_mysql_with_config(config['db_config'])
        elif config['db_type'] == 'postgres':
            connection = connect_to_postgres_with_config(config['db_config'])
        
        if not connection:
            return jsonify({'success': False, 'message': '数据库连接失败'})
        
        try:
            # 读取CSV文件
            df = pd.read_csv(config['file_path'])
            
            # 替换website_id
            if 'website_id' in df.columns:
                df['website_id'] = config['website_id']
            
            # 清空表（如果需要）
            if config['clear_tables']:
                truncate_tables(connection, config['db_type'])
            
            # 导入数据
            results = {}
            target_tables = ['session', 'website_event']
            
            for table in target_tables:
                try:
                    # 获取表结构
                    table_columns = get_table_columns(connection, table, config['db_type'])
                    
                    # 匹配列
                    common_columns = [col for col in table_columns if col in df.columns]
                    
                    if common_columns:
                        sub_df = df[common_columns].copy()
                        if 'website_id' in sub_df.columns:
                            sub_df['website_id'] = config['website_id']
                        
                        # 清洗数据
                        cleaned_df = clean_dataframe_for_db(sub_df)
                        
                        # 插入数据
                        insert_data_batch(connection, table, cleaned_df, config['db_type'])
                        
                        results[table] = {
                            'success': True,
                            'processed_rows': len(cleaned_df),
                            'columns': common_columns
                        }
                    else:
                        results[table] = {
                            'success': False,
                            'message': '没有匹配的列'
                        }
                        
                except Exception as e:
                    results[table] = {
                        'success': False,
                        'message': str(e)
                    }
            
            return jsonify({
                'success': True,
                'message': '数据导入完成',
                'results': results
            })
            
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'导入过程出错: {str(e)}'})

def connect_to_mysql_with_config(config):
    """使用配置连接MySQL"""
    try:
        import pymysql
        connection = pymysql.connect(**config)
        return connection
    except Exception as e:
        print(f"MySQL连接失败: {e}")
        return None

def connect_to_postgres_with_config(config):
    """使用配置连接PostgreSQL"""
    try:
        import psycopg2
        connection = psycopg2.connect(**config)
        return connection
    except Exception as e:
        print(f"PostgreSQL连接失败: {e}")
        return None

@app.route('/test-db', methods=['POST'])
def test_database_connection():
    """测试数据库连接"""
    try:
        data = request.get_json()
        db_type = data.get('db_type')
        db_config = data.get('db_config')
        
        connection = None
        if db_type == 'mysql':
            connection = connect_to_mysql_with_config(db_config)
        elif db_type == 'postgres':
            connection = connect_to_postgres_with_config(db_config)
        
        if connection:
            connection.close()
            return jsonify({'success': True, 'message': '数据库连接成功'})
        else:
            return jsonify({'success': False, 'message': '数据库连接失败'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'连接测试失败: {str(e)}'})

@app.errorhandler(413)
def too_large(e):
    """文件过大错误处理"""
    flash('文件过大，请上传小于50MB的文件', 'error')
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    # 开发环境运行
    app.run(debug=True, host='0.0.0.0', port=5000)
