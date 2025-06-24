#!/usr/bin/env python
"""
CRM自动化测试 - 模块测试脚本
验证所有模块是否正常导入和工作
"""
import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_module_imports():
    """测试所有模块是否可以正常导入"""
    print("🧪 开始测试模块导入...")
    
    try:
        # 测试工具模块
        from crm_utils import generate_random_phone, generate_random_suffix, setup_browser
        print("✅ crm_utils 模块导入成功")
        
        # 测试登录模块
        from crm_login import login_to_crm
        print("✅ crm_login 模块导入成功")
        
        # 测试职位切换模块
        from crm_role_switch import switch_role_fixed_v2
        print("✅ crm_role_switch 模块导入成功")
        
        # 测试私海线索模块
        from crm_private_sea import add_private_sea_clue, click_quick_follow_up
        print("✅ crm_private_sea 模块导入成功")
        
        # 测试工作流程模块
        from crm_workflow import login_and_complete_workflow, login_and_switch_role_fixed_v2, test_quick_follow_up_only
        print("✅ crm_workflow 模块导入成功")
        
        print("\n🎉 所有模块导入测试通过！")
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def test_utility_functions():
    """测试工具函数"""
    print("\n🔧 开始测试工具函数...")
    
    try:
        from crm_utils import generate_random_phone, generate_random_suffix
        
        # 测试随机手机号生成
        phone = generate_random_phone()
        print(f"📱 生成的随机手机号: {phone}")
        assert len(phone) == 11, "手机号长度应该是11位"
        assert phone.isdigit(), "手机号应该全是数字"
        
        # 测试随机后缀生成
        suffix = generate_random_suffix()
        print(f"🔢 生成的随机后缀: {suffix}")
        assert len(suffix) == 4, "随机后缀长度应该是4位"
        assert suffix.isdigit(), "随机后缀应该全是数字"
        
        print("✅ 工具函数测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 工具函数测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 CRM模块化测试")
    print("=" * 60)
    
    # 测试模块导入
    import_success = test_module_imports()
    
    # 测试工具函数
    utility_success = test_utility_functions()
    
    print("\n" + "=" * 60)
    if import_success and utility_success:
        print("🎉 所有测试通过！模块化拆分成功！")
        print("\n📋 使用说明:")
        print("   - 运行 'python main.py' 执行完整流程")
        print("   - 运行 'python login_role_switch_fixed_v2.py' 使用原始版本")
        print("   - 各个模块可以单独导入使用")
    else:
        print("❌ 部分测试失败，请检查模块配置")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 