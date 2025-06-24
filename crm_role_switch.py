#!/usr/bin/env python
"""
CRM自动化测试 - 职位切换功能模块
包含用户职位切换相关功能
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置日志
logger = logging.getLogger(__name__)


def switch_role_fixed_v2(driver):
    """
    修复版职位切换操作 v2
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 职位切换是否成功
    """
    try:
        logger.info("🔄 开始职位切换（修复版v2）...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 步骤1: 点击下拉箭头按钮
        logger.info("1. 点击下拉箭头...")
        dropdown_arrow = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "i.el-icon-arrow-down.el-icon--right"))
        )
        dropdown_arrow.click()
        logger.info("✅ 下拉箭头已点击")
        
        time.sleep(1)
        
        # 步骤2: 点击切换按钮
        logger.info("2. 点击切换按钮...")
        switch_button = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'el-dropdown-menu__item') and contains(text(), '切换')]"))
        )
        switch_button.click()
        logger.info("✅ 切换按钮已点击")
        
        # 等待切换对话框出现
        time.sleep(2)
        
        # 步骤3: 点击选择框打开下拉列表
        logger.info("3. 打开账号选择下拉...")
        try:
            # 尝试点击输入框
            select_input = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-select .el-input__inner"))
            )
            select_input.click()
            logger.info("✅ 选择框已点击")
        except:
            # 如果输入框不可用，点击箭头
            select_arrow = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "i.el-select__caret"))
            )
            select_arrow.click()
            logger.info("✅ 选择箭头已点击")
        
        time.sleep(2)  # 等待下拉列表完全展开
        
        # 步骤4: 选择账号（更精确的定位）
        logger.info("4. 选择账号...")
        
        # 使用更精确的JavaScript代码，只在下拉选项中查找
        js_select_account = """
        // 只在下拉选项中查找，避免点击其他地方的文本
        var dropdownItems = document.querySelectorAll('.el-select-dropdown__item, li.el-select-dropdown__item');
        console.log('找到下拉选项数量:', dropdownItems.length);
        
        for (var i = 0; i < dropdownItems.length; i++) {
            var item = dropdownItems[i];
            console.log('选项', i, ':', item.textContent);
            
            if (item.textContent.includes('秦仁驰') && 
                item.textContent.includes('15271193874') && 
                item.offsetWidth > 0 && 
                item.offsetHeight > 0) {
                console.log('找到目标账号，准备点击');
                item.click();
                return true;
            }
        }
        
        // 如果上面没找到，尝试更广泛的查找
        var allElements = document.querySelectorAll('li, span');
        for (var j = 0; j < allElements.length; j++) {
            var el = allElements[j];
            if (el.textContent.includes('秦仁驰') && 
                el.textContent.includes('15271193874') && 
                el.offsetWidth > 0 && 
                el.offsetHeight > 0 &&
                !el.textContent.includes('切换')) {  // 排除切换按钮
                console.log('在广泛搜索中找到目标账号');
                el.click();
                return true;
            }
        }
        
        return false;
        """
        
        account_selected = driver.execute_script(js_select_account)
        if account_selected:
            logger.info("✅ 账号已选择")
        else:
            logger.warning("⚠️ 账号选择失败，尝试备用方案...")
            
            # 备用方案：使用Selenium定位
            try:
                account_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), '秦仁驰') and contains(text(), '15271193874')]"))
                )
                account_option.click()
                logger.info("✅ 账号已选择（备用方案）")
            except Exception as e:
                logger.error(f"❌ 账号选择完全失败: {e}")
                # 继续尝试确定按钮
        
        time.sleep(1)
        
        # 步骤5: 点击确定按钮
        logger.info("5. 点击确定按钮...")
        
        # 更精确的确定按钮定位
        js_click_confirm = """
        var buttons = document.querySelectorAll('button.el-button--primary');
        console.log('找到主要按钮数量:', buttons.length);
        
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            console.log('按钮', i, ':', btn.textContent.trim());
            
            if (btn.textContent.trim() === '确定' && 
                btn.offsetWidth > 0 && 
                btn.offsetHeight > 0 &&
                !btn.disabled) {
                console.log('找到确定按钮，准备点击');
                btn.click();
                return true;
            }
        }
        return false;
        """
        
        confirm_clicked = driver.execute_script(js_click_confirm)
        if confirm_clicked:
            logger.info("✅ 确定按钮已点击")
        else:
            # 备用方案：使用Selenium定位
            try:
                confirm_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(text(), '确定')]"))
                )
                confirm_button.click()
                logger.info("✅ 确定按钮已点击（备用方案）")
            except Exception as e:
                logger.error(f"❌ 确定按钮点击失败: {e}")
                return False
        
        # 等待操作完成
        time.sleep(2)
        
        # 截图确认结果
        driver.save_screenshot("screenshots/role_switch_fixed_v2_completed.png")
        logger.info("📸 截图已保存")
        
        logger.info("🎉 职位切换完成！")
        return True
        
    except Exception as e:
        logger.error(f"职位切换异常: {e}")
        try:
            driver.save_screenshot("screenshots/role_switch_fixed_v2_error.png")
        except:
            pass
        return False 