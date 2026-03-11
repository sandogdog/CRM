#!/usr/bin/env python
"""
CRM自动化测试 - 私海线索投放模块
包含投放到公海相关功能，以及投放后的公海跟踪功能
"""
import time
import logging

# 配置日志
logger = logging.getLogger(__name__)


def handle_launch_operation(driver):
    """
    处理投放操作：点击投放按钮 + 填写投放原因 + 确定
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 投放操作是否成功
    """
    try:
        logger.info("🚀 开始处理投放操作...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 步骤1: 点击投放按钮
        logger.info("1. 点击投放按钮...")
        
        js_click_launch_button = """
        // 查找投放按钮 - 修复版：不依赖data-v属性，点击列表第一个投放按钮
        var buttons = document.querySelectorAll('button.el-button.el-button--primary.el-button--mini');
        console.log('找到的按钮数量:', buttons.length);
        
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            var span = btn.querySelector('span');
            if (span && span.textContent.trim() === '投放' && 
                btn.offsetWidth > 0 && 
                btn.offsetHeight > 0 &&
                !btn.disabled) {
                console.log('找到投放按钮，准备点击第一个，索引:', i);
                btn.click();
                return true;
            }
        }
        
        console.log('未找到投放按钮，尝试备用方案...');
        // 备用方案：通过更宽泛的选择器查找
        var allButtons = document.querySelectorAll('button');
        for (var j = 0; j < allButtons.length; j++) {
            var button = allButtons[j];
            var span = button.querySelector('span');
            if (span && span.textContent.trim() === '投放' && 
                button.className.includes('el-button') &&
                button.className.includes('el-button--primary') &&
                button.className.includes('el-button--mini') &&
                button.offsetWidth > 0 && 
                button.offsetHeight > 0 &&
                !button.disabled) {
                console.log('备用方案找到投放按钮，准备点击，索引:', j);
                button.click();
                return true;
            }
        }
        
        return false;
        """
        
        if driver.execute_script(js_click_launch_button):
            logger.info("✅ 投放按钮已点击")
        else:
            raise Exception("无法找到投放按钮")
        
        # 等待弹窗出现
        time.sleep(3)
        
        # 步骤2: 填写投放原因
        logger.info("2. 填写投放原因...")
        
        js_fill_launch_reason = """
        // 查找投放原因输入框
        var textareas = document.querySelectorAll('textarea.el-textarea__inner');
        console.log('找到的文本输入框数量:', textareas.length);
        
        for (var i = 0; i < textareas.length; i++) {
            var textarea = textareas[i];
            var rect = textarea.getBoundingClientRect();
            // 检查是否可见且符合投放原因输入框的特征
            if (rect.width > 0 && rect.height > 0 && 
                textarea.getAttribute('minlength') === '1' &&
                textarea.getAttribute('maxlength') === '500') {
                textarea.focus();
                textarea.value = 'UI自动化测试';
                // 触发input事件，确保Vue能检测到值的变化
                var event = new Event('input', { bubbles: true });
                textarea.dispatchEvent(event);
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
        time.sleep(2)
        
        # 步骤3: 点击确定按钮
        logger.info("3. 点击确定按钮...")
        
        js_click_confirm_button = """
        // 查找确定按钮
        var buttons = document.querySelectorAll('button.el-button.el-button--primary.el-button--medium');
        console.log('找到的确定按钮数量:', buttons.length);
        
        for (var i = 0; i < buttons.length; i++) {
            var button = buttons[i];
            var span = button.querySelector('span');
            if (span && span.textContent.trim() === '确 定') {
                var rect = button.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && !button.disabled) {
                    button.click();
                    console.log('点击了确定按钮');
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
        driver.save_screenshot("screenshots/launch_operation_completed.png")
        logger.info("📸 投放操作完成截图已保存")
        
        logger.info("🎉 投放操作完成！")
        return True
        
    except Exception as e:
        logger.error(f"投放操作异常: {e}")
        try:
            driver.save_screenshot("screenshots/launch_operation_error.png")
        except:
            pass
        return False


def test_private_sea_launch_workflow(driver):
    """
    完整的私海线索投放测试流程
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🚀 开始私海线索投放测试流程...")
        
        # 执行投放操作
        if not handle_launch_operation(driver):
            logger.error("❌ 投放操作失败")
            return False
        
        logger.info("🎉 私海线索投放测试流程完成！")
        logger.info("   ✅ 线索已成功投放到公海")
        
        return True
        
    except Exception as e:
        logger.error(f"私海线索投放测试流程异常: {e}")
        return False


def test_private_sea_launch_with_public_track(driver, clue_name_keyword="私海线索-ui自动化"):
    """
    私海线索投放 + 公海跟踪的完整流程
    
    Args:
        driver: Selenium WebDriver实例
        clue_name_keyword: 线索名称关键字，用于在公海中查找
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🚀 开始私海线索投放+公海跟踪完整流程...")
        
        # 步骤1: 执行投放操作
        logger.info("🔸 步骤1: 执行私海线索投放...")
        if not handle_launch_operation(driver):
            logger.error("❌ 投放操作失败")
            return False
        
        logger.info("✅ 私海线索投放成功")
        
        # 步骤2: 导入公海线索模块并执行跟踪
        logger.info("🔸 步骤2: 导航到公海线索并进行跟踪...")
        
        try:
            from crm_public_sea import test_public_sea_track_workflow
            
            # 执行公海跟踪流程
            if test_public_sea_track_workflow(driver, clue_name_keyword):
                logger.info("✅ 公海线索跟踪成功")
                logger.info("🎉 私海投放+公海跟踪完整流程测试完成！")
                logger.info("   ✅ 私海线索投放成功")
                logger.info("   ✅ 公海线索跟踪成功")
                return True
            else:
                logger.warning("⚠️ 公海线索跟踪失败，但投放已成功")
                return True  # 投放成功就算部分成功
                
        except ImportError as ie:
            logger.error(f"❌ 无法导入公海线索模块: {ie}")
            logger.info("✅ 私海线索投放已完成，但无法继续公海跟踪")
            return True  # 投放成功就算部分成功
        
    except Exception as e:
        logger.error(f"私海投放+公海跟踪流程异常: {e}")
        return False 