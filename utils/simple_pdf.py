"""
最简 PDF 生成器 - 不依赖 reportlab 复杂功能
"""
import os

def create_simple_pdf(content, topic, output_path):
    """
    创建最简单的 PDF（使用文本文件转 PDF 的替代方案）
    """
    try:
        from reportlab.pdfgen import canvas
        
        c = canvas.Canvas(output_path, pagesize=(612, 792))
        c.setFont("Helvetica", 10)
        
        # 写标题
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, 750, f"文献综述：{topic}")
        
        # 写内容
        c.setFont("Helvetica", 10)
        y = 720
        max_width = 450
        
        # 清理内容
        import re
        content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', content)
        
        # 分行处理
        lines = []
        for line in content.split('\n'):
            if line.strip():
                # 手动换行
                words = line.split()
                current_line = ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    # 粗略估计宽度
                    if len(test_line) * 6 < max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
            else:
                lines.append("")
        
        # 写入页面
        for line in lines:
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = 750
            c.drawString(72, y, line[:100])  # 限制长度
            y -= 15
        
        c.save()
        print(f"✅ PDF 已生成: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False

# 替换原有函数
def generate_pdf(content, topic, output_path):
    return create_simple_pdf(content, topic, output_path)