import pdfplumber
import io
from pathlib import Path

def extract_pdf_text(file_path_or_bytes):
    """
    从 PDF 文件提取文本
    支持文件路径或字节流
    
    Args:
        file_path_or_bytes: PDF 文件路径或字节流对象
        
    Returns:
        str: 提取的文本内容
    """
    try:
        text = ""
        
        # 判断输入类型
        if isinstance(file_path_or_bytes, (str, Path)):
            # 文件路径
            with pdfplumber.open(file_path_or_bytes) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        else:
            # 字节流（内存中的文件）
            with pdfplumber.open(io.BytesIO(file_path_or_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        return text.strip()
        
    except Exception as e:
        raise Exception(f"PDF 文本提取失败: {str(e)}")