"""
CRM客户管理模块
实现客户私海相关功能的自动化测试
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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


def navigate_to_customer_private_sea(driver):
    """
    导航到客户私海页面
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 导航是否成功
    """
    try:
        logger.info("👥 开始导航到客户私海页面...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 步骤0: 点击客户管理主菜单（前端更新后需要）
        if not click_customer_management_menu(driver):
            logger.warning("⚠️ 点击客户管理菜单失败，尝试继续...")
        
        # 步骤1: 点击客户主菜单（展开子菜单）
        logger.info("1. 点击客户主菜单...")
        
        js_click_customer_menu = """
        // 查找客户主菜单项
        var submenuTitles = document.querySelectorAll('div.el-submenu__title');
        for (var i = 0; i < submenuTitles.length; i++) {
            var title = submenuTitles[i];
            var span = title.querySelector('span');
            if (span && span.textContent.trim() === '客户') {
                console.log('找到客户主菜单，准备点击');
                title.click();
                return true;
            }
        }
        console.log('未找到客户主菜单');
        return false;
        """
        
        if driver.execute_script(js_click_customer_menu):
            logger.info("✅ 客户主菜单已点击，子菜单应该已展开")
        else:
            raise Exception("无法找到客户主菜单")
        
        # 等待子菜单展开
        time.sleep(2)
        
        # 步骤2: 点击私海子菜单
        logger.info("2. 点击私海子菜单...")
        
        js_click_private_sea_menu = """
        // 查找私海子菜单项
        var menuItems = document.querySelectorAll('li.el-menu-item.inner-menu-item');
        for (var i = 0; i < menuItems.length; i++) {
            var item = menuItems[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '私海' && 
                item.getAttribute('base-path') === '/customerManagement/privateSea') {
                console.log('找到私海菜单，准备点击');
                item.click();
                return true;
            }
        }
        console.log('未找到私海菜单');
        return false;
        """
        
        if driver.execute_script(js_click_private_sea_menu):
            logger.info("✅ 私海菜单已点击")
        else:
            raise Exception("无法找到私海菜单")
        
        # 等待页面加载
        time.sleep(3)
        
        # 验证是否成功进入客户私海页面
        js_verify_private_sea_page = """
        // 检查URL是否包含客户私海路径
        var currentUrl = window.location.href;
        return currentUrl.includes('/customerManagement/privateSea') || 
               currentUrl.includes('privateSea');
        """
        
        if driver.execute_script(js_verify_private_sea_page):
            logger.info("✅ 已成功进入客户私海页面")
            
            # 截图确认
            driver.save_screenshot("screenshots/customer_private_sea_page_loaded.png")
            logger.info("📸 客户私海页面加载截图已保存")
            
            return True
        else:
            logger.error("❌ 未能成功进入客户私海页面")
            return False
        
    except Exception as e:
        logger.error(f"导航到客户私海页面异常: {e}")
        try:
            driver.save_screenshot("screenshots/customer_private_sea_navigation_error.png")
        except:
            pass
        return False


def click_ipipgo_tab(driver):
    """
    点击IPIPGO标签页
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 点击是否成功
    """
    try:
        logger.info("🎯 开始点击IPIPGO标签页...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 查找并点击IPIPGO标签页
        js_click_ipipgo_tab = """
        // 查找IPIPGO标签页
        var tabItems = document.querySelectorAll('div.el-tabs__item');
        for (var i = 0; i < tabItems.length; i++) {
            var tab = tabItems[i];
            var text = tab.textContent.trim();
            if (text === 'IPIPGO' && tab.id && tab.id.includes('tab-')) {
                console.log('找到IPIPGO标签页，准备点击');
                console.log('标签页ID:', tab.id);
                tab.click();
                return { success: true, tabId: tab.id };
            }
        }
        
        // 如果没找到，列出所有可用的标签页
        var allTabs = [];
        for (var j = 0; j < tabItems.length; j++) {
            allTabs.push(tabItems[j].textContent.trim());
        }
        console.log('未找到IPIPGO标签页');
        console.log('可用标签页:', allTabs);
        return { success: false, tabs: allTabs };
        """
        
        result = driver.execute_script(js_click_ipipgo_tab)
        
        if result and result.get('success'):
            tab_id = result.get('tabId', 'unknown')
            logger.info(f"✅ IPIPGO标签页已点击成功！(ID: {tab_id})")
            
            # 等待标签页内容加载
            time.sleep(3)
            
            # 截图确认结果
            driver.save_screenshot("screenshots/ipipgo_tab_clicked.png")
            logger.info("📸 IPIPGO标签页点击成功截图已保存")
            
            return True
        else:
            logger.error("❌ 未找到IPIPGO标签页")
            if isinstance(result, dict) and 'tabs' in result:
                logger.error(f"   可用标签页: {result['tabs']}")
            
            # 截图调试
            driver.save_screenshot("screenshots/ipipgo_tab_not_found.png")
            logger.info("📸 标签页调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"点击IPIPGO标签页异常: {e}")
        try:
            driver.save_screenshot("screenshots/ipipgo_tab_error.png")
            logger.info("📸 错误截图已保存")
        except:
            pass
        return False


def handle_customer_public_sea_dialog(driver):
    """
    处理客户投入公海的弹窗
    填写投放原因并点击确认按钮
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 弹窗处理是否成功
    """
    try:
        logger.info("📋 开始处理客户投入公海弹窗...")
        
        # 等待弹窗出现
        time.sleep(3)
        
        # 填写投放原因
        logger.info("✍️ 填写投放原因...")
        
        js_fill_reason = """
        // 查找投放原因输入框
        var textareas = document.querySelectorAll('textarea.el-textarea__inner');
        var targetTextarea = null;
        
        for (var i = 0; i < textareas.length; i++) {
            var textarea = textareas[i];
            var placeholder = textarea.getAttribute('placeholder');
            if (placeholder && placeholder.includes('请输入投放原因')) {
                console.log('找到投放原因输入框');
                targetTextarea = textarea;
                break;
            }
        }
        
        if (!targetTextarea) {
            console.log('未找到投放原因输入框');
            return { success: false, error: '未找到投放原因输入框' };
        }
        
        // 清空并填写投放原因
        targetTextarea.value = '';
        targetTextarea.value = 'UI自动化测试';
        
        // 触发input事件确保Vue检测到变化
        var inputEvent = new Event('input', { bubbles: true });
        targetTextarea.dispatchEvent(inputEvent);
        
        // 触发change事件
        var changeEvent = new Event('change', { bubbles: true });
        targetTextarea.dispatchEvent(changeEvent);
        
        console.log('投放原因已填写: UI自动化测试');
        return { success: true, value: targetTextarea.value };
        """
        
        fill_result = driver.execute_script(js_fill_reason)
        
        if fill_result and fill_result.get('success'):
            logger.info(f"✅ 投放原因已填写: {fill_result.get('value', 'UI自动化测试')}")
            
            # 等待一下确保输入完成
            time.sleep(2)
            
            # 使用更强力的确认按钮点击策略
            logger.info("🔘 点击确认按钮...")
            
            # 首先尝试Selenium方式
            try:
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.action_chains import ActionChains
                
                # 查找所有确认按钮
                confirm_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'el-button--primary')]//span[text()='确认']/parent::button")
                
                if not confirm_buttons:
                    # 备用查找方式
                    confirm_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '确认')]")
                
                if not confirm_buttons:
                    # 再备用查找方式
                    all_buttons = driver.find_elements(By.TAG_NAME, "button")
                    confirm_buttons = [btn for btn in all_buttons if btn.is_displayed() and "确认" in btn.text]
                
                logger.info(f"找到确认按钮数量: {len(confirm_buttons)}")
                
                target_button = None
                for i, button in enumerate(confirm_buttons):
                    try:
                        if button.is_displayed() and button.is_enabled():
                            logger.info(f"确认按钮{i}: 文本='{button.text}', 可见={button.is_displayed()}, 可点击={button.is_enabled()}")
                            target_button = button
                            break
                    except Exception as e:
                        logger.warning(f"检查按钮{i}时出错: {e}")
                        continue
                
                if target_button:
                    # 多种点击方式
                    success = False
                    
                    # 方式1: 滚动到按钮并直接点击
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", target_button)
                        time.sleep(1)
                        target_button.click()
                        logger.info("✅ 确认按钮点击成功！(Selenium直接点击)")
                        success = True
                    except Exception as e1:
                        logger.warning(f"Selenium直接点击失败: {e1}")
                        
                        # 方式2: ActionChains点击
                        try:
                            actions = ActionChains(driver)
                            actions.move_to_element(target_button).click().perform()
                            logger.info("✅ 确认按钮点击成功！(ActionChains)")
                            success = True
                        except Exception as e2:
                            logger.warning(f"ActionChains点击失败: {e2}")
                            
                            # 方式3: JavaScript点击
                            try:
                                driver.execute_script("arguments[0].click();", target_button)
                                logger.info("✅ 确认按钮点击成功！(JavaScript)")
                                success = True
                            except Exception as e3:
                                logger.error(f"JavaScript点击也失败: {e3}")
                    
                    if success:
                        # 等待弹窗关闭
                        time.sleep(5)
                        
                        # 验证弹窗是否关闭
                        try:
                            # 检查弹窗是否还存在
                            remaining_dialogs = driver.find_elements(By.CSS_SELECTOR, ".el-dialog, .el-message-box, [role='dialog']")
                            visible_dialogs = [d for d in remaining_dialogs if d.is_displayed()]
                            
                            if len(visible_dialogs) == 0:
                                logger.info("✅ 弹窗已成功关闭！")
                            else:
                                logger.warning(f"⚠️ 仍有{len(visible_dialogs)}个可见弹窗")
                        except:
                            pass
                        
                        # 截图确认结果
                        driver.save_screenshot("screenshots/customer_public_sea_dialog_completed.png")
                        logger.info("📸 客户投入公海弹窗处理完成截图已保存")
                        
                        return True
                    else:
                        logger.error("❌ 所有Selenium点击方式都失败")
                else:
                    logger.error("❌ 未找到可用的确认按钮")
                
            except Exception as selenium_error:
                logger.error(f"❌ Selenium方式异常: {selenium_error}")
            
            # 截图调试
            driver.save_screenshot("screenshots/customer_confirm_button_error.png")
            logger.info("📸 确认按钮调试截图已保存")
            
            return False
        else:
            error_msg = fill_result.get('error', '未知错误') if fill_result else '填写失败'
            logger.error(f"❌ 投放原因填写失败: {error_msg}")
            
            # 截图调试
            driver.save_screenshot("screenshots/customer_reason_input_error.png")
            logger.info("📸 投放原因输入调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"处理客户投入公海弹窗异常: {e}")
        try:
            driver.save_screenshot("screenshots/customer_dialog_error.png")
            logger.info("📸 弹窗处理错误截图已保存")
        except:
            pass
        return False


def click_customer_public_sea_button(driver):
    """
    点击指定客户的投入公海按钮
    根据客户特征信息（电话号码183****6247）进行定位
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 点击是否成功
    """
    try:
        logger.info("🎯 开始点击客户的投入公海按钮...")
        
        # 等待表格加载完成
        time.sleep(3)
        
        # 首先调试：详细分析所有客户信息
        js_debug_customers = """
        var tableRows = document.querySelectorAll('tr.el-table__row');
        var customers = [];
        
        for (var i = 0; i < tableRows.length; i++) {
            var row = tableRows[i];
            var cellText = row.textContent;
            
            // 查找电话号码
            var phoneMatches = cellText.match(/1[3-9]\\d\\*\\*\\*\\*\\d{4}/g);
            if (phoneMatches && phoneMatches.length > 0) {
                // 获取更多客户信息
                var customerInfo = {
                    index: i,
                    phones: phoneMatches,
                    hasTargetPhone: cellText.includes('183****6247'),
                    hasQinRenChi: cellText.includes('秦仁驰'),
                    hasTestTags: cellText.includes('测试未转化') || cellText.includes('意向型客户'),
                    fullText: cellText.substring(0, 300)
                };
                
                customers.push(customerInfo);
                
                console.log('客户', i, '信息:');
                console.log('  电话:', phoneMatches);
                console.log('  包含183****6247:', customerInfo.hasTargetPhone);
                console.log('  包含秦仁驰:', customerInfo.hasQinRenChi);
                console.log('  包含测试标签:', customerInfo.hasTestTags);
            }
        }
        
        return { customers: customers };
        """
        
        debug_result = driver.execute_script(js_debug_customers)
        if debug_result and 'customers' in debug_result:
            logger.info(f"📊 找到客户数量: {len(debug_result['customers'])}")
            for i, customer in enumerate(debug_result['customers']):
                logger.info(f"   客户{customer['index']}: 电话{customer['phones']}")
                logger.info(f"      包含183****6247: {customer['hasTargetPhone']}")
                logger.info(f"      包含秦仁驰: {customer['hasQinRenChi']}")
                logger.info(f"      包含测试标签: {customer['hasTestTags']}")
        
        # 使用多重特征精确定位目标客户
        js_click_public_sea_button = """
        var tableRows = document.querySelectorAll('tr.el-table__row');
        var targetRow = null;
        var targetIndex = -1;
        var candidateRows = [];
        
        // 第一步：找到所有包含183****6247的行
        for (var i = 0; i < tableRows.length; i++) {
            var row = tableRows[i];
            var cellText = row.textContent;
            
            if (cellText.includes('183****6247')) {
                candidateRows.push({
                    index: i,
                    row: row,
                    text: cellText,
                    hasQinRenChi: cellText.includes('秦仁驰'),
                    hasTestTags: cellText.includes('测试未转化') && cellText.includes('意向型客户'),
                    hasPhoneNumber: cellText.includes('15271193874')
                });
                console.log('找到候选行', i, '包含183****6247');
            }
        }
        
        console.log('找到候选行数量:', candidateRows.length);
        
        // 第二步：在候选行中找到最匹配的目标行
        for (var j = 0; j < candidateRows.length; j++) {
            var candidate = candidateRows[j];
            console.log('检查候选行', candidate.index);
            console.log('  包含秦仁驰:', candidate.hasQinRenChi);
            console.log('  包含测试标签:', candidate.hasTestTags);
            console.log('  包含15271193874:', candidate.hasPhoneNumber);
            
            // 使用多重特征匹配
            if (candidate.hasQinRenChi && candidate.hasTestTags) {
                console.log('找到完全匹配的目标客户行:', candidate.index);
                targetRow = candidate.row;
                targetIndex = candidate.index;
                break;
            }
        }
        
        // 如果没有完全匹配，选择第一个包含183****6247的行
        if (!targetRow && candidateRows.length > 0) {
            console.log('使用第一个候选行作为目标');
            targetRow = candidateRows[0].row;
            targetIndex = candidateRows[0].index;
        }
        
        if (!targetRow) {
            console.log('未找到任何包含183****6247的客户行');
            return { success: false, error: '未找到目标客户', candidateCount: candidateRows.length };
        }
        
        console.log('最终选择的目标行索引:', targetIndex);
        
        // 第三步：在目标行中查找操作按钮
        var dropdown = targetRow.querySelector('div.el-dropdown');
        if (!dropdown) {
            console.log('在目标行中未找到操作下拉菜单');
            return { success: false, error: '未找到操作下拉菜单', targetIndex: targetIndex };
        }
        
        // 查找操作按钮 - 尝试多种选择器
        var operationBtn = dropdown.querySelector('button.el-button--info');
        if (!operationBtn) {
            // 备用选择器
            operationBtn = dropdown.querySelector('button[type="button"]');
        }
        if (!operationBtn) {
            // 再备用选择器
            operationBtn = dropdown.querySelector('button');
        }
        
        if (operationBtn) {
            console.log('在目标行中找到操作按钮，准备点击');
            operationBtn.click();
            return { 
                success: true, 
                step: 'button_clicked', 
                targetIndex: targetIndex,
                matchedFeatures: {
                    hasQinRenChi: candidateRows.find(c => c.index === targetIndex)?.hasQinRenChi,
                    hasTestTags: candidateRows.find(c => c.index === targetIndex)?.hasTestTags
                }
            };
        } else {
            console.log('在目标行中未找到操作按钮');
            return { success: false, error: '未找到操作按钮', targetIndex: targetIndex };
        }
        """
        
        result = driver.execute_script(js_click_public_sea_button)
        
        if result and result.get('success'):
            target_index = result.get('targetIndex', -1)
            matched_features = result.get('matchedFeatures', {})
            logger.info(f"✅ 客户操作按钮已点击！")
            logger.info(f"   目标客户行索引: {target_index}")
            logger.info(f"   匹配特征 - 包含秦仁驰: {matched_features.get('hasQinRenChi', 'unknown')}")
            logger.info(f"   匹配特征 - 包含测试标签: {matched_features.get('hasTestTags', 'unknown')}")
            
            # 等待菜单展开
            time.sleep(1.5)
            
            # 查找并点击"投入公海"菜单项
            logger.info("🔍 查找投入公海菜单项...")
            
            click_public_sea_menu_js = """
            var menuItems = document.querySelectorAll('li.el-dropdown-menu__item');
            var menuTexts = [];
            
            for (var i = 0; i < menuItems.length; i++) {
                var item = menuItems[i];
                var text = item.textContent.trim();
                menuTexts.push(text);
                
                if (text === '投入公海') {
                    console.log('找到投入公海菜单项，执行点击');
                    item.click();
                    return { success: true, clicked: '投入公海' };
                }
            }
            
            console.log('可用菜单项:', menuTexts);
            return { success: false, menus: menuTexts };
            """
            
            menu_result = driver.execute_script(click_public_sea_menu_js)
            
            if menu_result and menu_result.get('success'):
                logger.info(f"✅ 投入公海菜单项已点击成功！")
                
                # 等待弹窗出现
                time.sleep(2)
                
                # 处理投入公海弹窗
                if handle_customer_public_sea_dialog(driver):
                    logger.info("✅ 投入公海弹窗处理成功！")
                    
                    # 截图确认最终结果
                    driver.save_screenshot("screenshots/customer_public_sea_success.png")
                    logger.info("📸 客户投入公海成功截图已保存")
                    
                    return True
                else:
                    logger.error("❌ 投入公海弹窗处理失败")
                    return False
            else:
                logger.error("❌ 未找到投入公海菜单项")
                if isinstance(menu_result, dict) and 'menus' in menu_result:
                    logger.error(f"   可用菜单项: {menu_result['menus']}")
                
                # 截图调试
                driver.save_screenshot("screenshots/customer_menu_debug.png")
                logger.info("📸 菜单调试截图已保存")
                
                return False
        else:
            error_msg = result.get('error', '未知错误') if result else '操作失败'
            logger.error(f"❌ 客户操作按钮点击失败: {error_msg}")
            
            if isinstance(result, dict):
                if 'candidateCount' in result:
                    logger.error(f"   找到的候选行数量: {result['candidateCount']}")
                if 'targetIndex' in result:
                    logger.error(f"   目标行索引: {result['targetIndex']}")
            
            # 截图调试
            driver.save_screenshot("screenshots/customer_button_error.png")
            logger.info("📸 按钮调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"点击客户投入公海按钮异常: {e}")
        try:
            driver.save_screenshot("screenshots/customer_public_sea_error.png")
            logger.info("📸 错误截图已保存")
        except:
            pass
        return False


def search_customer_by_id(driver, user_id="7156"):
    """
    通过批量查用户ID功能搜索指定客户
    
    Args:
        driver: Selenium WebDriver实例
        user_id: 用户ID，默认为7156
    
    Returns:
        bool: 搜索是否成功
    """
    try:
        logger.info(f"🔍 开始通过用户ID {user_id} 搜索客户...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 点击批量查用户ID按钮
        logger.info("📋 点击批量查用户ID按钮...")
        
        js_click_batch_search = """
        // 查找批量查用户ID按钮
        var buttons = document.querySelectorAll('button.el-button--default');
        var targetButton = null;
        
        for (var i = 0; i < buttons.length; i++) {
            var button = buttons[i];
            var span = button.querySelector('span');
            if (span && span.textContent.trim() === '批量查用户ID') {
                console.log('找到批量查用户ID按钮');
                targetButton = button;
                break;
            }
        }
        
        if (!targetButton) {
            console.log('未找到批量查用户ID按钮');
            // 列出所有可用按钮
            var allButtons = document.querySelectorAll('button');
            var buttonTexts = [];
            for (var j = 0; j < allButtons.length; j++) {
                var btnText = allButtons[j].textContent.trim();
                if (btnText) buttonTexts.push(btnText);
            }
            return { success: false, error: '未找到批量查用户ID按钮', buttons: buttonTexts };
        }
        
        // 点击按钮
        targetButton.click();
        console.log('批量查用户ID按钮已点击');
        return { success: true };
        """
        
        click_result = driver.execute_script(js_click_batch_search)
        
        if click_result and click_result.get('success'):
            logger.info("✅ 批量查用户ID按钮已点击成功！")
            
            # 等待弹窗出现
            time.sleep(2)
            
            # 在输入框中输入用户ID
            logger.info(f"✍️ 在输入框中输入用户ID: {user_id}")
            
            js_input_user_id = """
            // 查找用户ID输入框
            var textareas = document.querySelectorAll('textarea.el-textarea__inner');
            var targetTextarea = null;
            
            for (var i = 0; i < textareas.length; i++) {
                var textarea = textareas[i];
                var placeholder = textarea.getAttribute('placeholder');
                if (placeholder && placeholder.includes('请输入用户Id')) {
                    console.log('找到用户ID输入框');
                    targetTextarea = textarea;
                    break;
                }
            }
            
            if (!targetTextarea) {
                console.log('未找到用户ID输入框');
                return { success: false, error: '未找到用户ID输入框' };
            }
            
            // 清空并输入用户ID
            targetTextarea.value = '';
            targetTextarea.value = '""" + user_id + """';
            
            // 触发input事件确保Vue检测到变化
            var inputEvent = new Event('input', { bubbles: true });
            targetTextarea.dispatchEvent(inputEvent);
            
            // 触发change事件
            var changeEvent = new Event('change', { bubbles: true });
            targetTextarea.dispatchEvent(changeEvent);
            
            console.log('用户ID已输入:', targetTextarea.value);
            return { success: true, value: targetTextarea.value };
            """
            
            input_result = driver.execute_script(js_input_user_id)
            
            if input_result and input_result.get('success'):
                logger.info(f"✅ 用户ID已输入: {input_result.get('value', user_id)}")
                
                # 等待输入完成
                time.sleep(1)
                
                # 点击查询按钮
                logger.info("🔍 点击查询按钮...")
                
                # 使用Selenium方式点击查询按钮，更可靠
                try:
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
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
                            driver.save_screenshot("screenshots/customer_search_by_id_result.png")
                            logger.info("📸 用户ID查询结果截图已保存")
                            
                            return True
                        else:
                            logger.error("❌ 所有查询按钮点击方式都失败")
                    else:
                        logger.error("❌ 未找到可用的查询按钮")
                        
                except Exception as selenium_error:
                    logger.error(f"❌ Selenium查询按钮点击异常: {selenium_error}")
                
                # 如果Selenium方式失败，回退到JavaScript方式但增加验证
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
                    
                    // 等待一下检查是否有反应
                    setTimeout(function() {
                        console.log('点击后检查页面状态');
                    }, 1000);
                    
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
                    driver.save_screenshot("screenshots/customer_search_by_id_result.png")
                    logger.info("📸 用户ID查询结果截图已保存")
                    
                    return True
                else:
                    error_msg = search_result.get('error', '未知错误') if search_result else '点击失败'
                    logger.error(f"❌ 查询按钮点击失败: {error_msg}")
                    
                    if isinstance(search_result, dict) and 'errors' in search_result:
                        logger.error(f"   错误详情: {search_result['errors']}")
                    
                    # 截图调试
                    driver.save_screenshot("screenshots/search_button_error.png")
                    logger.info("📸 查询按钮调试截图已保存")
                    
                    return False
            else:
                error_msg = input_result.get('error', '未知错误') if input_result else '输入失败'
                logger.error(f"❌ 用户ID输入失败: {error_msg}")
                
                # 截图调试
                driver.save_screenshot("screenshots/user_id_input_error.png")
                logger.info("📸 用户ID输入调试截图已保存")
                
                return False
        else:
            error_msg = click_result.get('error', '未知错误') if click_result else '点击失败'
            logger.error(f"❌ 批量查用户ID按钮点击失败: {error_msg}")
            
            if isinstance(click_result, dict) and 'buttons' in click_result:
                logger.error(f"   可用按钮: {click_result['buttons']}")
            
            # 截图调试
            driver.save_screenshot("screenshots/batch_search_button_error.png")
            logger.info("📸 批量查用户ID按钮调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"通过用户ID搜索客户异常: {e}")
        try:
            driver.save_screenshot("screenshots/search_customer_by_id_error.png")
            logger.info("📸 搜索客户错误截图已保存")
        except:
            pass
        return False


def click_searched_customer_public_sea_button(driver, user_id="7156"):
    """
    在搜索结果中点击指定客户的投入公海按钮
    
    Args:
        driver: Selenium WebDriver实例
        user_id: 用户ID，用于验证
    
    Returns:
        bool: 点击是否成功
    """
    try:
        logger.info(f"🎯 在搜索结果中查找用户ID {user_id} 的客户...")
        
        # 等待搜索结果加载
        time.sleep(2)
        
        # 在搜索结果中查找并点击操作按钮
        js_click_searched_customer = """
        // 查找搜索结果中的客户行
        var tableRows = document.querySelectorAll('tr.el-table__row');
        var targetRow = null;
        var targetIndex = -1;
        
        console.log('搜索结果中的行数:', tableRows.length);
        
        // 由于是通过ID搜索的，应该只有一行结果，直接操作第一行
        if (tableRows.length > 0) {
            targetRow = tableRows[0];
            targetIndex = 0;
            console.log('使用搜索结果第一行作为目标客户');
        }
        
        if (!targetRow) {
            console.log('搜索结果中未找到客户行');
            return { success: false, error: '搜索结果中未找到客户行' };
        }
        
        // 在目标行中查找操作按钮
        var dropdown = targetRow.querySelector('div.el-dropdown');
        if (!dropdown) {
            console.log('在搜索结果行中未找到操作下拉菜单');
            return { success: false, error: '未找到操作下拉菜单', targetIndex: targetIndex };
        }
        
        // 查找操作按钮
        var operationBtn = dropdown.querySelector('button.el-button--info');
        if (!operationBtn) {
            operationBtn = dropdown.querySelector('button[type="button"]');
        }
        if (!operationBtn) {
            operationBtn = dropdown.querySelector('button');
        }
        
        if (operationBtn) {
            console.log('在搜索结果中找到操作按钮，准备点击');
            operationBtn.click();
            return { success: true, step: 'button_clicked', targetIndex: targetIndex };
        } else {
            console.log('在搜索结果中未找到操作按钮');
            return { success: false, error: '未找到操作按钮', targetIndex: targetIndex };
        }
        """
        
        result = driver.execute_script(js_click_searched_customer)
        
        if result and result.get('success'):
            target_index = result.get('targetIndex', -1)
            logger.info(f"✅ 搜索结果中的客户操作按钮已点击！")
            logger.info(f"   目标客户行索引: {target_index}")
            
            # 等待菜单展开
            time.sleep(1.5)
            
            # 查找并点击"投入公海"菜单项
            logger.info("🔍 查找投入公海菜单项...")
            
            click_public_sea_menu_js = """
            var menuItems = document.querySelectorAll('li.el-dropdown-menu__item');
            var menuTexts = [];
            
            for (var i = 0; i < menuItems.length; i++) {
                var item = menuItems[i];
                var text = item.textContent.trim();
                menuTexts.push(text);
                
                if (text === '投入公海') {
                    console.log('找到投入公海菜单项，执行点击');
                    item.click();
                    return { success: true, clicked: '投入公海' };
                }
            }
            
            console.log('可用菜单项:', menuTexts);
            return { success: false, menus: menuTexts };
            """
            
            menu_result = driver.execute_script(click_public_sea_menu_js)
            
            if menu_result and menu_result.get('success'):
                logger.info(f"✅ 投入公海菜单项已点击成功！")
                
                # 等待弹窗出现
                time.sleep(2)
                
                # 处理投入公海弹窗
                if handle_customer_public_sea_dialog(driver):
                    logger.info("✅ 投入公海弹窗处理成功！")
                    
                    # 截图确认最终结果
                    driver.save_screenshot("screenshots/customer_public_sea_success_by_id.png")
                    logger.info("📸 通过用户ID的客户投入公海成功截图已保存")
                    
                    return True
                else:
                    logger.error("❌ 投入公海弹窗处理失败")
                    return False
            else:
                logger.error("❌ 未找到投入公海菜单项")
                if isinstance(menu_result, dict) and 'menus' in menu_result:
                    logger.error(f"   可用菜单项: {menu_result['menus']}")
                
                # 截图调试
                driver.save_screenshot("screenshots/searched_customer_menu_debug.png")
                logger.info("📸 搜索结果菜单调试截图已保存")
                
                return False
        else:
            error_msg = result.get('error', '未知错误') if result else '操作失败'
            logger.error(f"❌ 搜索结果中的客户操作按钮点击失败: {error_msg}")
            
            if isinstance(result, dict) and 'targetIndex' in result:
                logger.error(f"   目标行索引: {result['targetIndex']}")
            
            # 截图调试
            driver.save_screenshot("screenshots/searched_customer_button_error.png")
            logger.info("📸 搜索结果按钮调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"点击搜索结果中的客户投入公海按钮异常: {e}")
        try:
            driver.save_screenshot("screenshots/searched_customer_error.png")
            logger.info("📸 搜索结果操作错误截图已保存")
        except:
            pass
        return False


def test_customer_private_sea_ipipgo_workflow(driver):
    """
    完整的客户私海IPIPGO导航测试流程
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🎯 开始客户私海IPIPGO导航测试流程...")
        
        # 步骤1: 导航到客户私海页面
        if not navigate_to_customer_private_sea(driver):
            logger.error("❌ 导航到客户私海页面失败")
            return False
        
        # 步骤2: 点击IPIPGO标签页
        if not click_ipipgo_tab(driver):
            logger.error("❌ 点击IPIPGO标签页失败")
            return False
        
        logger.info("�� 客户私海IPIPGO导航测试流程完成！")
        logger.info("   ✅ 成功导航到客户私海页面")
        logger.info("   ✅ 成功点击IPIPGO标签页")
        
        return True
        
    except Exception as e:
        logger.error(f"客户私海IPIPGO导航测试流程异常: {e}")
        return False


