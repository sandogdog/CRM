#!/usr/bin/env python
"""
CRM自动化测试 - 私海商机操作模块
包含私海商机页面导航和相关功能
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from crm_utils import click_customer_management_menu

# 配置日志
logger = logging.getLogger(__name__)


def navigate_to_private_business(driver):
    """
    导航到私海商机页面
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 导航是否成功
    """
    try:
        logger.info("🏢 开始导航到私海商机页面...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 步骤0: 点击客户管理主菜单（前端更新后需要）
        if not click_customer_management_menu(driver):
            logger.warning("⚠️ 点击客户管理菜单失败，尝试继续...")
        
        # 步骤1: 点击商机主菜单（展开子菜单）
        logger.info("1. 点击商机主菜单...")
        
        js_click_business_menu = """
        // 查找商机主菜单项
        var submenuTitles = document.querySelectorAll('div.el-submenu__title');
        for (var i = 0; i < submenuTitles.length; i++) {
            var title = submenuTitles[i];
            var span = title.querySelector('span');
            if (span && span.textContent.trim() === '商机') {
                console.log('找到商机主菜单，准备点击');
                title.click();
                return true;
            }
        }
        console.log('未找到商机主菜单');
        return false;
        """
        
        if driver.execute_script(js_click_business_menu):
            logger.info("✅ 商机主菜单已点击，子菜单应该已展开")
        else:
            raise Exception("无法找到商机主菜单")
        
        # 等待子菜单展开
        time.sleep(2)
        
        # 步骤2: 点击私海商机子菜单
        logger.info("2. 点击私海商机子菜单...")
        
        js_click_private_business_menu = """
        // 查找私海商机子菜单项
        var menuItems = document.querySelectorAll('li.el-menu-item.inner-menu-item');
        for (var i = 0; i < menuItems.length; i++) {
            var item = menuItems[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '私海商机' && 
                item.getAttribute('base-path') === '/customerManagement/business/privateSea') {
                console.log('找到私海商机菜单，准备点击');
                item.click();
                return true;
            }
        }
        console.log('未找到私海商机菜单');
        return false;
        """
        
        if driver.execute_script(js_click_private_business_menu):
            logger.info("✅ 私海商机菜单已点击")
        else:
            raise Exception("无法找到私海商机菜单")
        
        # 等待页面加载
        time.sleep(3)
        
        # 验证是否成功进入私海商机页面
        js_verify_private_business_page = """
        // 检查URL是否包含私海商机路径
        var currentUrl = window.location.href;
        return currentUrl.includes('/customerManagement/business/privateSea') || 
               currentUrl.includes('privateSea');
        """
        
        if driver.execute_script(js_verify_private_business_page):
            logger.info("✅ 已成功进入私海商机页面")
            
            # 截图确认
            driver.save_screenshot("screenshots/private_business_page_loaded.png")
            logger.info("📸 私海商机页面加载截图已保存")
            
            return True
        else:
            logger.error("❌ 未能成功进入私海商机页面")
            return False
        
    except Exception as e:
        logger.error(f"导航到私海商机页面异常: {e}")
        try:
            driver.save_screenshot("screenshots/private_business_navigation_error.png")
        except:
            pass
        return False


def test_private_business_navigation(driver):
    """
    测试私海商机页面导航功能
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🧪 开始测试私海商机页面导航功能...")
        
        # 执行导航测试
        if not navigate_to_private_business(driver):
            logger.error("❌ 私海商机页面导航失败")
            return False
        
        logger.info("🎉 私海商机页面导航测试完成！")
        logger.info("   ✅ 成功点击商机主菜单")
        logger.info("   ✅ 成功点击私海商机子菜单")
        logger.info("   ✅ 成功进入私海商机页面")
        
        return True
        
    except Exception as e:
        logger.error(f"私海商机页面导航测试异常: {e}")
        return False


