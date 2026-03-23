"""
简单测试 PDF 生成 - 验证是否能正常生成 PDF
"""
import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("测试 PDF 生成功能")
print("=" * 60)

# 导入 PDF 生成函数
from utils.pdf_generator import generate_pdf

# 创建简单的测试内容
test_content = """
1. 研究背景与意义

人工智能在医疗领域的应用正在快速发展。深度学习算法在医学图像诊断中展现出优异性能，准确率超过人类专家。

2. 主要研究进展

2.1 医学影像诊断
卷积神经网络(CNN)在肺癌筛查、乳腺癌检测等领域取得突破性进展。研究显示，AI系统在早期诊断中的准确率达到95%以上。

2.2 药物研发
AI技术将新药研发周期从10年缩短到2-3年，大幅降低成本。

2.3 个性化治疗
基于患者基因信息和临床数据，AI系统推荐个性化治疗方案。

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
print("\n正在生成 PDF...")
output_file = "test_output.pdf"

try:
    result = generate_pdf(test_content, "人工智能在医疗诊断中的应用", output_file)
    
    if result:
        print(f"\n✅ PDF 生成成功！")
        
        # 检查文件是否存在
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"文件位置: {os.path.abspath(output_file)}")
            print(f"文件大小: {file_size} 字节")
            
            if file_size > 1000:
                print("✅ 文件大小正常，请打开查看")
            else:
                print("⚠️ 文件太小，可能生成有问题")
        else:
            print("❌ 文件未找到")
    else:
        print("❌ PDF 生成失败")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("请打开 test_output.pdf 查看效果")
print("=" * 60)