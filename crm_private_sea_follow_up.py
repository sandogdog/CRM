#!/usr/bin/env python
"""
CRM自动化测试 - 私海线索快速跟进模块
包含快速跟进、跟进面板配置、报价单填写等功能
"""
import time
import logging

# 配置日志
logger = logging.getLogger(__name__)


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


def handle_follow_up_panel(driver):
    """
    处理线索跟进面板的下拉框选择操作
    1. 选择跟进方式为"电话"
    2. 选择跟进结果为"商机转化"
    3. 输入日志记录"UI自动化测试"
    4. 选择客户来源为"付费推广"
    5. 选择公司等级为"A类"
    6. 选择商机类别为"普通商机"
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 操作是否成功
    """
    try:
        logger.info("🎯 开始处理线索跟进面板...")
        
        # 等待跟进面板完全加载
        time.sleep(3)
        
        # 步骤1: 点击第一个下拉框（沟通方式）
        logger.info("1. 点击沟通方式下拉框...")
        
        # 使用更精确的定位策略
        js_click_first_dropdown = """
        // 查找弹窗内所有的el-input__inner输入框
        var inputs = document.querySelectorAll('input.el-input__inner[placeholder="请选择"][readonly]');
        console.log('找到的输入框数量:', inputs.length);
        
        // 过滤出在弹窗内且可见的输入框
        var visibleInputs = [];
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            // 检查是否可见且在合理位置（不在页面角落）
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0 && 
                rect.top > 100 && rect.left > 100 && 
                rect.top < window.innerHeight - 100) {
                visibleInputs.push(input);
                console.log('可见输入框位置:', rect.top, rect.left);
            }
        }
        
        if (visibleInputs.length >= 1) {
            // 点击第一个可见输入框（沟通方式）
            visibleInputs[0].click();
            console.log('点击了第一个输入框 - 沟通方式');
            return true;
        }
        
        console.log('未找到合适的输入框');
        return false;
        """
        
        if driver.execute_script(js_click_first_dropdown):
            logger.info("✅ 沟通方式下拉框已点击")
        else:
            raise Exception("无法找到沟通方式下拉框")
        
        # 等待下拉框选项出现
        time.sleep(2)
        
        # 步骤2: 选择"电话"选项
        logger.info("2. 选择'电话'选项...")
        
        js_select_phone = """
        // 查找包含"电话"的选项
        var items = document.querySelectorAll('li.el-select-dropdown__item[data-v-668541f2]');
        console.log('找到的选项数量:', items.length);
        
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '电话') {
                // 检查选项是否可见
                var rect = item.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    item.click();
                    console.log('选择了电话选项');
                    return true;
                }
            }
        }
        
        console.log('未找到电话选项');
        return false;
        """
        
        if driver.execute_script(js_select_phone):
            logger.info("✅ '电话'选项已选择")
        else:
            raise Exception("无法找到'电话'选项")
        
        # 等待第一个下拉框关闭
        time.sleep(2)
        
        # 步骤3: 点击第二个下拉框（跟进进度）
        logger.info("3. 点击跟进进度下拉框...")
        
        js_click_second_dropdown = """
        // 重新查找所有可见的输入框
        var inputs = document.querySelectorAll('input.el-input__inner[placeholder="请选择"][readonly]');
        console.log('第二次查找的输入框数量:', inputs.length);
        
        var visibleInputs = [];
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0 && 
                rect.top > 100 && rect.left > 100 && 
                rect.top < window.innerHeight - 100) {
                visibleInputs.push(input);
            }
        }
        
        if (visibleInputs.length >= 2) {
            // 点击第二个可见输入框（跟进进度）
            visibleInputs[1].click();
            console.log('点击了第二个输入框 - 跟进进度');
            return true;
        }
        
        console.log('未找到第二个输入框');
        return false;
        """
        
        if driver.execute_script(js_click_second_dropdown):
            logger.info("✅ 跟进进度下拉框已点击")
        else:
            raise Exception("无法找到跟进进度下拉框")
        
        # 等待下拉框选项出现
        time.sleep(2)
        
        # 步骤4: 选择"商机转化"选项
        logger.info("4. 选择'商机转化'选项...")
        
        js_select_conversion = """
        // 查找包含"商机转化"的选项
        var items = document.querySelectorAll('li.el-select-dropdown__item[data-v-668541f2]');
        console.log('第二次找到的选项数量:', items.length);
        
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '商机转化') {
                // 检查选项是否可见
                var rect = item.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    item.click();
                    console.log('选择了商机转化选项');
                    return true;
                }
            }
        }
        
        console.log('未找到商机转化选项');
        return false;
        """
        
        if driver.execute_script(js_select_conversion):
            logger.info("✅ '商机转化'选项已选择")
        else:
            raise Exception("无法找到'商机转化'选项")
        
        # 等待选择完成
        time.sleep(2)
        
        # 步骤5: 输入日志记录
        logger.info("5. 输入日志记录...")
        
        js_input_log = """
        // 查找日志记录输入框
        var textareas = document.querySelectorAll('textarea.el-textarea__inner[placeholder="请输入日志记录"]');
        console.log('找到的日志输入框数量:', textareas.length);
        
        for (var i = 0; i < textareas.length; i++) {
            var textarea = textareas[i];
            var rect = textarea.getBoundingClientRect();
            // 检查是否可见
            if (rect.width > 0 && rect.height > 0) {
                textarea.focus();
                textarea.value = 'UI自动化测试';
                // 触发input事件，确保Vue能检测到值的变化
                var event = new Event('input', { bubbles: true });
                textarea.dispatchEvent(event);
                console.log('已输入日志记录: UI自动化测试');
                return true;
            }
        }
        
        console.log('未找到日志记录输入框');
        return false;
        """
        
        if driver.execute_script(js_input_log):
            logger.info("✅ 日志记录已输入：UI自动化测试")
        else:
            raise Exception("无法找到日志记录输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤6: 点击客户来源下拉框
        logger.info("6. 点击客户来源下拉框...")
        
        js_click_source_dropdown = """
        // 查找客户来源的下拉框（第三个下拉框）
        var inputs = document.querySelectorAll('input.el-input__inner[placeholder="请选择"][readonly]');
        console.log('第三次查找的输入框数量:', inputs.length);
        
        var visibleInputs = [];
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0 && 
                rect.top > 100 && rect.left > 100 && 
                rect.top < window.innerHeight - 100) {
                visibleInputs.push(input);
            }
        }
        
        if (visibleInputs.length >= 3) {
            // 点击第三个可见输入框（客户来源）
            visibleInputs[2].click();
            console.log('点击了第三个输入框 - 客户来源');
            return true;
        }
        
        console.log('未找到客户来源输入框');
        return false;
        """
        
        if driver.execute_script(js_click_source_dropdown):
            logger.info("✅ 客户来源下拉框已点击")
        else:
            raise Exception("无法找到客户来源下拉框")
        
        # 等待下拉框选项出现
        time.sleep(2)
        
        # 步骤7: 选择"付费推广"选项
        logger.info("7. 选择'付费推广'选项...")
        
        js_select_paid_promotion = """
        // 查找包含"付费推广"的选项
        var items = document.querySelectorAll('li.el-select-dropdown__item');
        console.log('客户来源选项数量:', items.length);
        
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '付费推广') {
                // 检查选项是否可见
                var rect = item.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    item.click();
                    console.log('选择了付费推广选项');
                    return true;
                }
            }
        }
        
        console.log('未找到付费推广选项');
        return false;
        """
        
        if driver.execute_script(js_select_paid_promotion):
            logger.info("✅ '付费推广'选项已选择")
        else:
            raise Exception("无法找到'付费推广'选项")
        
        # 等待选择完成
        time.sleep(2)
        
        # 步骤8: 点击公司等级下拉框
        logger.info("8. 点击公司等级下拉框...")
        
        js_click_company_level_dropdown = """
        // 重新查找所有可见的输入框（公司等级）
        var inputs = document.querySelectorAll('input.el-input__inner[placeholder="请选择"][readonly]');
        console.log('第四次查找的输入框数量:', inputs.length);
        
        var visibleInputs = [];
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0 && 
                rect.top > 100 && rect.left > 100 && 
                rect.top < window.innerHeight - 100) {
                visibleInputs.push(input);
                console.log('可见输入框位置:', rect.top, rect.left, '值:', input.value);
            }
        }
        
        if (visibleInputs.length >= 4) {
            // 点击第四个可见输入框（公司等级）
            visibleInputs[3].click();
            console.log('点击了第4个输入框 - 公司等级');
            return true;
        } else if (visibleInputs.length >= 3) {
            // 如果只有3个，点击第3个
            visibleInputs[2].click();
            console.log('点击了第3个输入框 - 公司等级');
            return true;
        }
        
        console.log('未找到公司等级输入框，总数:', visibleInputs.length);
        return false;
        """
        
        if driver.execute_script(js_click_company_level_dropdown):
            logger.info("✅ 公司等级下拉框已点击")
        else:
            raise Exception("无法找到公司等级下拉框")
        
        # 等待下拉框选项出现
        time.sleep(2)
        
        # 步骤9: 选择"A类"选项
        logger.info("9. 选择'A类'选项...")
        
        js_select_a_level = """
        // 查找包含"A类"的选项
        var items = document.querySelectorAll('li.el-select-dropdown__item');
        console.log('公司等级选项数量:', items.length);
        
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === 'A类') {
                // 检查选项是否可见
                var rect = item.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    item.click();
                    console.log('选择了A类选项');
                    return true;
                }
            }
        }
        
        console.log('未找到A类选项');
        return false;
        """
        
        if driver.execute_script(js_select_a_level):
            logger.info("✅ 'A类'选项已选择")
        else:
            raise Exception("无法找到'A类'选项")
        
        # 等待选择完成
        time.sleep(2)
        
        # 步骤10: 点击商机类别下拉框
        logger.info("10. 点击商机类别下拉框...")
        
        js_click_opportunity_type_dropdown = """
        // 查找商机类别下拉框，通过位置和上下文来精确定位
        var inputs = document.querySelectorAll('input.el-input__inner[placeholder="请选择"][readonly]');
        console.log('第五次查找的输入框数量:', inputs.length);
        
        var visibleInputs = [];
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0 && 
                rect.top > 100 && rect.left > 100 && 
                rect.top < window.innerHeight - 100) {
                visibleInputs.push({element: input, top: rect.top, left: rect.left, value: input.value});
                console.log('输入框', i+1, '位置:', rect.top, rect.left, '值:', input.value);
            }
        }
        
        // 按位置从上到下、从左到右排序
        visibleInputs.sort(function(a, b) {
            if (Math.abs(a.top - b.top) < 10) {
                return a.left - b.left; // 同一行按左到右
            }
            return a.top - b.top; // 不同行按上到下
        });
        
        // 根据实际页面结构，商机类别应该是最后一个下拉框
        // 跳过前面已经配置的字段：沟通方式、跟进进度、客户来源、公司等级
        var targetIndex = -1;
        var configuredCount = 0;
        
        for (var i = 0; i < visibleInputs.length; i++) {
            var input = visibleInputs[i];
            console.log('分析输入框', i+1, ':', input.value, '位置:', input.top);
            
            // 跳过已经有值的字段（沟通方式=电话、跟进进度=商机转化、客户来源=付费推广、公司等级=A类）
            if (input.value && input.value !== '请选择' && input.value.trim() !== '') {
                configuredCount++;
                console.log('跳过已配置字段:', input.value);
                continue;
            }
            
            // 找到第一个未配置的字段作为商机类别
            if (configuredCount >= 4) { // 前面4个字段已配置
                targetIndex = i;
                break;
            }
        }
        
        if (targetIndex >= 0) {
            visibleInputs[targetIndex].element.click();
            console.log('点击商机类别输入框，索引:', targetIndex);
            return true;
        } else {
            // 如果上面的逻辑没找到，尝试点击最后一个输入框
            if (visibleInputs.length > 0) {
                var lastIndex = visibleInputs.length - 1;
                visibleInputs[lastIndex].element.click();
                console.log('点击最后一个输入框作为商机类别，索引:', lastIndex);
                return true;
            }
        }
        
        console.log('未找到商机类别输入框，总数:', visibleInputs.length);
        return false;
        """
        
        if driver.execute_script(js_click_opportunity_type_dropdown):
            logger.info("✅ 商机类别下拉框已点击")
        else:
            raise Exception("无法找到商机类别下拉框")
        
        # 等待下拉框选项出现
        time.sleep(2)
        
        # 步骤11: 选择"普通商机"选项
        logger.info("11. 选择'普通商机'选项...")
        
        js_select_normal_opportunity = """
        // 查找包含"普通商机"的选项
        var items = document.querySelectorAll('li.el-select-dropdown__item');
        console.log('商机类别选项数量:', items.length);
        
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '普通商机') {
                // 检查选项是否可见
                var rect = item.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    item.click();
                    console.log('选择了普通商机选项');
                    return true;
                }
            }
        }
        
        console.log('未找到普通商机选项');
        return false;
        """
        
        if driver.execute_script(js_select_normal_opportunity):
            logger.info("✅ '普通商机'选项已选择")
        else:
            raise Exception("无法找到'普通商机'选项")
        
        # 等待选择完成
        time.sleep(2)
        
        # 截图确认结果
        driver.save_screenshot("screenshots/follow_up_panel_configured.png")
        logger.info("📸 跟进面板配置截图已保存")
        
        logger.info("🎉 线索跟进面板配置完成！")
        logger.info("   ✅ 沟通方式: 电话")
        logger.info("   ✅ 跟进进度: 商机转化")
        logger.info("   ✅ 日志记录: UI自动化测试")
        logger.info("   ✅ 客户来源: 付费推广")
        logger.info("   ✅ 公司等级: A类")
        logger.info("   ✅ 商机类别: 普通商机")
        
        return True
        
    except Exception as e:
        logger.error(f"处理跟进面板异常: {e}")
        try:
            driver.save_screenshot("screenshots/follow_up_panel_error.png")
        except:
            pass
        return False


def handle_quotation_tab(driver):
    """
    处理报价单页面的操作
    1. 点击报价单标签页
    2. 填写甲方公司信息（公司、地址、联系人、电话、邮箱）
    3. 填写乙方公司信息（公司选择、联系人、电话、邮箱）
    4. 填写套餐信息（套餐类型、收费项目、套餐明细）
    5. 保存
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 操作是否成功
    """
    try:
        logger.info("🎯 开始处理报价单页面...")
        
        # 步骤1: 点击报价单标签页
        logger.info("1. 点击报价单标签页...")
        
        js_click_quotation_tab = """
        // 查找报价单标签页
        var quotationTab = document.querySelector('#tab-quotation');
        if (quotationTab) {
            var rect = quotationTab.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                quotationTab.click();
                console.log('点击了报价单标签页');
                return true;
            }
        }
        
        console.log('未找到报价单标签页');
        return false;
        """
        
        if driver.execute_script(js_click_quotation_tab):
            logger.info("✅ 报价单标签页已点击")
        else:
            raise Exception("无法找到报价单标签页")
        
        # 等待页面切换
        time.sleep(3)
        
        # 步骤2: 填写甲方公司
        logger.info("2. 填写甲方公司...")
        
        js_fill_company = """
        // 查找甲方公司输入框
        var companyInputs = document.querySelectorAll('input.el-input__inner[placeholder="请输入甲方公司"]');
        console.log('找到的甲方公司输入框数量:', companyInputs.length);
        
        for (var i = 0; i < companyInputs.length; i++) {
            var input = companyInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                input.focus();
                input.value = '1';
                // 触发input事件
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                console.log('已填写甲方公司: 1');
                return true;
            }
        }
        
        console.log('未找到甲方公司输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_company):
            logger.info("✅ 甲方公司已填写：1")
        else:
            raise Exception("无法找到甲方公司输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤3: 填写甲方地址
        logger.info("3. 填写甲方地址...")
        
        js_fill_address = """
        // 查找甲方地址输入框
        var addressInputs = document.querySelectorAll('input.el-input__inner[placeholder="请输入甲方公司地址"]');
        console.log('找到的甲方地址输入框数量:', addressInputs.length);
        
        for (var i = 0; i < addressInputs.length; i++) {
            var input = addressInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                input.focus();
                input.value = '1';
                // 触发input事件
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                console.log('已填写甲方地址: 1');
                return true;
            }
        }
        
        console.log('未找到甲方地址输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_address):
            logger.info("✅ 甲方地址已填写：1")
        else:
            raise Exception("无法找到甲方地址输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤4: 填写甲方联系人
        logger.info("4. 填写甲方联系人...")
        
        js_fill_contact = """
        // 查找甲方联系人输入框
        var contactInputs = document.querySelectorAll('input.el-input__inner[placeholder="请输入联系人姓名"]');
        console.log('找到的联系人输入框数量:', contactInputs.length);
        
        for (var i = 0; i < contactInputs.length; i++) {
            var input = contactInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                input.focus();
                input.value = '秦仁驰';
                // 触发input事件
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                console.log('已填写联系人: 秦仁驰');
                return true;
            }
        }
        
        console.log('未找到联系人输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_contact):
            logger.info("✅ 甲方联系人已填写：秦仁驰")
        else:
            raise Exception("无法找到甲方联系人输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤5: 填写甲方联系电话
        logger.info("5. 填写甲方联系电话...")
        
        js_fill_phone = """
        // 查找甲方联系电话输入框
        var phoneInputs = document.querySelectorAll('input.el-input__inner[placeholder="请输入联系电话"]');
        console.log('找到的联系电话输入框数量:', phoneInputs.length);
        
        for (var i = 0; i < phoneInputs.length; i++) {
            var input = phoneInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                input.focus();
                input.value = '15271193874';
                // 触发input事件
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                console.log('已填写联系电话: 15271193874');
                return true;
            }
        }
        
        console.log('未找到联系电话输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_phone):
            logger.info("✅ 甲方联系电话已填写：15271193874")
        else:
            raise Exception("无法找到甲方联系电话输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤6: 填写甲方邮箱
        logger.info("6. 填写甲方邮箱...")
        
        js_fill_email = """
        // 查找甲方邮箱输入框
        var emailInputs = document.querySelectorAll('input.el-input__inner[placeholder="请输入甲方邮箱"]');
        console.log('找到的邮箱输入框数量:', emailInputs.length);
        
        for (var i = 0; i < emailInputs.length; i++) {
            var input = emailInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                input.focus();
                input.value = 'sandog_fan@qq.com';
                // 触发input事件
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                console.log('已填写邮箱: sandog_fan@qq.com');
                return true;
            }
        }
        
        console.log('未找到邮箱输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_email):
            logger.info("✅ 甲方邮箱已填写：sandog_fan@qq.com")
        else:
            raise Exception("无法找到甲方邮箱输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤7: 点击乙方公司下拉框
        logger.info("7. 点击乙方公司下拉框...")
        
        js_click_party_b_company = """
        // 查找乙方公司下拉框（在报价单页面中）
        var inputs = document.querySelectorAll('input.el-input__inner[placeholder="请选择"][readonly]');
        console.log('找到的下拉框数量:', inputs.length);
        
        // 在报价单页面中查找乙方公司下拉框
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                // 检查是否在报价单页面的可见区域内
                var tabPane = document.querySelector('#pane-quotation');
                if (tabPane && tabPane.contains(input)) {
                    input.click();
                    console.log('点击了乙方公司下拉框');
                    return true;
                }
            }
        }
        
        console.log('未找到乙方公司下拉框');
        return false;
        """
        
        if driver.execute_script(js_click_party_b_company):
            logger.info("✅ 乙方公司下拉框已点击")
        else:
            raise Exception("无法找到乙方公司下拉框")
        
        # 等待下拉框选项出现
        time.sleep(2)
        
        # 步骤8: 选择"南京光年之内网络科技有限公司"
        logger.info("8. 选择'南京光年之内网络科技有限公司'...")
        
        js_select_party_b_company = """
        // 查找并选择南京光年之内网络科技有限公司
        var items = document.querySelectorAll('li.el-select-dropdown__item[data-v-786664d6]');
        console.log('找到的乙方公司选项数量:', items.length);
        
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '南京光年之内网络科技有限公司') {
                var rect = item.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    item.click();
                    console.log('选择了南京光年之内网络科技有限公司');
                    return true;
                }
            }
        }
        
        console.log('未找到南京光年之内网络科技有限公司选项');
        return false;
        """
        
        if driver.execute_script(js_select_party_b_company):
            logger.info("✅ '南京光年之内网络科技有限公司'已选择")
        else:
            raise Exception("无法找到'南京光年之内网络科技有限公司'选项")
        
        # 等待选择完成
        time.sleep(2)
        
        # 步骤9: 填写乙方联系人
        logger.info("9. 填写乙方联系人...")
        
        js_fill_party_b_contact = """
        // 查找乙方联系人输入框
        var contactInputs = document.querySelectorAll('input.el-input__inner[placeholder="乙方联系人"]');
        console.log('找到的乙方联系人输入框数量:', contactInputs.length);
        
        for (var i = 0; i < contactInputs.length; i++) {
            var input = contactInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                input.focus();
                input.value = '秦仁驰';
                // 触发input事件
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                console.log('已填写乙方联系人: 秦仁驰');
                return true;
            }
        }
        
        console.log('未找到乙方联系人输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_party_b_contact):
            logger.info("✅ 乙方联系人已填写：秦仁驰")
        else:
            raise Exception("无法找到乙方联系人输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤10: 填写乙方联系电话
        logger.info("10. 填写乙方联系电话...")
        
        js_fill_party_b_phone = """
        // 查找乙方联系电话输入框
        var phoneInputs = document.querySelectorAll('input.el-input__inner[placeholder="乙方联系电话"]');
        console.log('找到的乙方联系电话输入框数量:', phoneInputs.length);
        
        for (var i = 0; i < phoneInputs.length; i++) {
            var input = phoneInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                input.focus();
                input.value = '15271193874';
                // 触发input事件
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                console.log('已填写乙方联系电话: 15271193874');
                return true;
            }
        }
        
        console.log('未找到乙方联系电话输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_party_b_phone):
            logger.info("✅ 乙方联系电话已填写：15271193874")
        else:
            raise Exception("无法找到乙方联系电话输入框")
        
        # 等待输入完成
        time.sleep(1)
        
        # 步骤11: 填写乙方邮箱
        logger.info("11. 填写乙方邮箱...")
        
        js_fill_party_b_email = """
        // 查找乙方邮箱输入框
        var emailInputs = document.querySelectorAll('input.el-input__inner[placeholder="乙方邮箱"]');
        console.log('找到的乙方邮箱输入框数量:', emailInputs.length);
        
        for (var i = 0; i < emailInputs.length; i++) {
            var input = emailInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                input.focus();
                input.value = 'sandog_fan@qq.com';
                // 触发input事件
                var event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
                console.log('已填写乙方邮箱: sandog_fan@qq.com');
                return true;
            }
        }
        
        console.log('未找到乙方邮箱输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_party_b_email):
            logger.info("✅ 乙方邮箱已填写：sandog_fan@qq.com")
        else:
            raise Exception("无法找到乙方邮箱输入框")
        
        # 等待输入完成
        time.sleep(2)
        
        # 步骤12: 点击套餐类型下拉框
        logger.info("12. 点击套餐类型下拉框...")
        
        js_click_package_type = """
        // 查找套餐类型下拉框
        var inputs = document.querySelectorAll('input.el-input__inner[placeholder="请选择"][readonly]');
        console.log('查找套餐类型下拉框，找到的输入框数量:', inputs.length);
        
        // 在报价单页面中查找剩余的下拉框（套餐类型）
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                // 检查是否在报价单页面的可见区域内且未被选择
                var tabPane = document.querySelector('#pane-quotation');
                if (tabPane && tabPane.contains(input) && !input.value) {
                    input.click();
                    console.log('点击了套餐类型下拉框');
                    return true;
                }
            }
        }
        
        console.log('未找到套餐类型下拉框');
        return false;
        """
        
        if driver.execute_script(js_click_package_type):
            logger.info("✅ 套餐类型下拉框已点击")
        else:
            raise Exception("无法找到套餐类型下拉框")
        
        # 等待下拉框选项出现
        time.sleep(2)
        
        # 步骤13: 选择"基础套餐"
        logger.info("13. 选择'基础套餐'...")
        
        js_select_basic_package = """
        // 查找并选择基础套餐
        var items = document.querySelectorAll('li.el-select-dropdown__item[data-v-786664d6]');
        console.log('找到的套餐类型选项数量:', items.length);
        
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '基础套餐') {
                var rect = item.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    item.click();
                    console.log('选择了基础套餐');
                    return true;
                }
            }
        }
        
        console.log('未找到基础套餐选项');
        return false;
        """
        
        if driver.execute_script(js_select_basic_package):
            logger.info("✅ '基础套餐'已选择")
        else:
            raise Exception("无法找到'基础套餐'选项")
        
        # 等待选择完成
        time.sleep(2)
        
        # 步骤14: 点击收费项目下拉框
        logger.info("14. 点击收费项目下拉框...")
        
        js_click_charge_item = """
        // 查找收费项目下拉框
        var inputs = document.querySelectorAll('input.el-input__inner[placeholder="请选择"][readonly]');
        console.log('查找收费项目下拉框，找到的输入框数量:', inputs.length);
        
        // 在报价单页面中查找剩余的下拉框（收费项目）
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                // 检查是否在报价单页面的可见区域内且未被选择
                var tabPane = document.querySelector('#pane-quotation');
                if (tabPane && tabPane.contains(input) && !input.value) {
                    input.click();
                    console.log('点击了收费项目下拉框');
                    return true;
                }
            }
        }
        
        console.log('未找到收费项目下拉框');
        return false;
        """
        
        if driver.execute_script(js_click_charge_item):
            logger.info("✅ 收费项目下拉框已点击")
        else:
            raise Exception("无法找到收费项目下拉框")
        
        # 等待下拉框选项出现
        time.sleep(2)
        
        # 步骤15: 选择"年度套餐"
        logger.info("15. 选择'年度套餐'...")
        
        js_select_annual_package = """
        // 查找并选择年度套餐
        var items = document.querySelectorAll('li.el-select-dropdown__item[data-v-786664d6]');
        console.log('找到的收费项目选项数量:', items.length);
        
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var span = item.querySelector('span');
            if (span && span.textContent.trim() === '年度套餐') {
                var rect = item.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    item.click();
                    console.log('选择了年度套餐');
                    return true;
                }
            }
        }
        
        console.log('未找到年度套餐选项');
        return false;
        """
        
        if driver.execute_script(js_select_annual_package):
            logger.info("✅ '年度套餐'已选择")
        else:
            raise Exception("无法找到'年度套餐'选项")
        
        # 等待选择完成
        time.sleep(2)
        
        # 步骤16: 填写套餐明细
        logger.info("16. 填写套餐明细...")
        
        js_fill_package_details = """
        // 查找套餐明细输入框
        var detailInputs = document.querySelectorAll('input.el-input__inner[placeholder="请输入收费明细"]');
        console.log('找到的套餐明细输入框数量:', detailInputs.length);
        
        for (var i = 0; i < detailInputs.length; i++) {
            var input = detailInputs[i];
            var rect = input.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                // 检查是否在报价单页面的可见区域内
                var tabPane = document.querySelector('#pane-quotation');
                if (tabPane && tabPane.contains(input)) {
                    input.focus();
                    input.value = 'UI自动化测试';
                    // 触发input事件
                    var event = new Event('input', { bubbles: true });
                    input.dispatchEvent(event);
                    console.log('已填写套餐明细: UI自动化测试');
                    return true;
                }
            }
        }
        
        console.log('未找到套餐明细输入框');
        return false;
        """
        
        if driver.execute_script(js_fill_package_details):
            logger.info("✅ 套餐明细已填写：UI自动化测试")
        else:
            raise Exception("无法找到套餐明细输入框")
        
        # 等待输入完成
        time.sleep(2)
        
        # 步骤17: 点击保存按钮
        logger.info("17. 点击保存按钮...")
        
        js_click_save_button = """
        // 查找保存按钮
        var saveButtons = document.querySelectorAll('button.el-button.el-button--primary[data-v-668541f2]');
        console.log('找到的保存按钮数量:', saveButtons.length);
        
        for (var i = 0; i < saveButtons.length; i++) {
            var button = saveButtons[i];
            var span = button.querySelector('span');
            if (span && span.textContent.trim() === '保存') {
                var rect = button.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && !button.disabled) {
                    button.click();
                    console.log('点击了保存按钮');
                    return true;
                }
            }
        }
        
        console.log('未找到保存按钮');
        return false;
        """
        
        if driver.execute_script(js_click_save_button):
            logger.info("✅ 保存按钮已点击")
        else:
            raise Exception("无法找到保存按钮")
        
        # 等待保存完成
        time.sleep(3)
        
        # 截图确认结果
        driver.save_screenshot("screenshots/quotation_tab_filled.png")
        logger.info("📸 报价单页面填写截图已保存")
        
        logger.info("🎉 报价单页面填写完成！")
        logger.info("   ✅ 甲方公司: 1")
        logger.info("   ✅ 甲方地址: 1")
        logger.info("   ✅ 甲方联系人: 秦仁驰")
        logger.info("   ✅ 甲方联系电话: 15271193874")
        logger.info("   ✅ 甲方邮箱: sandog_fan@qq.com")
        logger.info("   ✅ 乙方公司: 南京光年之内网络科技有限公司")
        logger.info("   ✅ 乙方联系人: 秦仁驰")
        logger.info("   ✅ 乙方联系电话: 15271193874")
        logger.info("   ✅ 乙方邮箱: sandog_fan@qq.com")
        logger.info("   ✅ 套餐类型: 基础套餐")
        logger.info("   ✅ 收费项目: 年度套餐")
        logger.info("   ✅ 套餐明细: UI自动化测试")
        logger.info("   ✅ 保存操作已完成")
        
        return True
        
    except Exception as e:
        logger.error(f"处理报价单页面异常: {e}")
        try:
            driver.save_screenshot("screenshots/quotation_tab_error.png")
        except:
            pass
        return False


def complete_follow_up_process(driver):
    """
    完整的快速跟进流程：点击快速跟进按钮 + 处理跟进面板 + 填写报价单
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 完整流程是否成功
    """
    try:
        logger.info("🚀 开始完整的快速跟进流程...")
        
        # 第一步：点击快速跟进按钮
        if not click_quick_follow_up(driver):
            logger.error("❌ 快速跟进按钮点击失败，终止流程")
            return False
        
        # 第二步：处理跟进面板
        if not handle_follow_up_panel(driver):
            logger.error("❌ 跟进面板处理失败")
            return False
        
        # 第三步：处理报价单页面
        if not handle_quotation_tab(driver):
            logger.error("❌ 报价单页面处理失败")
            return False
        
        logger.info("🎉 完整的快速跟进流程执行成功！")
        return True
        
    except Exception as e:
        logger.error(f"完整快速跟进流程异常: {e}")
        return False


def test_private_sea_follow_up_workflow(driver):
    """
    完整的私海线索快速跟进测试流程
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 测试是否成功
    """
    try:
        logger.info("🚀 开始私海线索快速跟进测试流程...")
        
        # 执行完整的快速跟进流程
        success = complete_follow_up_process(driver)
        
        if success:
            logger.info("🎉 私海线索快速跟进测试流程完成！")
            logger.info("   ✅ 快速跟进按钮点击成功")
            logger.info("   ✅ 跟进面板配置成功")
            logger.info("   ✅ 报价单处理成功")
        else:
            logger.error("❌ 私海线索快速跟进测试流程失败")
        
        return success
        
    except Exception as e:
        logger.error(f"私海线索快速跟进测试流程异常: {e}")
        return False 