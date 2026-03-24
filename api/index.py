"""
Vercel Serverless Function 入口
"""
from flask import Flask, request, jsonify, render_template_string
import os
import sys
import uuid
import tempfile
from werkzeug.utils import secure_filename

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 创建 Flask 应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vercel-deploy-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

# 导入工具函数
try:
    from utils.pdf_extractor import extract_pdf_text
    from utils.prompt_builder import build_prompt
    from utils.api_client import call_deepseek_api
    from utils.pdf_generator import generate_pdf
    print("✅ 工具函数导入成功")
except Exception as e:
    print(f"⚠️ 工具函数导入失败: {e}")

# HTML 模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文献综述自动生成系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 50px 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .card-header h1 { font-size: 28px; margin-bottom: 10px; }
        .card-body { padding: 40px; }
        .form-group { margin-bottom: 25px; }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        input[type="text"], input[type="password"], input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .file-list { margin-top: 15px; }
        .file-item {
            background: #f8f9fa;
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
        }
        .alert {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .alert-error { background: #fee; color: #c33; border: 1px solid #fcc; }
        .alert-success { background: #efe; color: #3a3; border: 1px solid #cfc; }
        .loader {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .text-center { text-align: center; }
        .small { font-size: 12px; color: #666; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <h1>📚 文献综述自动生成系统</h1>
                <p>基于 DeepSeek AI 的智能文献分析工具</p>
            </div>
            <div class="card-body">
                {% if error %}
                <div class="alert alert-error">{{ error }}</div>
                {% endif %}
                {% if success %}
                <div class="alert alert-success">{{ success }}</div>
                {% endif %}
                
                <form id="uploadForm" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label>🔬 研究主题</label>
                        <input type="text" name="research_topic" placeholder="例如：人工智能在医疗诊断中的应用" required>
                    </div>
                    
                    <div class="form-group">
                        <label>🔑 DeepSeek API Key</label>
                        <input type="password" name="api_key" placeholder="请输入您的 DeepSeek API Key" required>
                        <div class="small">您的 API Key 仅用于本次请求，不会被存储</div>
                    </div>
                    
                    <div class="form-group">
                        <label>📄 上传 PDF 文献</label>
                        <input type="file" name="pdf_files" accept=".pdf" multiple required onchange="updateFileList(this)">
                        <div id="fileList" class="file-list"></div>
                    </div>
                    
                    <div id="loading" style="display: none;">
                        <div class="loader"></div>
                        <div class="text-center">正在生成文献综述，请稍候...（可能需要 1-2 分钟）</div>
                    </div>
                    
                    <button type="submit" id="submitBtn">🚀 开始生成文献综述</button>
                </form>
                
                <div class="text-center small" style="margin-top: 20px;">
                    ✅ 系统运行正常 | Vercel 部署成功
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function updateFileList(input) {
            const fileList = document.getElementById('fileList');
            fileList.innerHTML = '';
            const files = Array.from(input.files);
            files.forEach(file => {
                const div = document.createElement('div');
                div.className = 'file-item';
                div.innerHTML = `<span>📄 ${file.name}</span><span>${(file.size / 1024).toFixed(2)} KB</span>`;
                fileList.appendChild(div);
            });
        }
        
        document.getElementById('uploadForm').addEventListener('submit', function() {
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            document.getElementById('submitBtn').innerHTML = '⏳ 处理中，请稍候...';
        });
    </script>
</body>
</html>
'''

# 结果模板
RESULT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生成成功 - 文献综述系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 50px 20px;
        }
        .container { max-width: 600px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            padding: 50px;
        }
        .success-icon { font-size: 80px; color: #28a745; margin-bottom: 20px; }
        h2 { color: #333; margin-bottom: 20px; }
        .info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            color: #666;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            margin: 10px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .btn-download {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-home {
            background: #6c757d;
            color: white;
        }
        .btn:hover { transform: translateY(-2px); }
        .small { font-size: 12px; color: #999; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="success-icon">✅</div>
            <h2>文献综述已成功生成！</h2>
            <div class="info">
                <strong>研究主题：</strong>{{ research_topic }}
            </div>
            <div>
                <a href="{{ download_url }}" class="btn btn-download">
                    📥 下载 PDF 报告
                </a>
                <a href="/" class="btn btn-home">
                    🏠 返回首页
                </a>
            </div>
            <div class="small">提示：下载链接将在本次会话中有效，建议立即保存文件</div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        research_topic = request.form.get('research_topic', '').strip()
        api_key = request.form.get('api_key', '').strip()
        files = request.files.getlist('pdf_files')
        
        if not research_topic:
            return render_template_string(HTML_TEMPLATE, error='请输入研究主题')
        
        if not api_key:
            return render_template_string(HTML_TEMPLATE, error='请输入 DeepSeek API Key')
        
        if not files or files[0].filename == '':
            return render_template_string(HTML_TEMPLATE, error='请上传至少一个 PDF 文件')
        
        # 这里处理 PDF 生成逻辑
        # 由于 Vercel 有执行时间限制（10秒），复杂处理建议用外部服务
        
        return render_template_string(HTML_TEMPLATE, success=f'收到请求！主题：{research_topic}，文件数：{len(files)}')
    
    return render_template_string(HTML_TEMPLATE)

# Vercel 需要导出的 handler
app.debug = False

# 导出 application 供 Vercel 使用
application = app