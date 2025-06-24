#!/usr/bin/env python
"""
CRM自动化测试 - 登录功能模块
包含SSO登录相关功能
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置日志
logger = logging.getLogger(__name__)


def login_to_crm(driver, username="qinrenchi", password="Sandog031220@"):
    """
    登录到CRM系统
    
    Args:
        driver: Selenium WebDriver实例
        username: 用户名，默认为qinrenchi
        password: 密码，默认为Sandog031220@
    
    Returns:
        bool: 登录是否成功
    """
    try:
        # 登录URL
        url = "https://sso.xiaoxitech.com/login?project=hqhtmsb1&cb=https%3A%2F%2Ftest-admin-crm.cd.xiaoxigroup.net%2Flogin"
        logger.info("正在登录CRM系统...")
        driver.get(url)
        
        time.sleep(2)
        
        # 切换到用户名密码登录（如果需要）
        try:
            username_password_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='用户名密码登录']"))
            )
            username_password_button.click()
            time.sleep(1)
        except:
            pass
        
        # 输入用户名和密码
        username_element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='用户名']"))
        )
        password_element = driver.find_element(By.XPATH, "//input[@placeholder='密码']")
        login_button = driver.find_element(By.XPATH, "//span[text()='登录']")
        
        username_element.clear()
        username_element.send_keys(username)
        password_element.clear()
        password_element.send_keys(password)
        
        login_button.click()
        logger.info("✅ 登录信息已提交")
        
        # 等待页面跳转到CRM系统
        WebDriverWait(driver, 10).until(
            lambda d: "test-admin-crm.cd.xiaoxigroup.net" in d.current_url
        )
        logger.info("✅ 登录CRM系统成功")
        
        return True
        
    except Exception as e:
        logger.error(f"登录CRM系统失败: {e}")
        return False 