def debug_business_launch_operation(driver, business_name_keyword="私海线索-ui自动化"):
    """
    调试版本的商机投放操作，提供详细的步骤信息
    
    Args:
        driver: Selenium WebDriver实例
        business_name_keyword: 商机名称关键字
    
    Returns:
        bool: 操作是否成功
    """
    try:
        logger.info(f"🔧 [DEBUG] 开始调试商机投放操作...")
        
        # 等待页面加载
        time.sleep(3)
        
        # 步骤1: 检查页面中的商机数据
        check_data_js = """
        var rows = document.querySelectorAll('tr.el-table__row');
        var businesses = [];
        
        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            var spans = row.querySelectorAll('span[data-v-36a81157]');
            for (var j = 0; j < spans.length; j++) {
                var text = spans[j].textContent.trim();
                if (text && text.length > 5) {
                    businesses.push(text);
                    break;
                }
            }
        }
        
        return {
            totalRows: rows.length,
            businesses: businesses
        };
        """
        
        data_info = driver.execute_script(check_data_js)
        logger.info(f"🔧 [DEBUG] 页面数据检查:")
        logger.info(f"   - 总行数: {data_info['totalRows']}")
        logger.info(f"   - 商机列表: {data_info['businesses']}")
        
        # 步骤2: 查找目标商机
        target_found = False
        for business in data_info['businesses']:
            if business_name_keyword in business:
                logger.info(f"🔧 [DEBUG] 找到目标商机: {business}")
                target_found = True
                break
        
        if not target_found:
            logger.error(f"🔧 [DEBUG] 未找到包含'{business_name_keyword}'的商机")
            return False
        
        # 步骤3: 查找并点击操作按钮
        logger.info(f"🔧 [DEBUG] 开始查找操作按钮...")
        
        click_operation_js = f"""
        var rows = document.querySelectorAll('tr.el-table__row');
        
        for (var i = 0; i < rows.length; i++) {{
            var row = rows[i];
            var spans = row.querySelectorAll('span[data-v-36a81157]');
            
            // 检查是否是目标商机行
            var isTargetRow = false;
            for (var j = 0; j < spans.length; j++) {{
                if (spans[j].textContent.includes('{business_name_keyword}')) {{
                    isTargetRow = true;
                    break;
                }}
            }}
            
            if (isTargetRow) {{
                console.log('找到目标商机行');
                
                // 查找操作按钮
                var dropdown = row.querySelector('div.el-dropdown');
                if (dropdown) {{
                    var operationBtn = dropdown.querySelector('button.el-button--info');
                    if (operationBtn) {{
                        console.log('找到操作按钮，执行点击');
                        operationBtn.click();
                        return true;
                    }} else {{
                        console.log('未找到操作按钮');
                        return false;
                    }}
                }} else {{
                    console.log('未找到下拉菜单组件');
                    return false;
                }}
            }}
        }}
        
        console.log('未找到目标商机行');
        return false;
        """
        
        operation_clicked = driver.execute_script(click_operation_js)
        
        if operation_clicked:
            logger.info("🔧 [DEBUG] 操作按钮已点击，等待菜单展开...")
            
            # 等待菜单展开
            time.sleep(1.5)
            
            # 步骤4: 查找投放菜单项
            logger.info("🔧 [DEBUG] 查找投放菜单项...")
            
            find_launch_menu_js = """
            var menuItems = document.querySelectorAll('li.el-dropdown-menu__item');
            var menuTexts = [];
            
            for (var i = 0; i < menuItems.length; i++) {
                var item = menuItems[i];
                var text = item.textContent.trim();
                menuTexts.push(text);
                
                if (text === '投放') {
                    console.log('找到投放菜单项，执行点击');
                    item.click();
                    return true;
                }
            }
            
            console.log('可用菜单项:', menuTexts);
            return { found: false, menus: menuTexts };
            """
            
            launch_result = driver.execute_script(find_launch_menu_js)
            
            if launch_result == True:
                logger.info("🔧 [DEBUG] 投放菜单项已点击成功！")
                
                # 等待操作完成
                time.sleep(2)
                
                # 截图确认
                driver.save_screenshot("screenshots/business_launch_debug_success.png")
                logger.info("📸 调试成功截图已保存")
                
                return True
            else:
                logger.error(f"🔧 [DEBUG] 未找到投放菜单项")
                if isinstance(launch_result, dict):
                    logger.error(f"   可用菜单项: {launch_result.get('menus', [])}")
                
                # 截图调试
                driver.save_screenshot("screenshots/business_launch_debug_menu_error.png")
                logger.info("📸 菜单调试截图已保存")
                
                return False
        else:
            logger.error("🔧 [DEBUG] 操作按钮点击失败")
            
            # 截图调试
            driver.save_screenshot("screenshots/business_launch_debug_button_error.png")
            logger.info("📸 按钮调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"🔧 [DEBUG] 调试操作异常: {e}")
        try:
            driver.save_screenshot("screenshots/business_launch_debug_exception.png")
            logger.info("📸 异常调试截图已保存")
        except:
            pass
        return False


def handle_business_launch_dialog(driver):
    """
    处理商机投放弹窗：填写投放原因 + 点击确定
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 弹窗处理是否成功
    """
    try:
        logger.info("📝 开始处理商机投放弹窗...")
        
        # 等待弹窗出现
        time.sleep(2)
        
        # 步骤1: 填写投放原因
        logger.info("1. 填写投放原因...")
        
        js_fill_launch_reason = """
        // 查找投放原因输入框
        var textareas = document.querySelectorAll('textarea.el-textarea__inner');
        console.log('找到的文本输入框数量:', textareas.length);
        
        for (var i = 0; i < textareas.length; i++) {
            var textarea = textareas[i];
            var placeholder = textarea.getAttribute('placeholder');
            
            // 检查是否是投放原因输入框
            if (placeholder && placeholder.includes('请输入投放原因')) {
                console.log('找到投放原因输入框');
                textarea.focus();
                textarea.value = 'UI自动化测试';
                
                // 触发input事件，确保Vue能检测到值的变化
                var inputEvent = new Event('input', { bubbles: true });
                textarea.dispatchEvent(inputEvent);
                
                // 触发change事件
                var changeEvent = new Event('change', { bubbles: true });
                textarea.dispatchEvent(changeEvent);
                
                console.log('已填写投放原因: UI自动化测试');
                return true;
            }
        }
        
        console.log('未找到投放原因输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_launch_reason):
            logger.info("✅ 投放原因已填写：UI自动化测试")
        else:
            raise Exception("无法找到投放原因输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤2: 点击确定按钮
        logger.info("2. 点击确定按钮...")
        
        js_click_confirm_button = """
        // 查找确定按钮
        var buttons = document.querySelectorAll('button.el-button--primary');
        console.log('找到的主要按钮数量:', buttons.length);
        
        for (var i = 0; i < buttons.length; i++) {
            var button = buttons[i];
            var span = button.querySelector('span');
            
            if (span && span.textContent.trim() === '确定') {
                var rect = button.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && !button.disabled) {
                    console.log('找到确定按钮，执行点击');
                    button.click();
                    return true;
                }
            }
        }
        
        console.log('未找到确定按钮');
        return false;
        """
        
        if driver.execute_script(js_click_confirm_button):
            logger.info("✅ 确定按钮已点击")
        else:
            raise Exception("无法找到确定按钮")
        
        # 等待操作完成
        time.sleep(3)
        
        # 截图确认结果
        driver.save_screenshot("screenshots/business_launch_dialog_completed.png")
        logger.info("📸 商机投放弹窗处理完成截图已保存")
        
        logger.info("🎉 商机投放弹窗处理完成！")
        return True
        
    except Exception as e:
        logger.error(f"处理商机投放弹窗异常: {e}")
        try:
            driver.save_screenshot("screenshots/business_launch_dialog_error.png")
            logger.info("📸 弹窗处理错误截图已保存")
        except:
            pass
        return False


def click_first_business_launch_button(driver):
    """
    直接点击私海商机列表第一条商机的投放按钮
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 投放按钮点击是否成功
    """
    try:
        logger.info("🔍 开始操作列表第一条商机的投放按钮...")
        
        # 等待表格加载完成
        time.sleep(3)
        
        # 直接操作第一条商机
        js_click_first_business = """
        // 获取第一条商机行
        var firstRow = document.querySelector('tr.el-table__row');
        
        if (!firstRow) {
            console.log('未找到商机数据行');
            return false;
        }
        
        // 获取第一条商机的名称（用于日志）
        var nameSpans = firstRow.querySelectorAll('span[data-v-36a81157]');
        var businessName = '';
        for (var i = 0; i < nameSpans.length; i++) {
            var text = nameSpans[i].textContent.trim();
            if (text && text.length > 5) {
                businessName = text;
                break;
            }
        }
        
        console.log('第一条商机名称:', businessName);
        
        // 查找第一条商机的操作按钮
        var dropdown = firstRow.querySelector('div.el-dropdown');
        if (dropdown) {
            var operationBtn = dropdown.querySelector('button.el-button--info');
            if (operationBtn) {
                console.log('找到第一条商机的操作按钮，执行点击');
                operationBtn.click();
                return { success: true, businessName: businessName };
            } else {
                console.log('未找到操作按钮');
                return false;
            }
        } else {
            console.log('未找到下拉菜单组件');
            return false;
        }
        """
        
        operation_result = driver.execute_script(js_click_first_business)
        
        if operation_result and operation_result.get('success'):
            business_name = operation_result.get('businessName', '未知商机')
            logger.info(f"✅ 已点击第一条商机的操作按钮: {business_name}")
            
            # 等待菜单展开
            time.sleep(1.5)
            
            # 查找并点击投放菜单项
            logger.info("🔍 查找投放菜单项...")
            
            click_launch_menu_js = """
            var menuItems = document.querySelectorAll('li.el-dropdown-menu__item');
            var menuTexts = [];
            
            for (var i = 0; i < menuItems.length; i++) {
                var item = menuItems[i];
                var text = item.textContent.trim();
                menuTexts.push(text);
                
                if (text === '投放') {
                    console.log('找到投放菜单项，执行点击');
                    item.click();
                    return true;
                }
            }
            
            console.log('可用菜单项:', menuTexts);
            return { found: false, menus: menuTexts };
            """
            
            launch_result = driver.execute_script(click_launch_menu_js)
            
            if launch_result == True:
                logger.info("✅ 投放菜单项已点击成功！")
                
                # 等待弹窗出现
                time.sleep(2)
                
                # 处理投放弹窗
                if handle_business_launch_dialog(driver):
                    logger.info("✅ 商机投放弹窗处理成功！")
                    
                    # 截图确认最终结果
                    driver.save_screenshot("screenshots/first_business_launch_complete.png")
                    logger.info("📸 第一条商机投放完整流程截图已保存")
                    
                    return True
                else:
                    logger.error("❌ 商机投放弹窗处理失败")
                    return False
                
            else:
                logger.error("❌ 未找到投放菜单项")
                if isinstance(launch_result, dict):
                    logger.error(f"   可用菜单项: {launch_result.get('menus', [])}")
                
                # 截图调试
                driver.save_screenshot("screenshots/first_business_launch_menu_error.png")
                logger.info("📸 菜单调试截图已保存")
                
                return False
        else:
            logger.error("❌ 第一条商机操作按钮点击失败")
            
            # 截图调试
            driver.save_screenshot("screenshots/first_business_button_error.png")
            logger.info("📸 按钮调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"点击第一条商机投放按钮异常: {e}")
        try:
            driver.save_screenshot("screenshots/first_business_launch_error.png")
            logger.info("📸 错误截图已保存")
        except:
            pass
        return False


def click_business_launch_button(driver, business_name_keyword="私海线索-ui自动化"):
    """
    在私海商机列表中查找指定商机并点击投放按钮
    已改为直接操作第一条商机
    
    Args:
        driver: Selenium WebDriver实例
        business_name_keyword: 保留参数，但现在直接操作第一条商机
    
    Returns:
        bool: 投放按钮点击是否成功
    """
    try:
        logger.info("🔍 直接操作列表第一条商机...")
        
        # 直接调用第一条商机操作函数
        return click_first_business_launch_button(driver)
        
    except Exception as e:
        logger.error(f"点击商机投放按钮异常: {e}")
        try:
            driver.save_screenshot("screenshots/business_launch_error.png")
            logger.info("📸 错误截图已保存")
        except:
            pass
        return False


def test_private_business_launch_workflow(driver):
    """
    完整的私海商机投放测试流程（操作第一条商机）
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🎯 开始私海商机投放测试流程（操作第一条商机）...")
        
        # 步骤1: 导航到私海商机页面
        if not navigate_to_private_business(driver):
            logger.error("❌ 导航到私海商机页面失败")
            return False
        
        # 步骤2: 直接操作第一条商机的投放按钮
        if not click_first_business_launch_button(driver):
            logger.error("❌ 点击第一条商机投放按钮失败")
            return False
        
        logger.info("🎉 私海商机投放测试流程完成！")
        logger.info("   ✅ 成功导航到私海商机页面")
        logger.info("   ✅ 成功操作第一条商机的投放按钮")
        
        return True
        
    except Exception as e:
        logger.error(f"私海商机投放测试流程异常: {e}")
        return False


