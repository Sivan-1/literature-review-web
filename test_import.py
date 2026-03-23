"""
测试模块导入
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 50)
print("测试 utils 模块导入")
print("=" * 50)

try:
    from utils import extract_pdf_text, build_prompt, call_deepseek_api, generate_pdf
    print("✅ 所有函数导入成功")
    print(f"   - extract_pdf_text: {extract_pdf_text}")
    print(f"   - build_prompt: {build_prompt}")
    print(f"   - call_deepseek_api: {call_deepseek_api}")
    print(f"   - generate_pdf: {generate_pdf}")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()

# 测试函数是否可调用
print("\n" + "=" * 50)
print("测试函数可调用性")
print("=" * 50)

try:
    # 测试 build_prompt
    test_prompt = build_prompt("测试主题", "测试内容")
    print(f"✅ build_prompt 可调用，返回长度: {len(test_prompt)}")
    
    # 测试 extract_pdf_text (需要文件，这里只测试导入)
    print(f"✅ extract_pdf_text 已导入")
    
    # 测试 generate_pdf (不实际运行，只检查存在)
    print(f"✅ generate_pdf 已导入")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")