"""
utils 包 - 工具函数模块
"""

from .pdf_extractor import extract_pdf_text
from .prompt_builder import build_prompt
from .api_client import call_deepseek_api
from .pdf_generator import generate_pdf

# 定义 __all__ 指定导出的函数
__all__ = [
    'extract_pdf_text',
    'build_prompt', 
    'call_deepseek_api',
    'generate_pdf'
]

# 打印确认信息（调试用）
print("✅ utils 模块加载成功")
print(f"   - extract_pdf_text: {extract_pdf_text.__name__ if callable(extract_pdf_text) else 'not callable'}")
print(f"   - build_prompt: {build_prompt.__name__ if callable(build_prompt) else 'not callable'}")
print(f"   - call_deepseek_api: {call_deepseek_api.__name__ if callable(call_deepseek_api) else 'not callable'}")
print(f"   - generate_pdf: {generate_pdf.__name__ if callable(generate_pdf) else 'not callable'}")