#!/usr/bin/env python
"""
CRM自动化测试 - 私海线索添加模块
包含私海线索页面导航和线索添加功能
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crm_utils import generate_random_phone, generate_random_suffix, click_customer_management_menu

# 配置日志
logger = logging.getLogger(__name__)


def navigate_to_private_sea(driver):
    """
    导航到私海线索页面
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 导航是否成功
    """
    try:
        logger.info("🌊 开始导航到私海线索页面...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 步骤1: 点击客户管理主菜单（前端更新后必须先点击）
        logger.info("步骤1: 点击客户管理主菜单...")
        if not click_customer_management_menu(driver):
            logger.error("❌ 点击客户管理菜单失败")
            # 截图调试
            try:
                driver.save_screenshot("screenshots/click_customer_management_error.png")
                logger.info("📸 客户管理菜单点击失败截图已保存")
            except:
                pass
            return False
        
        # 步骤2: 点击私海线索菜单
        logger.info("步骤2: 点击私海线索菜单...")
        
        # 使用JavaScript查找并点击私海线索菜单
        js_click_private_sea = """
        // 查找私海线索菜单项
        var menuItems = document.querySelectorAll('li.el-menu-item');
        console.log('找到的菜单项数量:', menuItems.length);
        
        for (var i = 0; i < menuItems.length; i++) {
            var item = menuItems[i];
            var basePath = item.getAttribute('base-path');
            var span = item.querySelector('span');
            
            console.log('菜单项', i, '- base-path:', basePath, '- text:', span ? span.textContent.trim() : 'N/A');
            
            if (basePath && basePath.includes('/customerManagement/clews/privateSea')) {
                console.log('找到私海线索菜单，准备点击');
                item.click();
                return true;
            }
        }
        
        console.log('未找到私海线索菜单');
        return false;
        """
        
        if driver.execute_script(js_click_private_sea):
            logger.info("✅ 私海线索菜单已点击")
        else:
            logger.error("❌ 未找到私海线索菜单")
            # 截图调试
            try:
                driver.save_screenshot("screenshots/private_sea_menu_not_found.png")
                logger.info("📸 私海线索菜单未找到截图已保存")
            except:
                pass
            return False
        
        # 等待页面跳转和加载
        time.sleep(3)
        
        # 验证是否成功进入私海线索页面
        js_verify_page = """
        var currentUrl = window.location.href;
        return currentUrl.includes('/customerManagement/clews/privateSea') || 
               currentUrl.includes('privateSea');
        """
        
        if driver.execute_script(js_verify_page):
            logger.info("✅ 已成功进入私海线索页面")
            
            # 截图确认
            driver.save_screenshot("screenshots/private_sea_page_loaded.png")
            logger.info("📸 私海线索页面加载截图已保存")
            
            logger.info("🎉 私海线索页面导航完成！")
            return True
        else:
            logger.error("❌ 未能成功进入私海线索页面")
            try:
                driver.save_screenshot("screenshots/private_sea_page_verify_failed.png")
                logger.info("📸 页面验证失败截图已保存")
            except:
                pass
            return False
        
    except Exception as e:
        logger.error(f"导航到私海线索页面异常: {e}")
        try:
            driver.save_screenshot("screenshots/navigate_private_sea_error.png")
        except:
            pass
        return False


def add_private_sea_clue(driver):
    """
    添加私海线索功能（仅添加线索，不包含页面导航）
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        tuple: (成功状态, 客户名称, 电话号码)
    """
    try:
        logger.info("📝 开始添加私海线索...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 点击添加线索按钮
        logger.info("点击添加线索按钮...")
        
        # 首先尝试已知有效的定位器
        try:
            add_clue_button = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-v-f2b64f12 and contains(@class, 'el-button--primary') and contains(@class, 'el-button--mini')]"))
            )
            add_clue_button.click()
            logger.info("✅ 添加线索按钮已点击")
        except:
            # 备用JavaScript方案
            logger.info("使用JavaScript查找添加线索按钮...")
            js_click_add_button = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                var btn = buttons[i];
                if (btn.textContent.includes('添加线索') && 
                    btn.offsetWidth > 0 && 
                    btn.offsetHeight > 0) {
                    btn.click();
                    return true;
                }
            }
            return false;
            """
            
            if driver.execute_script(js_click_add_button):
                logger.info("✅ 使用JavaScript成功点击添加线索按钮")
            else:
                raise Exception("无法找到添加线索按钮")
        
        # 等待添加线索面板出现
        time.sleep(2)
        
        # 生成随机数据
        random_suffix = generate_random_suffix()
        random_phone = generate_random_phone()
        customer_name = f"私海线索-ui自动化{random_suffix}"
        
        logger.info(f"📝 生成的测试数据:")
        logger.info(f"   客户名称: {customer_name}")
        logger.info(f"   联系人: 秦仁驰")
        logger.info(f"   电话: {random_phone}")
        logger.info(f"   业务类型: 1")
        logger.info(f"   业务需求: 1")
        
        # 填写客户名称
        logger.info("填写客户名称...")
        customer_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入客户名称']"))
        )
        customer_name_input.clear()
        customer_name_input.send_keys(customer_name)
        logger.info("✅ 客户名称已填写")
        
        # 填写联系人
        logger.info("填写联系人...")
        contact_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入联系人']"))
        )
        contact_input.clear()
        contact_input.send_keys("秦仁驰")
        logger.info("✅ 联系人已填写")
        
        # 填写电话
        logger.info("填写电话...")
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入电话']"))
        )
        phone_input.clear()
        phone_input.send_keys(random_phone)
        logger.info("✅ 电话已填写")
        
        # 填写业务类型
        logger.info("填写业务类型...")
        business_type_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入业务类型']"))
        )
        business_type_input.clear()
        business_type_input.send_keys("1")
        logger.info("✅ 业务类型已填写")
        
        # 填写业务需求
        logger.info("填写业务需求...")
        business_demand_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入业务需求']"))
        )
        business_demand_input.clear()
        business_demand_input.send_keys("1")
        logger.info("✅ 业务需求已填写")
        
        # 等待一下确保所有输入都完成
        time.sleep(1)
        
        # 点击确定按钮
        logger.info("点击确定按钮...")
        
        # 直接使用JavaScript方案（已验证有效）
        js_click_confirm = """
        var buttons = document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            var text = btn.textContent.trim();
            if ((text === '确定' || text === '确 定') && 
                btn.offsetWidth > 0 && 
                btn.offsetHeight > 0 &&
                !btn.disabled) {
                btn.click();
                return true;
            }
        }
        return false;
        """
        
        if driver.execute_script(js_click_confirm):
            logger.info("✅ 确定按钮已点击")
        else:
            raise Exception("无法找到确定按钮")
        
        # 等待操作完成
        time.sleep(3)
        
        # 截图确认结果
        driver.save_screenshot("screenshots/private_sea_clue_added.png")
        logger.info("📸 私海线索添加截图已保存")
        
        logger.info("🎉 私海线索添加完成！")
        return True, customer_name, random_phone
        
    except Exception as e:
        logger.error(f"私海线索添加异常: {e}")
        try:
            driver.save_screenshot("screenshots/private_sea_clue_error.png")
        except:
            pass
        return False, None, None


def test_private_sea_add_workflow(driver):
    """
    完整的私海线索添加测试流程
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🚀 开始私海线索添加测试流程...")
        
        # 步骤1: 导航到私海线索页面
        if not navigate_to_private_sea(driver):
            logger.error("❌ 导航到私海线索页面失败")
            return False
        
        # 步骤2: 添加私海线索
        success, customer_name, phone = add_private_sea_clue(driver)
        if not success:
            logger.error("❌ 添加私海线索失败")
            return False
        
        logger.info("🎉 私海线索添加测试流程完成！")
        logger.info(f"   ✅ 客户名称: {customer_name}")
        logger.info(f"   ✅ 电话号码: {phone}")
        
        return True
        
    except Exception as e:
        logger.error(f"私海线索添加测试流程异常: {e}")
        return False 