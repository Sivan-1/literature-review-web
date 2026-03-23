import requests
import time

def call_deepseek_api(prompt, api_key, max_retries=3):
    """
    调用 DeepSeek API 生成文献综述
    
    Args:
        prompt: 构建好的提示词
        api_key: DeepSeek API Key
        max_retries: 最大重试次数
        
    Returns:
        str: 生成的文献综述内容
    """
    api_url = "https://api.deepseek.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",  # 或使用其他可用模型
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的学术研究助理，擅长撰写高质量的文献综述。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            literature_review = result['choices'][0]['message']['content']
            
            return literature_review.strip()
            
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                raise Exception("API 调用超时，请稍后重试")
            time.sleep(2 ** attempt)  # 指数退避
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise Exception(f"API 调用失败: {str(e)}")
            time.sleep(2 ** attempt)