#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CRM客户公海领取测试模块
功能：导航到客户公海页面，通过用户ID查询客户并执行领取操作
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crm_utils import click_customer_management_menu

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crm_test.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def _input_user_id_in_dialog(driver, user_id):
    """
    在弹窗中输入用户ID的辅助函数
    
    Args:
        driver: WebDriver实例
        user_id: 要输入的用户ID
        
    Returns:
        bool: 输入是否成功
    """
    try:
        js_input_user_id = """
        // 查找弹窗中的输入框 - 增强调试版
        console.log('=== 开始查找输入框 ===');
        
        // 首先检查所有弹窗
        var dialogs = document.querySelectorAll('.el-dialog');
        console.log('页面中所有弹窗数量:', dialogs.length);
        
        var activeDialog = null;
        
        // 找到包含用户ID输入功能的弹窗
        for (var i = 0; i < dialogs.length; i++) {
            var dialog = dialogs[i];
            var style = window.getComputedStyle(dialog);
            var isVisible = style.display !== 'none' && style.visibility !== 'hidden';
            var dialogContent = dialog.innerHTML;
            var hasUserIdInput = dialogContent.includes('用户Id') || dialogContent.includes('用户ID');
            
            console.log('弹窗', i, ':');
            console.log('  可见性:', isVisible);
            console.log('  包含用户ID:', hasUserIdInput);
            console.log('  内容预览:', dialogContent.substring(0, 200));
            
            if (isVisible && hasUserIdInput) {
                console.log('找到用户ID输入弹窗', i);
                activeDialog = dialog;
                break;
            }
        }
        
        if (!activeDialog) {
            console.log('未找到用户ID输入弹窗');
            return { success: false, error: '未找到用户ID输入弹窗' };
        }
        
        console.log('用户ID输入弹窗HTML preview:', activeDialog.innerHTML.substring(0, 500));
        
        // 多种方式查找输入框
        var textarea = null;
        
        // 方法1: 查找所有textarea
        var textareas = activeDialog.querySelectorAll('textarea');
        console.log('弹窗中textarea数量:', textareas.length);
        
        for (var i = 0; i < textareas.length; i++) {
            var ta = textareas[i];
            var placeholder = ta.getAttribute('placeholder');
            var className = ta.className;
            var isVisible = ta.offsetParent !== null;
            
            console.log('textarea', i, ':');
            console.log('  placeholder:', placeholder);
            console.log('  className:', className);
            console.log('  可见:', isVisible);
            console.log('  HTML:', ta.outerHTML);
            
            if (placeholder && placeholder.includes('用户Id')) {
                console.log('找到用户ID输入框（通过placeholder）');
                textarea = ta;
                break;
            }
        }
        
        // 方法2: 如果方法1失败，查找el-textarea__inner类的textarea
        if (!textarea) {
            console.log('方法1失败，尝试方法2：查找.el-textarea__inner');
            var innerTextareas = activeDialog.querySelectorAll('textarea.el-textarea__inner');
            console.log('找到.el-textarea__inner数量:', innerTextareas.length);
            
            if (innerTextareas.length > 0) {
                textarea = innerTextareas[0];
                console.log('找到用户ID输入框（通过类名）');
            }
        }
        
        // 方法3: 如果还是找不到，使用第一个textarea
        if (!textarea && textareas.length > 0) {
            console.log('方法2失败，使用第一个textarea');
            textarea = textareas[0];
        }
        
        // 方法4: 查找所有input元素
        if (!textarea) {
            console.log('方法3失败，尝试查找input元素');
            var inputs = activeDialog.querySelectorAll('input');
            console.log('找到input数量:', inputs.length);
            
            for (var k = 0; k < inputs.length; k++) {
                var input = inputs[k];
                var placeholder = input.getAttribute('placeholder');
                console.log('input', k, 'placeholder:', placeholder, 'type:', input.type);
                
                if (placeholder && placeholder.includes('用户Id')) {
                    console.log('找到用户ID输入框（input类型）');
                    textarea = input;
                    break;
                }
            }
        }
        
        if (!textarea) {
            console.log('所有方法都失败，未找到输入框');
            return { success: false, error: '未找到输入框' };
        }
        
        console.log('找到输入框，准备输入用户ID');
        console.log('输入框详情:', textarea.outerHTML);
        
        // 清空并输入用户ID
        textarea.value = '';
        textarea.focus();
        textarea.value = arguments[0];
        
        // 触发多种输入事件确保Vue响应
        var events = ['input', 'change', 'keyup', 'blur'];
        for (var j = 0; j < events.length; j++) {
            var event = new Event(events[j], { bubbles: true });
            textarea.dispatchEvent(event);
        }
        
        console.log('用户ID已输入:', arguments[0], '，值为:', textarea.value);
        return { success: true };
        """
        
        input_result = driver.execute_script(js_input_user_id, user_id)
        
        if input_result and input_result.get('success'):
            return True
        else:
            error_msg = input_result.get('error', '未知错误') if input_result else '输入失败'
            logger.error(f"❌ 输入用户ID失败: {error_msg}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 输入用户ID异常: {e}")
        return False

