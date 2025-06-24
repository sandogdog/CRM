#!/usr/bin/env python
"""
CRM自动化测试 - 私海线索功能模块
包含私海线索添加和快速跟进相关功能
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crm_utils import generate_random_phone, generate_random_suffix

# 配置日志
logger = logging.getLogger(__name__)


def add_private_sea_clue(driver):
    """
    添加私海线索功能
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        tuple: (成功状态, 客户名称, 电话号码)
    """
    try:
        logger.info("🔍 开始私海线索测试...")
        
        # 等待页面加载完成
        time.sleep(3)
        
        # 步骤1: 点击私海线索菜单
        logger.info("1. 点击私海线索菜单...")
        
        # 使用已知有效的定位器
        private_sea_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'el-menu-item') and contains(@base-path, '/customerManagement/clews/privateSea')]"))
        )
        private_sea_menu.click()
        logger.info("✅ 私海线索菜单已点击")
        
        # 等待页面跳转和加载
        time.sleep(3)
        
        # 步骤2: 点击添加线索按钮
        logger.info("2. 点击添加线索按钮...")
        
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
        
        # 步骤3: 填写客户名称
        logger.info("3. 填写客户名称...")
        customer_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入客户名称']"))
        )
        customer_name_input.clear()
        customer_name_input.send_keys(customer_name)
        logger.info("✅ 客户名称已填写")
        
        # 步骤4: 填写联系人
        logger.info("4. 填写联系人...")
        contact_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入联系人']"))
        )
        contact_input.clear()
        contact_input.send_keys("秦仁驰")
        logger.info("✅ 联系人已填写")
        
        # 步骤5: 填写电话
        logger.info("5. 填写电话...")
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入电话']"))
        )
        phone_input.clear()
        phone_input.send_keys(random_phone)
        logger.info("✅ 电话已填写")
        
        # 步骤6: 填写业务类型
        logger.info("6. 填写业务类型...")
        business_type_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入业务类型']"))
        )
        business_type_input.clear()
        business_type_input.send_keys("1")
        logger.info("✅ 业务类型已填写")
        
        # 步骤7: 填写业务需求
        logger.info("7. 填写业务需求...")
        business_demand_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入业务需求']"))
        )
        business_demand_input.clear()
        business_demand_input.send_keys("1")
        logger.info("✅ 业务需求已填写")
        
        # 等待一下确保所有输入都完成
        time.sleep(1)
        
        # 步骤8: 点击确定按钮
        logger.info("8. 点击确定按钮...")
        
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


def click_quick_follow_up(driver):
    """
    点击第一行线索的快速跟进按钮
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 快速跟进按钮点击是否成功
    """
    try:
        logger.info("🔍 开始点击快速跟进按钮...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 使用JavaScript查找并点击第一个快速跟进按钮
        logger.info("正在定位快速跟进按钮...")
        js_click_quick_follow = """
        // 查找所有包含"快速跟进"文本的按钮
        var buttons = document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            var span = btn.querySelector('span');
            if (span && span.textContent.trim() === '快速跟进' && 
                btn.offsetWidth > 0 && 
                btn.offsetHeight > 0 &&
                !btn.disabled) {
                console.log('找到快速跟进按钮，准备点击');
                btn.click();
                return true;
            }
        }
        return false;
        """
        
        if driver.execute_script(js_click_quick_follow):
            logger.info("✅ 快速跟进按钮已点击")
            
            # 等待弹窗出现
            time.sleep(2)
            
            # 截图确认结果
            driver.save_screenshot("screenshots/quick_follow_up_clicked.png")
            logger.info("📸 快速跟进点击截图已保存")
            
            logger.info("🎉 快速跟进按钮点击完成！")
            return True
        else:
            logger.error("❌ 无法找到快速跟进按钮")
            return False
        
    except Exception as e:
        logger.error(f"点击快速跟进按钮异常: {e}")
        try:
            driver.save_screenshot("screenshots/quick_follow_up_error.png")
        except:
            pass
        return False 