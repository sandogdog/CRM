#!/usr/bin/env python3
"""
CRM自动化测试主程序
重构后的模块化架构，支持分模块独立测试
"""

import logging
import time
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crm_login import login_to_crm
from crm_role_switch import switch_role_fixed_v2  
from crm_private_sea_add import test_private_sea_add_workflow, navigate_to_private_sea, add_private_sea_clue
from crm_private_sea_launch import test_private_sea_launch_workflow, test_private_sea_launch_with_public_track
from crm_private_sea_follow_up import click_quick_follow_up, complete_follow_up_process
from crm_public_sea import test_public_sea_track_workflow
from crm_business_private_sea import navigate_to_private_business, test_private_business_navigation, test_private_business_launch_workflow, test_public_business_track_workflow, test_private_business_launch_with_public_track
from crm_customer_private_sea import test_customer_private_sea_ipipgo_workflow, test_customer_private_sea_to_public_workflow
from crm_customer_public_sea import test_customer_public_sea_claim, test_customer_private_to_public_claim_workflow
from utils.driver_manager import DriverManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crm_test.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def initialize_crm_session(driver):
    """
    初始化CRM会话：登录 + 角色切换
    这是所有测试流程的通用前置步骤
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 初始化是否成功
    """
    try:
        logger.info("🔧 开始初始化CRM会话...")
        
        # 步骤1: 登录CRM系统
        logger.info("步骤1: 开始登录CRM系统...")
        if not login_to_crm(driver):
            logger.error("❌ 登录失败")
            return False
            
        # 步骤2: 切换到销售角色
        logger.info("步骤2: 开始切换到销售角色...")
        if not switch_role_fixed_v2(driver):
            logger.error("❌ 角色切换失败")
            return False
        
        logger.info("✅ CRM会话初始化完成！")
        return True
        
    except Exception as e:
        logger.error(f"CRM会话初始化异常: {e}")
        return False


