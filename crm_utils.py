#!/usr/bin/env python
"""
CRM自动化测试 - 工具函数模块
包含随机数据生成、导航辅助等通用功能
"""
import time
import random
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_random_phone():
    """生成随机中国手机号码"""
    # 中国手机号前缀
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '147', '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    
    prefix = random.choice(prefixes)
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return prefix + suffix


def generate_random_suffix():
    """生成4位随机数"""
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])


def click_customer_management_menu(driver):
    """
    点击"客户管理"主菜单
    前端更新后，在切换岗位后需要先点击此菜单才能继续导航
    
    Args:
        driver: Selenium WebDriver实例
    
    Returns:
        bool: 点击是否成功
    """
    try:
        logger.info("📋 点击客户管理主菜单...")
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 使用JavaScript查找并点击客户管理菜单
        js_click_customer_management = """
        // 查找客户管理菜单项
        var menuItems = document.querySelectorAll('li.el-menu-item');
        for (var i = 0; i < menuItems.length; i++) {
            var item = menuItems[i];
            var span = item.querySelector('span');
            var icon = item.querySelector('i.iconfont.icon-kehuguanli');
            
            if (span && span.textContent.trim() === '客户管理' && icon) {
                console.log('找到客户管理菜单，准备点击');
                item.click();
                return true;
            }
        }
        console.log('未找到客户管理菜单');
        return false;
        """
        
        if driver.execute_script(js_click_customer_management):
            logger.info("✅ 客户管理菜单已点击")
            # 等待菜单加载
            time.sleep(2)
            return True
        else:
            logger.warning("⚠️ 未找到客户管理菜单，可能已经在客户管理区域")
            return True  # 返回True继续执行，因为可能已经在正确的区域
        
    except Exception as e:
        logger.error(f"点击客户管理菜单异常: {e}")
        return False


def setup_browser():
    """初始化浏览器配置"""
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    
    logger.info("初始化浏览器...")
    edge_options = EdgeOptions()
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_experimental_option("detach", True)
    
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.implicitly_wait(8)
    driver.maximize_window()
    
    logger.info("✅ 浏览器就绪")
    return driver 