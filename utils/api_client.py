"""
DeepSeek API 客户端 - 强化学术格式
"""
import requests
import time
import re

def clean_api_response(text):
    """清理 API 返回的文本，保持格式"""
    if not text:
        return ""
    
    # 只移除 Markdown 粗体斜体标记
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    
    # 移除单独的 # 号（但不是中文标题的编号）
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # 移除行首的 # 号（但保留中文编号）
        if line.strip().startswith('#') and not line.strip().startswith(('一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、')):
            line = re.sub(r'^#+\s*', '', line)
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # 确保标题格式正确
    text = re.sub(r'^([一二三四五六七八九十]+、)', r'\n\1', text, flags=re.MULTILINE)
    
    return text.strip()

def call_deepseek_api(prompt, api_key, max_retries=3):
    """
    调用 DeepSeek API 生成文献综述
    """
    api_url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": """你是一位资深的学术研究专家，专门从事文献综述撰写工作。

【输出格式规范】
你必须严格遵守以下格式要求：

1. 使用中文数字编号的标题：一、二、三、四、五、六、七、八、
2. 每个标题单独占一行，后面紧跟内容
3. 段落之间用空行分隔
4. 参考文献使用[1]、[2]等编号，每条单独占一行
5. 禁止使用任何Markdown格式（不要用**、*、#、>等符号）
6. 输出纯文本，保持清晰的结构

【正确格式示例】
一、研究背景与意义
（这里是内容段落）

二、国内外研究现状
（这里是内容段落）

八、参考文献
[1] 作者. 文章标题[J]. 期刊名称, 年份, 卷(期): 页码.
[2] Author. Article Title[J]. Journal Name, Year, Volume(Issue): Pages.

请严格按照此格式输出。"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
        "stream": False
    }
    
    for attempt in range(max_retries):
        try:
            print(f"调用 API... (尝试 {attempt + 1}/{max_retries})")
            response = requests.post(api_url, headers=headers, json=data, timeout=90)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # 清理内容
                content = clean_api_response(content)
                
                print(f"✅ API 调用成功，返回内容长度: {len(content)} 字符")
                return content.strip()
                
            else:
                print(f"API 错误: {response.status_code}")
                if attempt == max_retries - 1:
                    raise Exception(f"API 调用失败: {response.text}")
                time.sleep(2 ** attempt)
                
        except requests.exceptions.Timeout:
            print(f"请求超时 (尝试 {attempt + 1})")
            if attempt == max_retries - 1:
                raise Exception("API 调用超时")
            time.sleep(2 ** attempt)
            
        except Exception as e:
            print(f"错误: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)