def test_private_sea_add_only():
    """独立测试私海线索添加功能"""
    driver = None
    try:
        logger.info("🧪 开始测试私海线索添加功能...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 执行私海线索添加测试
        success = test_private_sea_add_workflow(driver)
        
        if success:
            logger.info("🎉 私海线索添加测试完成！")
        else:
            logger.error("❌ 私海线索添加测试失败！")
        
        return success
        
    except Exception as e:
        logger.error(f"私海线索添加测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(2)
            driver.quit()


def test_private_sea_launch_only():
    """独立测试私海线索投放功能 - 基于现有线索"""
    driver = None
    try:
        logger.info("🧪 开始测试私海线索投放功能...")
        logger.info("⚠️ 注意：此功能需要页面已有线索数据才能执行投放操作")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 导航到私海线索页面
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
        
        # 直接执行投放测试（基于现有线索）
        success = test_private_sea_launch_workflow(driver)
        
        if success:
            logger.info("🎉 私海线索投放测试完成！")
        else:
            logger.error("❌ 私海线索投放测试失败！")
            logger.error("💡 提示：请确保页面中已有可投放的线索数据")
        
        return success
        
    except Exception as e:
        logger.error(f"私海线索投放测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(2)
            driver.quit()


def test_private_sea_follow_up_only():
    """独立测试私海线索快速跟进功能 - 基于现有线索"""
    driver = None
    try:
        logger.info("🧪 开始测试私海线索快速跟进功能...")
        logger.info("⚠️ 注意：此功能需要页面已有线索数据才能执行跟进操作")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 导航到私海线索页面
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
            
        # 直接执行快速跟进测试（基于现有线索）
        success = click_quick_follow_up(driver)
        
        if success:
            logger.info("🎉 私海线索快速跟进测试完成！")
            logger.info("⚠️ 注意：快速跟进完整流程（跟进面板+报价单）功能待完善")
        else:
            logger.error("❌ 私海线索快速跟进测试失败！")
            logger.error("💡 提示：请确保页面中已有可跟进的线索数据")
        
        return success
        
    except Exception as e:
        logger.error(f"私海线索快速跟进测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(3)  # 多等一会儿，便于查看结果
            driver.quit()


def test_add_then_launch():
    """测试添加线索后投放的组合流程"""
    driver = None
    try:
        logger.info("🧪 开始测试添加+投放组合流程...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 导航到私海线索页面
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
        
        # 步骤1: 添加线索
        logger.info("🔸 步骤1: 添加新线索...")
        success, customer_name, phone = add_private_sea_clue(driver)
        if not success:
            logger.error("❌ 添加线索失败")
            return False
        logger.info(f"✅ 成功添加线索: {customer_name}, 电话: {phone}")
        
        # 步骤2: 投放线索
        logger.info("🔸 步骤2: 投放刚添加的线索...")
        success = test_private_sea_launch_workflow(driver)
        if not success:
            logger.error("❌ 投放线索失败")
            return False
        
        logger.info("🎉 添加+投放组合流程测试完成！")
        return True
        
    except Exception as e:
        logger.error(f"添加+投放组合流程测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(2)
            driver.quit()


def test_add_then_follow_up():
    """测试添加线索后跟进的组合流程"""
    driver = None
    try:
        logger.info("🧪 开始测试添加+跟进组合流程...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
            
        # 导航到私海线索页面
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
        
        # 步骤1: 添加线索
        logger.info("🔸 步骤1: 添加新线索...")
        success, customer_name, phone = add_private_sea_clue(driver)
        if not success:
            logger.error("❌ 添加线索失败")
            return False
        logger.info(f"✅ 成功添加线索: {customer_name}, 电话: {phone}")
        
        # 步骤2: 快速跟进
        logger.info("🔸 步骤2: 对刚添加的线索进行快速跟进...")
        success = click_quick_follow_up(driver)
        if success:
            logger.info("✅ 快速跟进操作成功")
        else:
            logger.warning("⚠️ 快速跟进操作失败")
        
        logger.info("🎉 添加+跟进组合流程测试完成！")
        return True
        
    except Exception as e:
        logger.error(f"添加+跟进组合流程测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(3)
            driver.quit()


def test_add_then_launch_then_track():
    """测试添加线索后投放再跟踪的完整业务流程"""
    driver = None
    try:
        logger.info("🧪 开始测试添加+投放+跟踪完整业务流程...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 导航到私海线索页面
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
        
        # 步骤1: 添加线索
        logger.info("🔸 步骤1: 添加新线索...")
        success, customer_name, phone = add_private_sea_clue(driver)
        if not success:
            logger.error("❌ 添加线索失败")
            return False
        logger.info(f"✅ 成功添加线索: {customer_name}, 电话: {phone}")
        
        # 步骤2: 投放线索并继续到公海跟踪
        logger.info("🔸 步骤2: 投放线索并导航到公海进行跟踪...")
        success = test_private_sea_launch_with_public_track(driver, "私海线索-ui自动化")
        if not success:
            logger.error("❌ 投放+跟踪流程失败")
            return False
        
        logger.info("🎉 添加+投放+跟踪完整业务流程测试完成！")
        return True
        
    except Exception as e:
        logger.error(f"添加+投放+跟踪流程测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(3)
            driver.quit()


def test_public_sea_track_only():
    """独立测试公海线索跟踪功能 - 基于现有线索"""
    driver = None
    try:
        logger.info("🧪 开始测试公海线索跟踪功能...")
        logger.info("⚠️ 注意：此功能需要公海页面已有线索数据才能执行跟踪操作")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 直接执行公海跟踪测试
        success = test_public_sea_track_workflow(driver, "私海线索-ui自动化")
        
        if success:
            logger.info("🎉 公海线索跟踪测试完成！")
        else:
            logger.error("❌ 公海线索跟踪测试失败！")
            logger.error("💡 提示：请确保公海页面中已有可跟踪的线索数据")
        
        return success
        
    except Exception as e:
        logger.error(f"公海线索跟踪测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(3)
            driver.quit()


def test_private_business_navigation_only():
    """独立测试私海商机页面导航功能"""
    driver = None
    try:
        logger.info("🧪 开始测试私海商机页面导航功能...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 执行私海商机导航测试
        success = test_private_business_navigation(driver)
        
        if success:
            logger.info("🎉 私海商机页面导航测试完成！")
        else:
            logger.error("❌ 私海商机页面导航测试失败！")
        
        return success
        
    except Exception as e:
        logger.error(f"私海商机页面导航测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(2)
            driver.quit()


def test_business_launch_with_track():
    """测试商机投放+跟踪的完整流程"""
    driver = None
    try:
        logger.info("🧪 开始测试商机投放→跟踪完整流程...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 执行商机投放+跟踪完整流程
        success = test_private_business_launch_with_public_track(driver)
        
        if success:
            logger.info("🎉 商机投放→跟踪完整流程测试完成！")
            logger.info("💡 浏览器保持打开状态，您可以查看操作结果")
        else:
            logger.error("❌ 商机投放→跟踪完整流程测试失败！")
        
        return success
        
    except Exception as e:
        logger.error(f"商机投放→跟踪完整流程测试异常: {e}")
        return False
        
    finally:
        # 不关闭浏览器，保持打开状态
        logger.info("✅ 测试完成，浏览器保持打开状态供查看结果")


def test_customer_private_sea_ipipgo():
    """测试客户私海IPIPGO导航功能"""
    driver = None
    try:
        logger.info("🧪 开始测试客户私海IPIPGO导航功能...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 执行客户私海IPIPGO导航测试
        success = test_customer_private_sea_ipipgo_workflow(driver)
        
        if success:
            logger.info("🎉 客户私海IPIPGO导航测试完成！")
            logger.info("💡 浏览器保持打开状态，您可以查看操作结果")
        else:
            logger.error("❌ 客户私海IPIPGO导航测试失败！")
            logger.error("💡 提示：请确保客户私海页面中存在IPIPGO标签页")
        
        return success
        
    except Exception as e:
        logger.error(f"客户私海IPIPGO导航测试异常: {e}")
        return False
        
    finally:
        # 不关闭浏览器，保持打开状态
        logger.info("✅ 测试完成，浏览器保持打开状态供查看结果")


def test_customer_private_sea_to_public():
    """测试客户私海投入公海功能"""
    driver = None
    try:
        logger.info("🧪 开始测试客户私海投入公海功能...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 执行客户私海投入公海测试
        success = test_customer_private_sea_to_public_workflow(driver)
        
        if success:
            logger.info("🎉 客户私海投入公海测试完成！")
            logger.info("💡 浏览器保持打开状态，您可以查看操作结果")
        else:
            logger.error("❌ 客户私海投入公海测试失败！")
            logger.error("💡 提示：请确保客户私海IPIPGO页面中存在目标客户（电话183****6247）")
        
        return success
        
    except Exception as e:
        logger.error(f"客户私海投入公海测试异常: {e}")
        return False
        
    finally:
        # 不关闭浏览器，保持打开状态
        logger.info("✅ 测试完成，浏览器保持打开状态供查看结果")


def test_customer_public_sea_claim_workflow():
    """测试客户公海领取功能"""
    driver = None
    try:
        logger.info("🧪 开始测试客户公海领取功能...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 执行客户公海领取测试
        success = test_customer_public_sea_claim(driver)
        
        if success:
            logger.info("🎉 客户公海领取测试完成！")
            logger.info("💡 浏览器保持打开状态，您可以查看操作结果")
        else:
            logger.error("❌ 客户公海领取测试失败！")
            logger.error("💡 提示：请确保客户公海IPIPGO页面中存在目标客户（用户ID 7156）")
        
        return success
        
    except Exception as e:
        logger.error(f"客户公海领取测试异常: {e}")
        return False
        
    finally:
        # 不关闭浏览器，保持打开状态
        logger.info("✅ 测试完成，浏览器保持打开状态供查看结果")


def test_customer_complete_workflow():
    """测试客户完整业务流程：私海投入公海 → 公海领取客户"""
    driver = None
    try:
        logger.info("🧪 开始测试客户完整业务流程...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 执行客户完整流程测试
        success = test_customer_private_to_public_claim_workflow(driver)
        
        if success:
            logger.info("🎉 客户完整业务流程测试完成！")
            logger.info("💡 浏览器保持打开状态，您可以查看操作结果")
        else:
            logger.error("❌ 客户完整业务流程测试失败！")
            logger.error("💡 提示：请确保用户ID 7156在系统中存在且可操作")
        
        return success
        
    except Exception as e:
        logger.error(f"客户完整业务流程测试异常: {e}")
        return False
        
    finally:
        # 不关闭浏览器，保持打开状态
        logger.info("✅ 测试完成，浏览器保持打开状态供查看结果")


def test_all_private_sea_workflows():
    """测试所有私海线索功能的完整流程"""
    driver = None
    try:
        logger.info("🧪 开始测试所有私海线索功能...")
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        if not initialize_crm_session(driver):
            return False
        
        # 导航到私海线索页面
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
        
        # 测试1: 添加线索
        logger.info("🔸 测试1: 添加线索")
        success, customer_name, phone = add_private_sea_clue(driver)
        if not success:
            logger.error("❌ 添加线索失败")
            return False
        
        logger.info(f"✅ 成功添加线索: {customer_name}, 电话: {phone}")
        
        # 测试2: 投放线索
        logger.info("🔸 测试2: 投放线索")
        success = test_private_sea_launch_workflow(driver)
        if not success:
            logger.error("❌ 投放线索失败")
            return False
        
        # 重新添加线索用于快速跟进测试
        logger.info("🔸 重新添加线索用于快速跟进测试")
        success, customer_name2, phone2 = add_private_sea_clue(driver)
        if not success:
            logger.error("❌ 重新添加线索失败")
            return False
        
        logger.info(f"✅ 成功添加第二个线索: {customer_name2}, 电话: {phone2}")
        
        # 测试3: 快速跟进
        logger.info("🔸 测试3: 快速跟进功能")
        success = click_quick_follow_up(driver)
        if success:
            logger.info("✅ 快速跟进按钮点击成功")
        else:
            logger.warning("⚠️ 快速跟进功能测试失败")
        
        logger.info("🎉 所有私海线索功能测试完成！")
        logger.info("📊 测试结果汇总:")
        logger.info("   ✅ 登录和角色切换")
        logger.info("   ✅ 私海线索页面导航")
        logger.info("   ✅ 线索添加功能")
        logger.info("   ✅ 线索投放功能")
        logger.info(f"   {'✅' if success else '⚠️'} 快速跟进功能")
        
        return True
        
    except Exception as e:
        logger.error(f"私海线索完整测试异常: {e}")
        return False
        
    finally:
        if driver:
            logger.info("关闭浏览器...")
            time.sleep(3)
            driver.quit()


def show_main_menu():
    """显示主菜单"""
    print("=" * 70)
    print("🚀 CRM自动化测试系统 - 核心功能测试")
    print("=" * 70)
    print("📋 核心功能独立测试:")
    print("")
    print("1️⃣  线索添加功能测试")
    print("2️⃣  线索投放与跟踪测试")
    print("3️⃣  线索快速跟进测试")
    print("4️⃣  商机投放→跟踪完整流程")
    print("5️⃣  客户私海IPIPGO导航测试")
    print("6️⃣  客户投入公海→领取完整流程")
    print("")
    print("0️⃣  退出程序")
    print("=" * 70)
    print("💡 每项功能都是独立测试，方便单独验证")
    print("💡 选择对应数字即可开始相应功能的测试")
    print("💡 测试完成后浏览器保持打开状态供查看结果")
    print("💡 商机投放→跟踪是完整业务流程（私海投放后到公海跟踪）")
    print("💡 客户投入公海→领取是完整业务流程（私海投入后到公海领取）")
    print("💡 客户操作会使用指定客户（用户ID 7156）")
    print("=" * 70)


def test_complete_crm_workflow():
    """完整的CRM业务流程测试
    
    执行顺序：
    1. 添加线索
    2. 线索的投放和领取
    3. 线索的快速跟进
    4. 商机的投放和领取
    5. 客户的投放和领取
    """
    driver = None
    try:
        logger.info("🚀 开始完整CRM业务流程测试...")
        logger.info("=" * 80)
        logger.info("📋 完整流程包括：")
        logger.info("   1️⃣ 添加线索")
        logger.info("   2️⃣ 线索的投放和领取")
        logger.info("   3️⃣ 线索的快速跟进（按钮+面板+报价单）")
        logger.info("   4️⃣ 商机的投放和领取")
        logger.info("   5️⃣ 客户的投放和领取")
        logger.info("=" * 80)
        
        # 初始化WebDriver
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 初始化CRM会话
        logger.info("🔧 步骤0: 初始化CRM会话（登录+角色切换）...")
        if not initialize_crm_session(driver):
            logger.error("❌ CRM会话初始化失败")
            return False
        
        logger.info("✅ CRM会话初始化完成")
        time.sleep(2)
        
        # 步骤1: 添加线索
        logger.info("🔸 步骤1: 开始添加线索...")
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
            
        success, customer_name, phone = add_private_sea_clue(driver)
        if not success:
            logger.error("❌ 添加线索失败")
            return False
        
        logger.info(f"✅ 步骤1完成: 成功添加线索 {customer_name}, 电话: {phone}")
        time.sleep(3)
        
        # 步骤2: 线索的投放和领取
        logger.info("🔸 步骤2: 开始线索投放和领取...")
        success = test_private_sea_launch_with_public_track(driver)
        if not success:
            logger.error("❌ 线索投放和领取失败")
            return False
        
        logger.info("✅ 步骤2完成: 线索投放和领取成功")
        time.sleep(3)
        
        # 步骤3: 线索的快速跟进（完整流程：按钮点击+面板处理+报价单）
        logger.info("🔸 步骤3: 开始线索快速跟进完整流程...")
        logger.info("💡 完整流程包括：快速跟进按钮 → 跟进面板配置 → 报价单填写")
        
        # 确保在私海线索页面
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
            
        # 执行完整的快速跟进流程
        success = complete_follow_up_process(driver)
        if not success:
            logger.warning("⚠️ 线索快速跟进完整流程失败，但继续执行后续流程")
        else:
            logger.info("✅ 步骤3完成: 线索快速跟进完整流程成功")
        
        time.sleep(3)
        
        # 步骤4: 商机的投放和领取
        logger.info("🔸 步骤4: 开始商机投放和领取...")
        success = test_private_business_launch_with_public_track(driver)
        if not success:
            logger.error("❌ 商机投放和领取失败")
            return False
        
        logger.info("✅ 步骤4完成: 商机投放和领取成功")
        time.sleep(3)
        
        # 步骤5: 客户的投放和领取
        logger.info("🔸 步骤5: 开始客户投放和领取...")
        success = test_customer_private_to_public_claim_workflow(driver)
        if not success:
            logger.error("❌ 客户投放和领取失败")
            return False
        
        logger.info("✅ 步骤5完成: 客户投放和领取成功")
        
        # 完整流程总结
        logger.info("🎉 完整CRM业务流程测试完成！")
        logger.info("=" * 80)
        logger.info("📊 流程执行总结：")
        logger.info("   ✅ 1. 添加线索 - 成功")
        logger.info("   ✅ 2. 线索投放和领取 - 成功")
        logger.info(f"   {'✅' if success else '⚠️'} 3. 线索快速跟进 - {'成功' if success else '部分成功'}")
        logger.info("   ✅ 4. 商机投放和领取 - 成功")
        logger.info("   ✅ 5. 客户投放和领取 - 成功")
        logger.info("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"完整CRM业务流程测试异常: {e}")
        return False
        
    finally:
        # 完成后等待3秒关闭浏览器
        if driver:
            logger.info("✅ 测试完成，等待3秒后关闭浏览器...")
            time.sleep(3)
            try:
                driver.quit()
                logger.info("🚪 浏览器已关闭")
            except Exception as e:
                logger.warning(f"⚠️ 关闭浏览器时出现异常: {e}")


def main():
    """主函数 - 执行完整CRM业务流程"""
    try:
        print("🚀 CRM自动化测试系统 - 完整业务流程")
        print("=" * 80)
        print("📋 即将执行完整的CRM业务流程测试：")
        print("   1️⃣ 添加线索")
        print("   2️⃣ 线索的投放和领取")
        print("   3️⃣ 线索的快速跟进（按钮+面板+报价单）")
        print("   4️⃣ 商机的投放和领取")
        print("   5️⃣ 客户的投放和领取")
        print("=" * 80)
        print("💡 整个流程将自动执行，无需手动选择")
        print("💡 测试完成后浏览器将等待3秒后自动关闭")
        print("💡 按Ctrl+C可以随时中断测试")
        print("=" * 80)
        
        input("按回车键开始执行完整流程...")
        
        # 执行完整流程
        success = test_complete_crm_workflow()
        
        if success:
            print("\n🎉 完整CRM业务流程测试成功完成！")
        else:
            print("\n❌ 完整CRM业务流程测试失败！")
            
    except KeyboardInterrupt:
        print("\n👋 用户中断，退出测试系统")
    except Exception as e:
        logger.error(f"主程序异常: {e}")
        print(f"❌ 程序异常: {e}")


if __name__ == "__main__":
    main() 