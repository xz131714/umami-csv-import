#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Umami CSV 数据导入工具 - Web版本
基于Flask的Web应用程序，提供友好的用户界面
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import pandas as pd
import os
import json
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime
import sys
import traceback

# 导入数据库连接模块
try:
    import pymysql
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    # 如果没有安装数据库驱动，继续运行但功能受限
    pass

app = Flask(__name__)
app.secret_key = 'umami-csv-import-tool-2024'  # 在生产环境中请更改此密钥
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB最大文件大小

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'csv', 'txt'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_mysql_connection(host, port, user, password, database):
    """创建MySQL连接"""
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def create_postgres_connection(host, port, user, password, database):
    """创建PostgreSQL连接"""
    return psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursor_factory=RealDictCursor
    )

def get_table_columns(connection, table_name, db_type):
    """获取表的列名"""
    cursor = connection.cursor()
    
    if db_type == 'mysql':
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [row['Field'] for row in cursor.fetchall()]
    elif db_type == 'postgresql':
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        columns = [row['column_name'] for row in cursor.fetchall()]
    
    cursor.close()
    return columns

def clean_dataframe_for_db(df):
    """清理DataFrame以适合数据库插入"""
    # 处理NaN值
    df = df.fillna('')
    
    # 确保字符串列不会太长
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str[:255]
    
    return df

def insert_data_batch(connection, table_name, df, db_type):
    """批量插入数据"""
    if df.empty:
        return 0
    
    cursor = connection.cursor()
    
    # 构建插入语句
    columns = list(df.columns)
    placeholders = ', '.join(['%s'] * len(columns))
    column_names = ', '.join(columns)
    
    sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    
    # 转换数据为元组列表
    data = [tuple(row) for row in df.to_numpy()]
    
    # 批量插入
    cursor.executemany(sql, data)
    connection.commit()
    
    rows_inserted = cursor.rowcount
    cursor.close()
    return rows_inserted

def truncate_tables(connection, db_type):
    """清空数据表"""
    cursor = connection.cursor()
    
    tables = ['website_event', 'session', 'website']
    
    try:
        # 禁用外键检查
        if db_type == 'mysql':
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 清空表
        for table in tables:
            if db_type == 'mysql':
                cursor.execute(f"TRUNCATE TABLE {table}")
            elif db_type == 'postgresql':
                cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
        
        # 重新启用外键检查
        if db_type == 'mysql':
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        connection.commit()
        
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/config')
def config():
    """数据库配置页面"""
    return render_template('config.html')

@app.route('/test_connection', methods=['POST'])
def test_connection():
    """测试数据库连接"""
    try:
        data = request.get_json()
        
        # 创建数据库连接
        if data['db_type'] == 'mysql':
            connection = create_mysql_connection(
                host=data['host'],
                port=int(data['port']),
                user=data['username'],
                password=data['password'],
                database=data['database']
            )
        elif data['db_type'] == 'postgresql':
            connection = create_postgres_connection(
                host=data['host'],
                port=int(data['port']),
                user=data['username'],
                password=data['password'],
                database=data['database']
            )
        else:
            return jsonify({'success': False, 'error': '不支持的数据库类型'})
        
        # 测试连接
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'message': '数据库连接成功'})
        
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
    """文件上传页面"""
    if request.method == 'POST':
        # 检查数据库配置
        db_config = session.get('db_config')
        if not db_config:
            flash('请先配置数据库连接信息', 'warning')
            return redirect(url_for('config'))
        
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
        # 从session获取数据库配置
        db_config = session.get('db_config')
        if not db_config:
            return jsonify({
                'success': False,
                'error': '请先配置数据库连接'
            })
        
        data = request.get_json()
        
        # 获取上传的文件信息
        file_path = data.get('file_path')
        if not file_path or not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': '文件不存在或已过期'
            })
        
        # 创建数据库连接
        if db_config['db_type'] == 'mysql':
            connection = create_mysql_connection(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['username'],
                password=db_config['password'],
                database=db_config['database']
            )
        elif db_config['db_type'] == 'postgresql':
            connection = create_postgres_connection(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['username'],
                password=db_config['password'],
                database=db_config['database']
            )
        else:
            return jsonify({
                'success': False,
                'error': '不支持的数据库类型'
            })
        
        # 如果需要清空数据表
        if db_config.get('clear_tables', False):
            truncate_tables(connection, db_config['db_type'])
        
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 数据处理和导入
        tables = ['website_event', 'session']  # 根据需要调整
        total_imported = 0
        
        for table in tables:
            if table in df.columns or f'{table}_' in str(df.columns):
                # 根据表名过滤相关列
                table_columns = get_table_columns(connection, table, db_config['db_type'])
                
                # 这里需要根据实际的CSV结构来映射数据
                # 简化版本：假设CSV列名与数据库列名匹配
                table_df = df[df.columns.intersection(table_columns)]
                
                if not table_df.empty:
                    # 分批处理大文件
                    batch_size = 1000
                    for i in range(0, len(table_df), batch_size):
                        batch_df = table_df.iloc[i:i + batch_size]
                        cleaned_df = clean_dataframe_for_db(batch_df)
                        
                        # 插入数据
                        rows_inserted = insert_data_batch(connection, table, cleaned_df, db_config['db_type'])
                        total_imported += rows_inserted
        
        connection.close()
        
        # 清理临时文件
        try:
            os.remove(file_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'message': f'数据导入完成！共导入 {total_imported} 条记录。',
            'imported_count': total_imported
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'导入失败: {str(e)}',
            'details': traceback.format_exc()
        })
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
