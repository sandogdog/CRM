#!/usr/bin/env python
"""
CRM自动化测试 - 工具函数模块
包含随机数据生成等通用功能
"""
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