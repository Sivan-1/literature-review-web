def build_prompt(research_topic, text_content):
    """
    构建发送给 DeepSeek API 的提示词
    
    Args:
        research_topic: 研究主题
        text_content: 从 PDF 提取的文本内容
        
    Returns:
        str: 完整的提示词
    """
    # 限制文本长度，避免超过 API 限制（这里设置为 15000 字符）
    max_text_length = 15000
    if len(text_content) > max_text_length:
        text_content = text_content[:max_text_length] + "...(内容已截断)"
    
    prompt = f"""请基于以下研究主题和文献内容，生成一份详细的文献综述报告。

研究主题：{research_topic}

文献内容：
{text_content}

请按照以下结构生成文献综述：

1. 研究背景与意义
2. 主要研究进展与发现
3. 研究方法与技术路线总结
4. 研究热点与趋势分析
5. 存在的问题与挑战
6. 未来研究方向建议
7. 主要参考文献

要求：
- 语言专业、严谨，符合学术规范
- 内容基于提供的文献进行分析和总结
- 适当引用文献中的观点
- 字数控制在 2000-3000 字

请开始生成文献综述："""
    
    return prompt