#!/usr/bin/env python
"""
CRM自动化测试 - 公海线索操作模块
包含公海线索页面导航和跟踪等功能
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置日志
logger = logging.getLogger(__name__)


def navigate_to_public_sea(driver):
    """
    导航到公海线索页面
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 导航是否成功
    """
    try:
        logger.info("🌊 开始导航到公海线索页面...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 点击公海线索菜单
        logger.info("点击公海线索菜单...")
        
        js_click_public_sea_menu = """
        // 查找公海线索菜单项
        var menuItems = document.querySelectorAll('li.el-menu-item.inner-menu-item');
        for (var i = 0; i < menuItems.length; i++) {
            var item = menuItems[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '公海线索' && 
                item.getAttribute('base-path') === '/customerManagement/clews/publicSea') {
                console.log('找到公海线索菜单，准备点击');
                item.click();
                return true;
            }
        }
        console.log('未找到公海线索菜单');
        return false;
        """
        
        if driver.execute_script(js_click_public_sea_menu):
            logger.info("✅ 公海线索菜单已点击")
        else:
            raise Exception("无法找到公海线索菜单")
        
        # 等待页面加载
        time.sleep(3)
        
        # 验证是否成功进入公海线索页面
        js_verify_public_sea_page = """
        // 检查URL是否包含公海线索路径
        var currentUrl = window.location.href;
        return currentUrl.includes('/customerManagement/clews/publicSea') || 
               currentUrl.includes('publicSea');
        """
        
        if driver.execute_script(js_verify_public_sea_page):
            logger.info("✅ 已成功进入公海线索页面")
            
            # 截图确认
            driver.save_screenshot("screenshots/public_sea_page_loaded.png")
            logger.info("📸 公海线索页面加载截图已保存")
            
            return True
        else:
            logger.error("❌ 未能成功进入公海线索页面")
            return False
        
    except Exception as e:
        logger.error(f"导航到公海线索页面异常: {e}")
        try:
            driver.save_screenshot("screenshots/public_sea_navigation_error.png")
        except:
            pass
        return False


def click_track_button_for_clue(driver, clue_name_keyword="私海线索-ui自动化"):
    """
    在公海线索列表中查找指定线索并点击跟踪按钮
    
    Args:
        driver: Selenium WebDriver实例
        clue_name_keyword: 线索名称关键字，用于查找目标线索
    
    Returns:
        bool: 跟踪按钮点击是否成功
    """
    try:
        logger.info(f"🔍 开始查找包含'{clue_name_keyword}'的线索并点击跟踪按钮...")
        
        # 等待表格加载完成
        time.sleep(3)
        
        # 查找并点击跟踪按钮
        js_click_track_button = f"""
        // 查找包含指定关键字的线索行并点击跟踪按钮
        var rows = document.querySelectorAll('tr.el-table__row');
        console.log('找到的表格行数:', rows.length);
        
        for (var i = 0; i < rows.length; i++) {{
            var row = rows[i];
            var cells = row.querySelectorAll('td');
            
            // 查找线索名称列（通常是第2列）
            for (var j = 0; j < cells.length; j++) {{
                var cell = cells[j];
                var spans = cell.querySelectorAll('span[data-v-2fc6bf6a]');
                
                for (var k = 0; k < spans.length; k++) {{
                    var span = spans[k];
                    if (span.textContent.includes('{clue_name_keyword}')) {{
                        console.log('找到匹配的线索:', span.textContent);
                        
                        // 在当前行查找跟踪按钮
                        var trackButtons = row.querySelectorAll('button.el-button--primary.el-button--mini');
                        for (var m = 0; m < trackButtons.length; m++) {{
                            var button = trackButtons[m];
                            var buttonSpan = button.querySelector('span');
                            if (buttonSpan && buttonSpan.textContent.trim() === '跟踪') {{
                                console.log('找到跟踪按钮，准备点击');
                                button.click();
                                return true;
                            }}
                        }}
                    }}
                }}
            }}
        }}
        
        console.log('未找到匹配的线索或跟踪按钮');
        return false;
        """
        
        if driver.execute_script(js_click_track_button):
            logger.info("✅ 跟踪按钮已点击")
            
            # 等待跟踪页面加载
            time.sleep(3)
            
            # 截图确认
            driver.save_screenshot("screenshots/public_sea_track_clicked.png")
            logger.info("📸 公海线索跟踪点击截图已保存")
            
            return True
        else:
            logger.error(f"❌ 未找到包含'{clue_name_keyword}'的线索或跟踪按钮")
            
            # 截图调试
            driver.save_screenshot("screenshots/public_sea_track_not_found.png")
            logger.info("📸 调试截图已保存")
            
            return False
        
    except Exception as e:
        logger.error(f"点击跟踪按钮异常: {e}")
        try:
            driver.save_screenshot("screenshots/public_sea_track_error.png")
        except:
            pass
        return False


def test_public_sea_track_workflow(driver, clue_name_keyword="私海线索-ui自动化"):
    """
    完整的公海线索跟踪测试流程
    
    Args:
        driver: Selenium WebDriver实例
        clue_name_keyword: 线索名称关键字
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🎯 开始公海线索跟踪测试流程...")
        
        # 步骤1: 导航到公海线索页面
        if not navigate_to_public_sea(driver):
            logger.error("❌ 导航到公海线索页面失败")
            return False
        
        # 步骤2: 查找并点击跟踪按钮
        if not click_track_button_for_clue(driver, clue_name_keyword):
            logger.error("❌ 点击跟踪按钮失败")
            return False
        
        logger.info("🎉 公海线索跟踪测试流程完成！")
        logger.info("   ✅ 成功导航到公海线索页面")
        logger.info(f"   ✅ 成功找到并点击'{clue_name_keyword}'的跟踪按钮")
        
        return True
        
    except Exception as e:
        logger.error(f"公海线索跟踪测试流程异常: {e}")
        return False 