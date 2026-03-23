"""
PDF 生成器 - 强化学术文献综述格式
"""
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

# 全局字体变量
CHINESE_FONT_NAME = None

def register_chinese_font():
    """注册中文字体"""
    global CHINESE_FONT_NAME
    
    font_paths = [
        ('SimHei', r'C:\Windows\Fonts\simhei.ttf'),
        ('Microsoft YaHei', r'C:\Windows\Fonts\msyh.ttc'),
        ('SimSun', r'C:\Windows\Fonts\simsun.ttc'),
        ('KaiTi', r'C:\Windows\Fonts\simkai.ttf'),
    ]
    
    for font_name, font_path in font_paths:
        try:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                CHINESE_FONT_NAME = font_name
                print(f"✅ 已注册字体: {font_name}")
                return font_name
        except Exception as e:
            continue
    
    print("⚠️ 未找到中文字体，使用默认字体")
    CHINESE_FONT_NAME = 'Helvetica'
    return 'Helvetica'

register_chinese_font()

def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    
    # 移除控制字符
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'[\u200b-\u200f\u2028-\u202f\u2060-\u206f]', '', text)
    text = text.replace('\u3000', ' ')
    text = text.replace('\xa0', ' ')
    
    return text.strip()

def generate_pdf(content, topic, output_path):
    """
    生成 PDF 报告 - 强化学术格式
    """
    try:
        print(f"\n开始生成 PDF...")
        
        # 清理内容
        content = clean_text(content)
        
        # 创建文档
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=72,
            bottomMargin=72,
            leftMargin=72,
            rightMargin=72
        )
        
        # 样式定义
        styles = getSampleStyleSheet()
        
        # 主标题样式
        title_style = ParagraphStyle(
            'MainTitle',
            parent=styles['Title'],
            fontName=CHINESE_FONT_NAME,
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            alignment=1,
            spaceAfter=30,
            leading=30
        )
        
        # 一级标题样式（一、二、三、）
        heading1_style = ParagraphStyle(
            'Heading1',
            parent=styles['Heading1'],
            fontName=CHINESE_FONT_NAME,
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceBefore=20,
            spaceAfter=12,
            leading=24,
            keepWithNext=True
        )
        
        # 二级标题样式（3.1、4.2等）
        heading2_style = ParagraphStyle(
            'Heading2',
            parent=styles['Heading2'],
            fontName=CHINESE_FONT_NAME,
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceBefore=12,
            spaceAfter=8,
            leading=18,
            leftIndent=0
        )
        
        # 正文样式
        body_style = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontName=CHINESE_FONT_NAME,
            fontSize=11,
            leading=18,
            alignment=0,
            spaceAfter=8
        )
        
        # 参考文献样式
        ref_style = ParagraphStyle(
            'Reference',
            parent=styles['Normal'],
            fontName=CHINESE_FONT_NAME,
            fontSize=10,
            leading=14,
            alignment=0,
            spaceAfter=4,
            leftIndent=20,
            firstLineIndent=0
        )
        
        # 构建内容
        story = []
        
        # 添加主标题
        story.append(Paragraph(f"文献综述：{topic}", title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # 添加生成信息
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontName=CHINESE_FONT_NAME,
            fontSize=9,
            textColor=colors.grey,
            alignment=2
        )
        story.append(Paragraph(f"生成时间：{datetime.now().strftime('%Y年%m月%d日')}", info_style))
        story.append(Spacer(1, 0.3 * inch))
        
        # 解析内容
        lines = content.split('\n')
        
        in_reference_section = False
        para_buffer = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                # 空行，结束当前段落
                if para_buffer:
                    para_text = ' '.join(para_buffer)
                    if para_text:
                        # 判断段落类型
                        if in_reference_section:
                            # 参考文献
                            if re.match(r'^\[\d+\]', para_text):
                                story.append(Paragraph(para_text, ref_style))
                        elif re.match(r'^[一二三四五六七八九十]+、', para_text):
                            # 一级标题
                            story.append(Paragraph(para_text, heading1_style))
                        elif re.match(r'^\d+\.\d+', para_text):
                            # 二级标题
                            story.append(Paragraph(para_text, heading2_style))
                        else:
                            # 普通正文
                            if len(para_text) > 800:
                                # 拆分长段落
                                for i in range(0, len(para_text), 500):
                                    sub_para = para_text[i:i+500]
                                    story.append(Paragraph(sub_para, body_style))
                            else:
                                story.append(Paragraph(para_text, body_style))
                        story.append(Spacer(1, 0.05 * inch))
                    para_buffer = []
                continue
            
            # 检查是否进入参考文献部分
            if '参考文献' in line or '八、参考文献' in line:
                in_reference_section = True
                story.append(Paragraph(line, heading1_style))
                story.append(Spacer(1, 0.1 * inch))
                continue
            
            # 检查是否是一级标题
            if re.match(r'^[一二三四五六七八九十]+、', line):
                if para_buffer:
                    para_text = ' '.join(para_buffer)
                    if para_text:
                        story.append(Paragraph(para_text, body_style))
                        story.append(Spacer(1, 0.05 * inch))
                    para_buffer = []
                story.append(Paragraph(line, heading1_style))
                story.append(Spacer(1, 0.1 * inch))
                continue
            
            # 检查是否是二级标题
            if re.match(r'^\d+\.\d+', line):
                if para_buffer:
                    para_text = ' '.join(para_buffer)
                    if para_text:
                        story.append(Paragraph(para_text, body_style))
                        story.append(Spacer(1, 0.05 * inch))
                    para_buffer = []
                story.append(Paragraph(line, heading2_style))
                story.append(Spacer(1, 0.08 * inch))
                continue
            
            # 普通文本，添加到缓冲区
            para_buffer.append(line)
        
        # 处理最后一个段落
        if para_buffer:
            para_text = ' '.join(para_buffer)
            if para_text:
                if in_reference_section and re.match(r'^\[\d+\]', para_text):
                    story.append(Paragraph(para_text, ref_style))
                else:
                    story.append(Paragraph(para_text, body_style))
                story.append(Spacer(1, 0.05 * inch))
        
        # 生成 PDF
        doc.build(story)
        
        # 验证
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ PDF 已生成: {output_path}")
            print(f"文件大小: {file_size:,} 字节")
            return True
        else:
            print("❌ 文件未生成")
            return False
            
    except Exception as e:
        print(f"❌ PDF 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False