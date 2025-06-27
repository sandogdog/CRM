#!/usr/bin/env python3
"""
CRM自动化测试 - 自动运行脚本
直接执行完整的CRM业务流程，无需用户选择
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入主程序
from main import test_complete_crm_workflow

if __name__ == "__main__":
    print("🚀 CRM自动化测试 - 自动运行模式")
    print("=" * 60)
    print("📋 将自动执行完整CRM业务流程：")
    print("   1️⃣ 添加线索")
    print("   2️⃣ 线索的投放和领取")
    print("   3️⃣ 线索的快速跟进（按钮+面板+报价单）")
    print("   4️⃣ 商机的投放和领取")
    print("   5️⃣ 客户的投放和领取")
    print("=" * 60)
    
    try:
        # 直接执行完整流程
        success = test_complete_crm_workflow()
        
        if success:
            print("\n🎉 完整CRM业务流程自动测试成功！")
            print("💡 浏览器已自动关闭")
        else:
            print("\n❌ 完整CRM业务流程自动测试失败！")
            print("💡 请查看日志文件 crm_test.log 获取详细错误信息")
            
    except KeyboardInterrupt:
        print("\n👋 用户中断测试")
    except Exception as e:
        print(f"\n❌ 自动测试异常: {e}") 