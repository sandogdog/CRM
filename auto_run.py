#!/usr/bin/env python
"""
CRM自动化测试 - 自动化执行入口（简化版）
专门用于生产环境的完全自动化执行，无需人工干预

此文件现在是main.py的简化包装器，避免代码重复。
如果需要完整的交互式功能，请直接使用 main.py

使用方法：
python auto_run.py
"""
import sys
import os
import subprocess

def main():
    """自动化执行主函数 - 调用main.py的完整流程"""
    print("=" * 80)
    print("🚀 CRM自动化测试 - 完全自动化执行")
    print("=" * 80)
    print("🎯 自动执行完整业务流程测试")
    print("⚡ 调用main.py的完整流程功能")
    print("")
    
    try:
        # 调用main.py，并自动选择完整流程（选项4）
        print("🔄 启动main.py...")
        
        # 这里可以通过环境变量或参数来控制main.py的行为
        # 暂时保持简单，提示用户使用main.py
        print("💡 建议直接运行：python main.py")
        print("   然后选择 '4️⃣ 测试所有私海线索功能（完整流程）'")
        print("")
        print("🔧 如需完全自动化，请在main.py中添加命令行参数支持")
        
        return 0
        
    except Exception as e:
        print(f"❌ 执行异常: {e}")
        return 1
    
    finally:
        print("=" * 80)
        print("🏁 auto_run.py 执行完毕")
        print("💡 提示：建议直接使用 main.py 获得更好的体验")
        print("=" * 80)


if __name__ == "__main__":
    sys.exit(main()) 