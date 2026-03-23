from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

def generate_pdf(content, topic, output_path):
    """
    生成 PDF 报告
    
    Args:
        content: 文献综述内容
        topic: 研究主题
        output_path: 输出文件路径
    """
    try:
        # 创建 PDF 文档
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # 样式设置
        styles = getSampleStyleSheet()
        
        # 自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=1  # 居中
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=0  # 左对齐
        )
        
        # 构建文档内容
        story = []
        
        # 标题
        story.append(Paragraph(f"文献综述：{topic}", title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # 处理内容，分割段落
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            if para.strip():
                # 检查是否为标题（简单判断：以数字加点开头）
                if para.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.')):
                    story.append(Paragraph(para, heading_style))
                else:
                    story.append(Paragraph(para, body_style))
                story.append(Spacer(1, 0.1 * inch))
        
        # 生成 PDF
        doc.build(story)
        
    except Exception as e:
        raise Exception(f"PDF 生成失败: {str(e)}")