def test_customer_private_sea_to_public_workflow(driver):
    """
    完整的客户私海投入公海测试流程
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🎯 开始客户私海投入公海测试流程...")
        
        # 步骤1: 导航到客户私海页面
        if not navigate_to_customer_private_sea(driver):
            logger.error("❌ 导航到客户私海页面失败")
            return False
        
        # 步骤2: 点击IPIPGO标签页
        if not click_ipipgo_tab(driver):
            logger.error("❌ 点击IPIPGO标签页失败")
            return False
        
        # 步骤3: 通过用户ID搜索客户
        if not search_customer_by_id(driver, "7156"):
            logger.error("❌ 通过用户ID搜索客户失败")
            return False
        
        # 步骤4: 在搜索结果中点击客户的投入公海按钮
        if not click_searched_customer_public_sea_button(driver, "7156"):
            logger.error("❌ 点击搜索结果中的客户投入公海按钮失败")
            return False
        
        logger.info("🎉 客户私海投入公海测试流程完成！")
        logger.info("   ✅ 成功导航到客户私海页面")
        logger.info("   ✅ 成功点击IPIPGO标签页")
        logger.info("   ✅ 成功通过用户ID 7156 搜索客户")
        logger.info("   ✅ 成功点击客户投入公海按钮")
        
        return True
        
    except Exception as e:
        logger.error(f"客户私海投入公海测试流程异常: {e}")
        return False


if __name__ == "__main__":
    # 这里可以添加独立测试代码
    logger.info("客户私海模块已加载") 