def test_customer_public_sea_claim(driver):
    """
    测试客户公海领取功能
    
    Args:
        driver: WebDriver实例
        
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🚀 开始客户公海领取测试...")
        
        # 第一步：点击客户管理主菜单（使用通用辅助函数）
        logger.info("📋 步骤1: 点击客户管理主菜单...")
        
        if not click_customer_management_menu(driver):
            logger.error("❌ 点击客户管理菜单失败")
            return False
        
        # 第二步：点击公海子菜单
        logger.info("📋 步骤2: 点击公海子菜单...")
        
        js_click_public_sea = """
        // 查找公海子菜单
        var publicSeaMenu = document.querySelector('li[base-path="/customerManagement/publicSea"]');
        
        if (!publicSeaMenu) {
            console.log('未找到公海菜单');
            return { success: false, error: '未找到公海菜单' };
        }
        
        console.log('找到公海菜单');
        publicSeaMenu.click();
        console.log('公海菜单已点击');
        return { success: true };
        """
        
        public_sea_result = driver.execute_script(js_click_public_sea)
        
        if not public_sea_result or not public_sea_result.get('success'):
            logger.error("❌ 点击公海菜单失败")
            return False
        
        logger.info("✅ 公海菜单点击成功")
        time.sleep(3)  # 等待页面加载
        
        # 第三步：验证是否进入公海页面
        logger.info("📋 步骤3: 验证公海页面加载...")
        
        # 检查URL是否包含公海路径
        current_url = driver.current_url
        if "/customerManagement/publicSea" in current_url:
            logger.info("✅ 成功进入客户公海页面")
        else:
            logger.warning(f"⚠️ 当前URL可能不是公海页面: {current_url}")
        
        # 截图确认
        driver.save_screenshot("screenshots/customer_public_sea_page_loaded.png")
        logger.info("📸 公海页面截图已保存")
        
        # 第四步：点击IPIPGO标签页
        logger.info("📋 步骤4: 点击IPIPGO标签页...")
        
        js_click_ipipgo_tab = """
        // 查找IPIPGO标签页
        var tabs = document.querySelectorAll('.el-tabs__item');
        var ipipgoTab = null;
        
        console.log('找到标签页数量:', tabs.length);
        
        for (var i = 0; i < tabs.length; i++) {
            var tab = tabs[i];
            var tabText = tab.textContent.trim();
            console.log('标签页', i, '文本:', tabText);
            
            if (tabText === 'IPIPGO') {
                console.log('找到IPIPGO标签页');
                ipipgoTab = tab;
                break;
            }
        }
        
        if (!ipipgoTab) {
            console.log('未找到IPIPGO标签页');
            return { success: false, error: '未找到IPIPGO标签页' };
        }
        
        // 点击IPIPGO标签页
        ipipgoTab.click();
        console.log('IPIPGO标签页已点击');
        return { success: true };
        """
        
        tab_result = driver.execute_script(js_click_ipipgo_tab)
        
        if not tab_result or not tab_result.get('success'):
            logger.error("❌ 点击IPIPGO标签页失败")
            return False
        
        logger.info("✅ IPIPGO标签页点击成功")
        time.sleep(3)  # 等待标签页内容加载
        
        # 截图确认
        driver.save_screenshot("screenshots/public_sea_ipipgo_tab_clicked.png")
        logger.info("📸 IPIPGO标签页点击截图已保存")
        
        # 第五步：点击批量查用户ID按钮
        logger.info("📋 步骤5: 点击批量查用户ID按钮...")
        
        js_click_batch_search = """
        // 查找"批量查用户ID"按钮
        var buttons = document.querySelectorAll('button.el-button');
        var batchSearchButton = null;
        
        console.log('找到按钮数量:', buttons.length);
        
        for (var i = 0; i < buttons.length; i++) {
            var button = buttons[i];
            var span = button.querySelector('span');
            var buttonText = span ? span.textContent.trim() : button.textContent.trim();
            console.log('按钮', i, '文本:', buttonText);
            
            if (buttonText === '批量查用户ID') {
                console.log('找到批量查用户ID按钮');
                batchSearchButton = button;
                break;
            }
        }
        
        if (!batchSearchButton) {
            console.log('未找到批量查用户ID按钮');
            return { success: false, error: '未找到批量查用户ID按钮' };
        }
        
        // 点击按钮
        batchSearchButton.click();
        console.log('批量查用户ID按钮已点击');
        return { success: true };
        """
        
        batch_result = driver.execute_script(js_click_batch_search)
        
        if not batch_result or not batch_result.get('success'):
            logger.error("❌ 点击批量查用户ID按钮失败")
            return False
        
        logger.info("✅ 批量查用户ID按钮点击成功")
        time.sleep(2)  # 等待弹窗出现
        
        # 第六步：在弹窗中输入用户ID
        logger.info("📋 步骤6: 在弹窗中输入用户ID...")
        
        js_input_user_id = """
        // 查找弹窗中的输入框
        var dialogs = document.querySelectorAll('.el-dialog');
        var activeDialog = null;
        
        // 找到可见的弹窗
        for (var i = 0; i < dialogs.length; i++) {
            var dialog = dialogs[i];
            var style = window.getComputedStyle(dialog);
            if (style.display !== 'none' && style.visibility !== 'hidden') {
                console.log('找到活动弹窗');
                activeDialog = dialog;
                break;
            }
        }
        
        if (!activeDialog) {
            console.log('未找到活动弹窗');
            return { success: false, error: '未找到活动弹窗' };
        }
        
        // 在弹窗中查找输入框
        var textarea = activeDialog.querySelector('textarea.el-textarea__inner');
        
        if (!textarea) {
            console.log('未找到输入框');
            return { success: false, error: '未找到输入框' };
        }
        
        console.log('找到输入框');
        
        // 清空并输入用户ID
        textarea.value = '';
        textarea.value = '7156';
        
        // 触发输入事件
        var inputEvent = new Event('input', { bubbles: true });
        var changeEvent = new Event('change', { bubbles: true });
        textarea.dispatchEvent(inputEvent);
        textarea.dispatchEvent(changeEvent);
        
        console.log('用户ID已输入: 7156');
        return { success: true };
        """
        
        input_result = driver.execute_script(js_input_user_id)
        
        if not input_result or not input_result.get('success'):
            logger.error("❌ 输入用户ID失败")
            return False
        
        logger.info("✅ 用户ID输入成功: 7156")
        time.sleep(1)
        
        # 第七步：点击查询按钮
        logger.info("📋 步骤7: 点击查询按钮...")
        
        # 使用增强的查询按钮点击逻辑（从私海模块复制并优化）
        if not _click_search_button_enhanced(driver):
            logger.error("❌ 查询按钮点击失败")
            return False
        
        # 第八步：定位客户并执行领取操作
        logger.info("📋 步骤8: 定位客户并执行领取操作...")
        
        if not _claim_customer_from_table(driver):
            logger.error("❌ 客户领取操作失败")
            return False
        
        logger.info("🎉 客户公海领取测试流程完成！")
        logger.info("   ✅ 成功导航到客户公海页面")
        logger.info("   ✅ 成功点击IPIPGO标签页")
        logger.info("   ✅ 成功通过用户ID查询客户")
        logger.info("   ✅ 成功执行客户领取操作")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 客户公海领取测试异常: {e}")
        
        # 异常截图
        try:
            driver.save_screenshot("screenshots/public_sea_claim_error.png")
            logger.info("📸 异常截图已保存")
        except:
            pass
        
        return False

def _click_search_button_enhanced(driver):
    """
    增强的查询按钮点击逻辑
    
    Args:
        driver: WebDriver实例
        
    Returns:
        bool: 点击是否成功
    """
    logger.info("🔍 点击查询按钮...")
    
    # 使用Selenium方式点击查询按钮，更可靠
    try:
        from selenium.webdriver.common.action_chains import ActionChains
        
        # 等待查询按钮可见和可点击
        time.sleep(1)
        
        # 查找查询按钮
        search_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'el-button--primary')]//span[text()='查询']/parent::button")
        
        if not search_buttons:
            # 备用查找方式
            search_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '查询')]")
        
        if not search_buttons:
            # 再备用查找方式
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            search_buttons = [btn for btn in all_buttons if btn.is_displayed() and "查询" in btn.text]
        
        logger.info(f"找到查询按钮数量: {len(search_buttons)}")
        
        target_search_button = None
        for i, button in enumerate(search_buttons):
            try:
                if button.is_displayed() and button.is_enabled():
                    logger.info(f"查询按钮{i}: 文本='{button.text}', 可见={button.is_displayed()}, 可点击={button.is_enabled()}")
                    target_search_button = button
                    break
            except Exception as e:
                logger.warning(f"检查查询按钮{i}时出错: {e}")
                continue
        
        if target_search_button:
            # 多种点击方式
            search_success = False
            
            # 方式1: 滚动到按钮并直接点击
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", target_search_button)
                time.sleep(1)
                target_search_button.click()
                logger.info("✅ 查询按钮点击成功！(Selenium直接点击)")
                search_success = True
            except Exception as e1:
                logger.warning(f"Selenium直接点击失败: {e1}")
                
                # 方式2: ActionChains点击
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(target_search_button).click().perform()
                    logger.info("✅ 查询按钮点击成功！(ActionChains)")
                    search_success = True
                except Exception as e2:
                    logger.warning(f"ActionChains点击失败: {e2}")
                    
                    # 方式3: JavaScript点击
                    try:
                        driver.execute_script("arguments[0].click();", target_search_button)
                        logger.info("✅ 查询按钮点击成功！(JavaScript)")
                        search_success = True
                    except Exception as e3:
                        logger.error(f"JavaScript点击也失败: {e3}")
            
            if search_success:
                # 等待查询结果
                time.sleep(4)
                
                # 验证查询是否真正执行 - 检查页面变化
                js_verify_search = """
                // 检查是否有加载指示器或结果更新
                var loadingElements = document.querySelectorAll('.el-loading-mask, .el-loading-spinner, [class*="loading"]');
                var tableRows = document.querySelectorAll('tr.el-table__row');
                
                return {
                    hasLoading: loadingElements.length > 0,
                    tableRowCount: tableRows.length,
                    timestamp: new Date().getTime()
                };
                """
                
                search_status = driver.execute_script(js_verify_search)
                logger.info(f"查询状态验证: 表格行数={search_status.get('tableRowCount', 0)}")
                
                # 截图确认查询结果
                driver.save_screenshot("screenshots/public_sea_search_by_id_result.png")
                logger.info("📸 公海用户ID查询结果截图已保存")
                
                return True
            else:
                logger.error("❌ 所有查询按钮点击方式都失败")
        else:
            logger.error("❌ 未找到可用的查询按钮")
            
    except Exception as selenium_error:
        logger.error(f"❌ Selenium查询按钮点击异常: {selenium_error}")
    
    # 如果Selenium方式失败，回退到JavaScript方式
    logger.warning("⚠️ Selenium方式失败，尝试增强的JavaScript方式...")
    
    js_click_search_enhanced = """
    // 增强的查询按钮点击
    var buttons = document.querySelectorAll('button.el-button--primary');
    var searchButton = null;
    
    console.log('找到主要按钮数量:', buttons.length);
    
    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        var span = button.querySelector('span');
        var buttonText = span ? span.textContent.trim() : button.textContent.trim();
        console.log('按钮', i, '文本:', buttonText);
        
        if (buttonText === '查询') {
            console.log('找到查询按钮，检查状态');
            var rect = button.getBoundingClientRect();
            var isVisible = rect.width > 0 && rect.height > 0;
            var isEnabled = !button.disabled;
            
            console.log('按钮可见:', isVisible, '按钮可用:', isEnabled);
            
            if (isVisible && isEnabled) {
                searchButton = button;
                break;
            }
        }
    }
    
    if (!searchButton) {
        console.log('未找到可用的查询按钮');
        return { success: false, error: '未找到可用的查询按钮' };
    }
    
    // 尝试多种JavaScript点击方式
    try {
        // 方式1: 直接点击
        searchButton.click();
        console.log('查询按钮已点击（方式1）');
        return { success: true, method: 'direct_click' };
    } catch (e1) {
        console.log('方式1失败:', e1.message);
        try {
            // 方式2: 触发多种事件
            var events = ['mousedown', 'mouseup', 'click'];
            for (var j = 0; j < events.length; j++) {
                var event = new MouseEvent(events[j], {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                searchButton.dispatchEvent(event);
            }
            console.log('查询按钮已点击（方式2-多事件）');
            return { success: true, method: 'multi_events' };
        } catch (e2) {
            console.log('方式2失败:', e2.message);
            return { success: false, error: '所有JavaScript点击方式都失败', errors: [e1.message, e2.message] };
        }
    }
    """
    
    search_result = driver.execute_script(js_click_search_enhanced)
    
    if search_result and search_result.get('success'):
        method = search_result.get('method', 'unknown')
        logger.info(f"✅ 查询按钮已点击成功！(增强JavaScript方式: {method})")
        
        # 等待查询结果
        time.sleep(4)
        
        # 截图确认查询结果
        driver.save_screenshot("screenshots/public_sea_search_by_id_result.png")
        logger.info("📸 公海用户ID查询结果截图已保存")
        
        return True
    else:
        error_msg = search_result.get('error', '未知错误') if search_result else '点击失败'
        logger.error(f"❌ 查询按钮点击失败: {error_msg}")
        
        if isinstance(search_result, dict) and 'errors' in search_result:
            logger.error(f"   错误详情: {search_result['errors']}")
        
        # 截图调试
        driver.save_screenshot("screenshots/public_sea_search_button_error.png")
        logger.info("📸 公海查询按钮调试截图已保存")
        
        return False

def _claim_customer_from_table(driver):
    """
    从表格中定位客户并执行领取操作
    
    Args:
        driver: WebDriver实例
        
    Returns:
        bool: 操作是否成功
    """
    logger.info("👤 开始定位客户并执行领取操作...")
    
    # 查找表格中的第一行客户（查询结果应该只有一个客户）
    js_claim_customer = """
    // 查找表格行
    var tableRows = document.querySelectorAll('tr.el-table__row');
    console.log('找到表格行数量:', tableRows.length);
    
    if (tableRows.length === 0) {
        console.log('未找到客户数据');
        return { success: false, error: '未找到客户数据' };
    }
    
    // 操作第一行客户
    var firstRow = tableRows[0];
    console.log('找到第一行客户');
    
    // 查找操作按钮（下拉菜单）
    var dropdown = firstRow.querySelector('.el-dropdown');
    if (!dropdown) {
        console.log('未找到操作下拉菜单');
        return { success: false, error: '未找到操作下拉菜单' };
    }
    
    // 查找下拉箭头按钮（关键修复：应该点击带箭头的按钮而不是"操作"按钮）
    var dropdownButton = dropdown.querySelector('button.el-dropdown__caret-button');
    if (!dropdownButton) {
        // 备用方案：查找第二个按钮
        var buttons = dropdown.querySelectorAll('button.el-button--info');
        if (buttons.length >= 2) {
            dropdownButton = buttons[1]; // 使用第二个按钮
            console.log('使用第二个按钮作为下拉按钮');
        } else {
            // 最后备用方案：使用第一个按钮
            dropdownButton = dropdown.querySelector('button.el-button--info');
            console.log('使用第一个按钮作为备用下拉按钮');
        }
    }
    
    if (!dropdownButton) {
        console.log('未找到下拉按钮');
        return { success: false, error: '未找到下拉按钮' };
    }
    
    console.log('找到下拉按钮，准备点击');
    
    // 点击下拉按钮展开菜单
    dropdownButton.click();
    console.log('下拉按钮已点击，菜单应该展开');
    
    return { success: true, step: 'dropdown_opened' };
    """
    
    claim_result = driver.execute_script(js_claim_customer)
    
    if not claim_result or not claim_result.get('success'):
        error_msg = claim_result.get('error', '未知错误') if claim_result else '操作失败'
        logger.error(f"❌ 展开操作下拉菜单失败: {error_msg}")
        return False
    
    logger.info("✅ 操作下拉菜单已展开")
    time.sleep(2)  # 等待下拉菜单展开
    
    # 点击"领取客户"菜单项
    logger.info("🎯 点击领取客户菜单项...")
    
    js_click_claim_menu = """
    // 增强的菜单项查找逻辑
    var claimMenuItem = null;
    var allMenuTexts = [];
    
    // 方法1：查找下拉菜单项
    var dropdownMenus = document.querySelectorAll('.el-dropdown-menu');
    console.log('找到下拉菜单数量:', dropdownMenus.length);
    
    // 查找可见的下拉菜单
    for (var i = 0; i < dropdownMenus.length; i++) {
        var menu = dropdownMenus[i];
        var style = window.getComputedStyle(menu);
        
        console.log('菜单', i, '显示状态:', style.display, '可见性:', style.visibility);
        
        // 更宽松的可见性检查
        if (style.display !== 'none') {
            console.log('找到可见的下拉菜单');
            
            // 在菜单中查找"领取客户"项
            var menuItems = menu.querySelectorAll('.el-dropdown-menu__item');
            console.log('菜单项数量:', menuItems.length);
            
            for (var j = 0; j < menuItems.length; j++) {
                var item = menuItems[j];
                var itemText = item.textContent.trim();
                console.log('菜单项', j, '文本:', itemText);
                allMenuTexts.push(itemText);
                
                if (itemText === '领取客户') {
                    console.log('找到领取客户菜单项');
                    claimMenuItem = item;
                    break;
                }
            }
            
            if (claimMenuItem) break;
        }
    }
    
    // 方法2：如果方法1失败，尝试查找所有可能的菜单项
    if (!claimMenuItem) {
        console.log('方法1失败，尝试方法2：查找所有li元素');
        var allLiElements = document.querySelectorAll('li');
        
        for (var k = 0; k < allLiElements.length; k++) {
            var li = allLiElements[k];
            var liText = li.textContent.trim();
            
            if (liText === '领取客户' && li.className.includes('dropdown-menu__item')) {
                console.log('通过方法2找到领取客户菜单项');
                claimMenuItem = li;
                break;
            }
        }
    }
    
    // 方法3：最后尝试直接查找包含"领取客户"文本的元素
    if (!claimMenuItem) {
        console.log('方法2失败，尝试方法3：直接查找包含文本的元素');
        var allElements = document.querySelectorAll('*');
        
        for (var m = 0; m < allElements.length; m++) {
            var element = allElements[m];
            var elementText = element.textContent.trim();
            
            if (elementText === '领取客户' && 
                (element.tagName === 'LI' || element.className.includes('menu'))) {
                console.log('通过方法3找到领取客户菜单项');
                claimMenuItem = element;
                break;
            }
        }
    }
    
    if (!claimMenuItem) {
        console.log('所有方法都失败：未找到领取客户菜单项');
        console.log('所有找到的菜单项:', allMenuTexts);
        return { success: false, error: '未找到领取客户菜单项', allMenus: allMenuTexts };
    }
    
    // 点击领取客户菜单项
    claimMenuItem.click();
    console.log('领取客户菜单项已点击');
    
    return { success: true };
    """
    
    menu_result = driver.execute_script(js_click_claim_menu)
    
    if not menu_result or not menu_result.get('success'):
        error_msg = menu_result.get('error', '未知错误') if menu_result else '点击失败'
        logger.error(f"❌ 点击领取客户菜单项失败: {error_msg}")
        
        # 截图调试
        driver.save_screenshot("screenshots/public_sea_claim_menu_error.png")
        logger.info("📸 领取客户菜单调试截图已保存")
        
        return False
    
    logger.info("✅ 领取客户菜单项点击成功")
    
    # 等待通知弹窗显示和消失（3秒）
    logger.info("⏳ 等待领取成功通知弹窗（3秒）...")
    time.sleep(3)
    
    # 检查操作结果
    logger.info("🔍 检查领取操作结果...")
    
    js_check_claim_result = """
    // 检查页面状态，看是否还有通知弹窗
    var notifications = document.querySelectorAll('.el-notification, .el-message, .el-alert');
    var hasNotification = false;
    
    for (var i = 0; i < notifications.length; i++) {
        var notification = notifications[i];
        var style = window.getComputedStyle(notification);
        if (style.display !== 'none' && style.visibility !== 'hidden') {
            console.log('发现通知弹窗:', notification.textContent);
            hasNotification = true;
        }
    }
    
    // 检查表格状态
    var tableRows = document.querySelectorAll('tr.el-table__row');
    
    return {
        hasNotification: hasNotification,
        tableRowCount: tableRows.length,
        timestamp: new Date().getTime()
    };
    """
    
    claim_status = driver.execute_script(js_check_claim_result)
    
    if claim_status:
        if claim_status.get('hasNotification'):
            logger.info("ℹ️ 仍有通知弹窗显示，操作可能正在处理中")
        else:
            logger.info("✅ 通知弹窗已消失，领取操作应该已完成")
        
        logger.info(f"📊 当前表格行数: {claim_status.get('tableRowCount', 0)}")
    
    # 最终截图确认
    driver.save_screenshot("screenshots/public_sea_customer_claim_completed.png")
    logger.info("📸 客户领取操作完成截图已保存")
    
    logger.info("✅ 客户领取操作完成")
    return True

def _navigate_to_public_sea_and_claim(driver):
    """
    从当前状态直接导航到公海页面并执行领取操作
    这个函数用于完整流程的第二阶段，不需要重新从客户管理菜单开始
    
    Args:
        driver: WebDriver实例
        
    Returns:
        bool: 操作是否成功
    """
    try:
        logger.info("🔄 第二阶段：导航到公海页面...")
        
        # 步骤1：点击公海子菜单（假设客户管理菜单已经展开）
        logger.info("📋 步骤1: 点击公海子菜单...")
        
        js_click_public_sea = """
        // 查找公海子菜单
        var publicSeaMenu = document.querySelector('li[base-path="/customerManagement/publicSea"]');
        
        if (!publicSeaMenu) {
            console.log('未找到公海菜单，尝试其他方式');
            // 尝试通过文本查找
            var menuItems = document.querySelectorAll('li.inner-menu-item');
            for (var i = 0; i < menuItems.length; i++) {
                var item = menuItems[i];
                var span = item.querySelector('span');
                if (span && span.textContent.trim() === '公海') {
                    console.log('通过文本找到公海菜单');
                    publicSeaMenu = item;
                    break;
                }
            }
        }
        
        if (!publicSeaMenu) {
            console.log('未找到公海菜单');
            return { success: false, error: '未找到公海菜单' };
        }
        
        console.log('找到公海菜单，准备点击');
        publicSeaMenu.click();
        console.log('公海菜单已点击');
        return { success: true };
        """
        
        public_sea_result = driver.execute_script(js_click_public_sea)
        
        if not public_sea_result or not public_sea_result.get('success'):
            logger.error("❌ 点击公海菜单失败")
            return False
        
        logger.info("✅ 公海菜单点击成功")
        time.sleep(3)  # 等待页面加载
        
        # 步骤2：验证是否进入公海页面
        logger.info("📋 步骤2: 验证公海页面加载...")
        
        # 检查URL是否包含公海路径
        current_url = driver.current_url
        if "/customerManagement/publicSea" in current_url:
            logger.info("✅ 成功进入客户公海页面")
        else:
            logger.warning(f"⚠️ 当前URL可能不是公海页面: {current_url}")
        
        # 截图确认
        driver.save_screenshot("screenshots/customer_public_sea_stage2_loaded.png")
        logger.info("📸 第二阶段公海页面截图已保存")
        
        # 步骤3：点击IPIPGO标签页
        logger.info("📋 步骤3: 点击IPIPGO标签页...")
        
        js_click_ipipgo_tab = """
        // 查找IPIPGO标签页
        var tabs = document.querySelectorAll('.el-tabs__item');
        var ipipgoTab = null;
        
        console.log('找到标签页数量:', tabs.length);
        
        for (var i = 0; i < tabs.length; i++) {
            var tab = tabs[i];
            var tabText = tab.textContent.trim();
            console.log('标签页', i, '文本:', tabText);
            
            if (tabText === 'IPIPGO') {
                console.log('找到IPIPGO标签页');
                ipipgoTab = tab;
                break;
            }
        }
        
        if (!ipipgoTab) {
            console.log('未找到IPIPGO标签页');
            return { success: false, error: '未找到IPIPGO标签页' };
        }
        
        // 点击IPIPGO标签页
        ipipgoTab.click();
        console.log('IPIPGO标签页已点击');
        return { success: true };
        """
        
        tab_result = driver.execute_script(js_click_ipipgo_tab)
        
        if not tab_result or not tab_result.get('success'):
            logger.error("❌ 点击IPIPGO标签页失败")
            return False
        
        logger.info("✅ IPIPGO标签页点击成功")
        time.sleep(3)  # 等待标签页内容加载
        
        # 截图确认
        driver.save_screenshot("screenshots/public_sea_stage2_ipipgo_tab_clicked.png")
        logger.info("📸 第二阶段IPIPGO标签页点击截图已保存")
        
        # 步骤4：点击批量查用户ID按钮
        logger.info("📋 步骤4: 点击批量查用户ID按钮...")
        
        js_click_batch_search = """
        // 查找"批量查用户ID"按钮
        var buttons = document.querySelectorAll('button.el-button');
        var batchSearchButton = null;
        
        console.log('找到按钮数量:', buttons.length);
        
        for (var i = 0; i < buttons.length; i++) {
            var button = buttons[i];
            var span = button.querySelector('span');
            var buttonText = span ? span.textContent.trim() : button.textContent.trim();
            console.log('按钮', i, '文本:', buttonText);
            
            if (buttonText === '批量查用户ID') {
                console.log('找到批量查用户ID按钮');
                batchSearchButton = button;
                break;
            }
        }
        
        if (!batchSearchButton) {
            console.log('未找到批量查用户ID按钮');
            return { success: false, error: '未找到批量查用户ID按钮' };
        }
        
        // 点击按钮
        batchSearchButton.click();
        console.log('批量查用户ID按钮已点击');
        return { success: true };
        """
        
        batch_result = driver.execute_script(js_click_batch_search)
        
        if not batch_result or not batch_result.get('success'):
            logger.error("❌ 点击批量查用户ID按钮失败")
            return False
        
        logger.info("✅ 批量查用户ID按钮点击成功")
        time.sleep(2)  # 等待弹窗出现
        
        # 步骤5：在弹窗中输入用户ID
        logger.info("📋 步骤5: 在弹窗中输入用户ID...")
        
        # 使用简化的输入逻辑
        success = _input_user_id_in_dialog(driver, "7156")
        if not success:
            logger.error("❌ 输入用户ID失败")
            return False
        
        logger.info("✅ 用户ID输入成功: 7156")
        time.sleep(1)
        
        # 步骤6：点击查询按钮
        logger.info("📋 步骤6: 点击查询按钮...")
        
        if not _click_search_button_enhanced(driver):
            logger.error("❌ 查询按钮点击失败")
            return False
        
        # 步骤7：定位客户并执行领取操作
        logger.info("📋 步骤7: 定位客户并执行领取操作...")
        
        if not _claim_customer_from_table(driver):
            logger.error("❌ 客户领取操作失败")
            return False
        
        logger.info("✅ 第二阶段：公海领取客户操作完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 第二阶段公海领取操作异常: {e}")
        
        # 异常截图
        try:
            driver.save_screenshot("screenshots/public_sea_stage2_error.png")
            logger.info("📸 第二阶段异常截图已保存")
        except:
            pass
        
        return False

def test_customer_private_to_public_claim_workflow(driver):
    """
    测试客户完整流程：私海投入公海 → 公海领取客户
    这是一个完整的业务流程测试
    
    Args:
        driver: WebDriver实例
        
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🚀 开始客户完整流程测试：私海投入公海 → 公海领取客户")
        logger.info("=" * 60)
        
        # 导入私海投入公海功能
        from crm_customer_private_sea import test_customer_private_sea_to_public_workflow
        
        # 第一阶段：私海投入公海
        logger.info("🔸 第一阶段：客户私海投入公海")
        logger.info("   📋 流程：客户管理 → 私海 → IPIPGO → 查询用户ID 7156 → 投入公海")
        
        success_private = test_customer_private_sea_to_public_workflow(driver)
        
        if not success_private:
            logger.error("❌ 第一阶段失败：客户私海投入公海操作失败")
            return False
        
        logger.info("✅ 第一阶段完成：客户已成功投入公海")
        logger.info("⏳ 等待5秒，确保数据同步...")
        time.sleep(5)
        
        # 第二阶段：直接导航到公海页面
        logger.info("🔸 第二阶段：公海领取客户")
        logger.info("   📋 流程：导航到公海 → IPIPGO → 查询用户ID 7156 → 领取客户")
        
        # 直接导航到公海页面（不需要重新从客户管理开始）
        success_public = _navigate_to_public_sea_and_claim(driver)
        
        if not success_public:
            logger.error("❌ 第二阶段失败：公海领取客户操作失败")
            logger.warning("⚠️ 注意：第一阶段的投入公海操作已成功，但第二阶段领取失败")
            return False
        
        logger.info("✅ 第二阶段完成：客户已成功从公海领取")
        
        # 流程完成
        logger.info("=" * 60)
        logger.info("🎉 客户完整业务流程测试成功完成！")
        logger.info("📊 流程总结：")
        logger.info("   ✅ 第一阶段：私海投入公海 - 成功")
        logger.info("   ✅ 第二阶段：公海领取客户 - 成功")
        logger.info("   🎯 目标客户：用户ID 7156")
        logger.info("   💡 完整业务闭环：私海 → 公海 → 重新领取")
        
        # 最终截图
        driver.save_screenshot("screenshots/customer_complete_workflow_success.png")
        logger.info("📸 完整流程成功截图已保存")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 客户完整流程测试异常: {e}")
        
        # 异常截图
        try:
            driver.save_screenshot("screenshots/customer_complete_workflow_error.png")
            logger.info("📸 流程异常截图已保存")
        except:
            pass
        
        return False

if __name__ == "__main__":
    print("这是CRM客户公海领取测试模块")
    print("请通过主程序调用 test_customer_public_sea_claim() 函数") 