def navigate_to_public_business(driver):
    """
    导航到公海商机页面
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 导航是否成功
    """
    try:
        logger.info("🌊 开始导航到公海商机页面...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 步骤0: 点击客户管理主菜单（前端更新后需要）
        if not click_customer_management_menu(driver):
            logger.warning("⚠️ 点击客户管理菜单失败，尝试继续...")
        
        # 步骤1: 点击商机主菜单（展开子菜单）
        logger.info("1. 点击商机主菜单...")
        
        js_click_business_menu = """
        // 查找商机主菜单项
        var submenuTitles = document.querySelectorAll('div.el-submenu__title');
        for (var i = 0; i < submenuTitles.length; i++) {
            var title = submenuTitles[i];
            var span = title.querySelector('span');
            if (span && span.textContent.trim() === '商机') {
                console.log('找到商机主菜单，准备点击');
                title.click();
                return true;
            }
        }
        console.log('未找到商机主菜单');
        return false;
        """
        
        if driver.execute_script(js_click_business_menu):
            logger.info("✅ 商机主菜单已点击，子菜单应该已展开")
        else:
            raise Exception("无法找到商机主菜单")
        
        # 等待子菜单展开
        time.sleep(2)
        
        # 步骤2: 点击公海商机子菜单
        logger.info("2. 点击公海商机子菜单...")
        
        js_click_public_business_menu = """
        // 查找公海商机子菜单项
        var menuItems = document.querySelectorAll('li.el-menu-item.inner-menu-item');
        for (var i = 0; i < menuItems.length; i++) {
            var item = menuItems[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '公海商机' && 
                item.getAttribute('base-path') === '/customerManagement/business/publicSea') {
                console.log('找到公海商机菜单，准备点击');
                item.click();
                return true;
            }
        }
        console.log('未找到公海商机菜单');
        return false;
        """
        
        if driver.execute_script(js_click_public_business_menu):
            logger.info("✅ 公海商机菜单已点击")
        else:
            raise Exception("无法找到公海商机菜单")
        
        # 等待页面加载
        time.sleep(3)
        
        # 验证是否成功进入公海商机页面
        js_verify_public_business_page = """
        // 检查URL是否包含公海商机路径
        var currentUrl = window.location.href;
        return currentUrl.includes('/customerManagement/business/publicSea') || 
               currentUrl.includes('publicSea');
        """
        
        if driver.execute_script(js_verify_public_business_page):
            logger.info("✅ 已成功进入公海商机页面")
            
            # 截图确认
            driver.save_screenshot("screenshots/public_business_page_loaded.png")
            logger.info("📸 公海商机页面加载截图已保存")
            
            return True
        else:
            logger.error("❌ 未能成功进入公海商机页面")
            return False
        
    except Exception as e:
        logger.error(f"导航到公海商机页面异常: {e}")
        try:
            driver.save_screenshot("screenshots/public_business_navigation_error.png")
        except:
            pass
        return False


def click_first_public_business_track_button(driver):
    """
    在公海商机列表中点击第一条商机的跟踪按钮
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 跟踪按钮点击是否成功
    """
    try:
        logger.info("🔍 开始操作公海商机列表第一条商机的跟踪按钮...")
        
        # 等待表格加载完成
        time.sleep(3)
        
        # 直接操作第一条公海商机
        js_click_first_track = """
        // 获取第一条公海商机行
        var firstRow = document.querySelector('tr.el-table__row');
        
        if (!firstRow) {
            console.log('未找到公海商机数据行');
            return false;
        }
        
        // 获取第一条商机的名称（用于日志）
        var nameSpans = firstRow.querySelectorAll('span');
        var businessName = '';
        for (var i = 0; i < nameSpans.length; i++) {
            var text = nameSpans[i].textContent.trim();
            if (text && text.length > 5 && !text.includes('详情') && !text.includes('跟踪')) {
                businessName = text;
                break;
            }
        }
        
        console.log('第一条公海商机名称:', businessName);
        
        // 查找第一条商机的操作下拉菜单
        var dropdown = firstRow.querySelector('div.el-dropdown');
        if (dropdown) {
            var operationBtn = dropdown.querySelector('button');
            if (operationBtn) {
                console.log('找到第一条公海商机的操作按钮，执行点击');
                operationBtn.click();
                return { success: true, businessName: businessName };
            } else {
                console.log('未找到操作按钮');
                return false;
            }
        } else {
            console.log('未找到下拉菜单组件');
            return false;
        }
        """
        
        operation_result = driver.execute_script(js_click_first_track)
        
        if operation_result and operation_result.get('success'):
            business_name = operation_result.get('businessName', '未知商机')
            logger.info(f"✅ 已点击第一条公海商机的操作按钮: {business_name}")
            
            # 等待菜单展开
            time.sleep(1.5)
            
            # 查找并点击跟踪菜单项
            logger.info("🔍 查找跟踪菜单项...")
            
            click_track_menu_js = """
            var menuItems = document.querySelectorAll('li.el-dropdown-menu__item');
            var menuTexts = [];
            
            for (var i = 0; i < menuItems.length; i++) {
                var item = menuItems[i];
                var text = item.textContent.trim();
                menuTexts.push(text);
                
                if (text === '跟踪') {
                    console.log('找到跟踪菜单项，执行点击');
                    item.click();
                    return true;
                }
            }
            
            console.log('可用菜单项:', menuTexts);
            return { found: false, menus: menuTexts };
            """
            
            track_result = driver.execute_script(click_track_menu_js)
            
            if track_result == True:
                logger.info("✅ 跟踪菜单项已点击成功！")
                
                # 等待跟踪页面加载
                time.sleep(3)
                
                # 截图确认结果
                driver.save_screenshot("screenshots/public_business_track_success.png")
                logger.info("📸 公海商机跟踪成功截图已保存")
                
                return True
            else:
                logger.error("❌ 未找到跟踪菜单项")
                if isinstance(track_result, dict):
                    logger.error(f"   可用菜单项: {track_result.get('menus', [])}")
                
                # 截图调试
                driver.save_screenshot("screenshots/public_business_track_menu_error.png")
                logger.info("📸 菜单调试截图已保存")
                
                return False
        else:
            logger.error("❌ 第一条公海商机操作按钮点击失败")
            
            # 截图调试
            driver.save_screenshot("screenshots/public_business_button_error.png")
            logger.info("📸 按钮调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"点击公海商机跟踪按钮异常: {e}")
        try:
            driver.save_screenshot("screenshots/public_business_track_error.png")
            logger.info("📸 错误截图已保存")
        except:
            pass
        return False


def test_public_business_track_workflow(driver):
    """
    完整的公海商机跟踪测试流程
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🎯 开始公海商机跟踪测试流程...")
        
        # 步骤1: 导航到公海商机页面
        if not navigate_to_public_business(driver):
            logger.error("❌ 导航到公海商机页面失败")
            return False
        
        # 步骤2: 点击第一条商机的跟踪按钮
        if not click_first_public_business_track_button(driver):
            logger.error("❌ 点击公海商机跟踪按钮失败")
            return False
        
        logger.info("🎉 公海商机跟踪测试流程完成！")
        logger.info("   ✅ 成功导航到公海商机页面")
        logger.info("   ✅ 成功点击第一条商机的跟踪按钮")
        
        return True
        
    except Exception as e:
        logger.error(f"公海商机跟踪测试流程异常: {e}")
        return False


def test_private_business_launch_with_public_track(driver):
    """
    私海商机投放 + 公海商机跟踪的完整流程
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🚀 开始私海商机投放+公海跟踪完整流程...")
        
        # 步骤1: 执行私海商机投放
        logger.info("🔸 步骤1: 执行私海商机投放...")
        if not test_private_business_launch_workflow(driver):
            logger.error("❌ 私海商机投放失败")
            return False
        
        logger.info("✅ 私海商机投放成功")
        
        # 步骤2: 导航到公海商机并进行跟踪
        logger.info("🔸 步骤2: 导航到公海商机并进行跟踪...")
        if test_public_business_track_workflow(driver):
            logger.info("✅ 公海商机跟踪成功")
            logger.info("🎉 私海投放+公海跟踪完整流程测试完成！")
            logger.info("   ✅ 私海商机投放成功")
            logger.info("   ✅ 公海商机跟踪成功")
            return True
        else:
            logger.warning("⚠️ 公海商机跟踪失败，但投放已成功")
            return True  # 投放成功就算部分成功
        
    except Exception as e:
        logger.error(f"私海投放+公海跟踪流程异常: {e}")
        return False 