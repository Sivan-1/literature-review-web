"""
完整流程调试脚本 - 测试每一步并保存中间结果
"""
import os
import sys
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("文献综述系统调试工具")
print("=" * 60)

# 1. 测试 PDF 提取
print("\n[1/5] 测试 PDF 文本提取...")
from utils.pdf_extractor import extract_pdf_text

# 创建简单的测试 PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

test_pdf_path = "test_simple.pdf"
c = canvas.Canvas(test_pdf_path, pagesize=letter)
c.setFont('Helvetica', 12)
test_content = """
人工智能在医疗领域的应用

摘要：本文研究AI技术在医疗诊断中的应用。
深度学习算法在医学图像分析中表现优异。
卷积神经网络在肺癌筛查中准确率达95%。
"""
y = 750
for line in test_content.strip().split('\n'):
    c.drawString(72, y, line)
    y -= 20
c.save()
print(f"✅ 创建测试文件: {test_pdf_path}")

# 提取文本
extracted_text = extract_pdf_text(test_pdf_path)
print(f"✅ 提取的文本长度: {len(extracted_text)} 字符")
print(f"提取内容:\n{extracted_text[:500]}\n")

# 2. 测试提示词构建
print("\n[2/5] 测试提示词构建...")
from utils.prompt_builder import build_prompt

topic = "人工智能在医疗诊断中的应用"
prompt = build_prompt(topic, extracted_text)
print(f"✅ 提示词构建成功，长度: {len(prompt)} 字符")
print(f"提示词预览:\n{prompt[:300]}...\n")

# 保存提示词供检查
with open("debug_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)
print("✅ 提示词已保存到 debug_prompt.txt")

# 3. 测试 API 调用（可选，需要您输入 API Key）
print("\n[3/5] 测试 API 调用...")
api_key = input("请输入 DeepSeek API Key (直接回车跳过): ").strip()

if api_key:
    from utils.api_client import call_deepseek_api
    
    print("正在调用 API...")
    try:
        literature_review = call_deepseek_api(prompt, api_key)
        print(f"✅ API 返回内容长度: {len(literature_review)} 字符")
        
        # 保存 API 返回内容
        with open("debug_api_response.txt", "w", encoding="utf-8") as f:
            f.write(literature_review)
        print("✅ API 返回内容已保存到 debug_api_response.txt")
        
        # 显示前500字符
        print(f"\nAPI 返回预览:\n{literature_review[:500]}...\n")
        
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        literature_review = None
else:
    print("跳过 API 调用")
    literature_review = None

# 4. 测试 PDF 生成
print("\n[4/5] 测试 PDF 生成...")
from utils.pdf_generator import generate_pdf

if literature_review:
    test_content = literature_review
else:
    # 使用测试内容
    test_content = """
1. 研究背景与意义

人工智能技术在医疗领域的应用正在快速发展。深度学习算法在医学图像诊断中展现出优异性能，准确率超过人类专家。

2. 主要研究进展

2.1 医学影像诊断
卷积神经网络(CNN)在肺癌筛查、乳腺癌检测等领域取得突破性进展。研究显示，AI系统在早期诊断中的准确率达到95%以上。

2.2 药物研发
AI技术将新药研发周期从10年缩短到2-3年，大幅降低成本。机器学习模型可以预测药物分子的活性和毒性。

2.3 个性化治疗
基于患者基因信息和临床数据，AI系统推荐个性化治疗方案，提高治疗效果。

3. 研究方法与技术路线

深度学习方法、自然语言处理、知识图谱等技术被广泛应用于医疗数据分析。

4. 研究热点与趋势分析

可解释性AI、联邦学习、多模态学习是当前研究热点。

5. 存在的问题与挑战

数据隐私保护、算法偏见、临床验证、法规遵从是主要挑战。

6. 未来研究方向建议

- 开发可解释的AI模型
- 建立医疗AI评估标准
- 推动多中心临床研究
- 加强数据隐私保护技术

7. 主要参考文献

[1] 张明等. 深度学习在医学影像分析中的应用. 中国医学影像技术, 2023.
[2] Smith J. AI in Healthcare: A Comprehensive Review. Nature Medicine, 2022.
[3] 李华. 人工智能辅助诊断系统研究进展. 中华医学杂志, 2023.
"""

# 生成 PDF
output_path = "debug_output.pdf"
try:
    generate_pdf(test_content, topic, output_path)
    print(f"✅ PDF 生成成功: {output_path}")
    
    # 检查文件大小
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"文件大小: {size} 字节")
        if size < 1000:
            print("⚠️ 警告: 文件太小，可能生成有问题")
except Exception as e:
    print(f"❌ PDF 生成失败: {e}")
    import traceback
    traceback.print_exc()

# 5. 生成报告
print("\n[5/5] 生成调试报告...")
report = {
    "timestamp": datetime.now().isoformat(),
    "python_version": sys.version,
    "extracted_text_length": len(extracted_text),
    "prompt_length": len(prompt),
    "api_called": bool(api_key),
    "api_response_length": len(literature_review) if literature_review else 0,
}

with open("debug_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("调试完成！生成的文件:")
print("  - test_simple.pdf (测试用 PDF)")
print("  - debug_prompt.txt (提示词内容)")
if api_key:
    print("  - debug_api_response.txt (API 返回内容)")
print("  - debug_output.pdf (生成的 PDF)")
print("  - debug_report.json (调试报告)")
print("=" * 60)
print("\n请检查 debug_output.pdf 是否正常显示内容")