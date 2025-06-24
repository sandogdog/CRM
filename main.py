#!/usr/bin/env python
"""
CRM自动化测试 - 主入口文件
修复版登录和职位切换脚本 v2
解决职位选择时重复点击切换按钮的问题
新增：私海线索UI测试功能

代码已模块化拆分：
- crm_utils.py: 工具函数
- crm_login.py: 登录功能
- crm_role_switch.py: 职位切换功能
- crm_private_sea.py: 私海线索操作功能
- crm_workflow.py: 主工作流程
"""
import sys
import os
import time
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入模块化后的功能
from crm_workflow import login_and_complete_workflow, login_and_switch_role_fixed_v2, test_quick_follow_up_only

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 CRM自动化测试 - 登录、职位切换、私海线索")
    print("=" * 70)
    
    start_time = time.time()
    print("🚀 开始执行完整自动化流程...")
    
    result, customer_name, phone, quick_follow_success = login_and_complete_workflow()
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("=" * 70)
    if result and hasattr(result, 'current_url'):
        print("✅ 完整自动化流程执行成功！")
        print(f"⏱️ 执行时间: {execution_time:.2f} 秒")
        print("🌐 浏览器保持打开状态")
        print(f"📍 当前页面: {result.current_url}")
        print("")
        print("🎯 完成的操作:")
        print("   ✅ SSO登录")
        print("   ✅ 职位切换")
        if customer_name and phone:
            print("   ✅ 私海线索添加")
            print(f"   📝 添加的线索信息:")
            print(f"      客户名称: {customer_name}")
            print(f"      联系人: 秦仁驰")
            print(f"      电话: {phone}")
        if quick_follow_success:
            print("   ✅ 快速跟进按钮点击")
        else:
            print("   ⚠️ 快速跟进按钮点击失败")
        print("")
        print("📸 截图保存位置:")
        print("   - screenshots/role_switch_fixed_v2_completed.png")
        if customer_name and phone:
            print("   - screenshots/private_sea_clue_added.png")
        if quick_follow_success:
            print("   - screenshots/quick_follow_up_clicked.png")
        else:
            print("   - screenshots/quick_follow_up_error.png")
        print("")
        print("🎉 自动化流程完成！浏览器保持打开状态以供后续操作。")
        if quick_follow_success:
            print("💡 快速跟进弹窗应该已经打开，您可以继续进行后续操作。")
    else:
        print("❌ 完整自动化流程执行失败！")
        print(f"⏱️ 执行时间: {execution_time:.2f} 秒")
        print("💡 请检查错误日志和截图")
    
    print("=" * 70) 