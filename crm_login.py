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
        
        # 填入用户名和密码
        username_element.clear()
        username_element.send_keys(username)
        password_element.clear()
        password_element.send_keys(password)
        logger.info("✅ 用户名和密码已填入")
        
        # 检查是否有验证码元素
        captcha_present = False
        try:
            # 尝试查找验证码相关元素（可能的验证码输入框或图片）
            captcha_elements = driver.find_elements(By.XPATH, "//input[contains(@placeholder,'验证码') or contains(@placeholder,'captcha')]")
            captcha_img = driver.find_elements(By.XPATH, "//img[contains(@alt,'验证码') or contains(@src,'captcha')]")
            
            if captcha_elements or captcha_img:
                captcha_present = True
                logger.info("🔍 检测到验证码，需要手动输入")
        except:
            pass
        
        if captcha_present:
            # 有验证码时的处理流程
            logger.info("⏳ 请在10秒内手动完成以下操作：")
            logger.info("   1️⃣ 输入验证码")
            logger.info("   2️⃣ 点击登录按钮")
            logger.info("⌛ 等待用户操作中...")
            
            # 等待10秒，让用户输入验证码并点击登录
            time.sleep(10)
            
            # 检测页面是否成功跳转（最多等待15秒）
            logger.info("🔍 检测登录状态...")
            try:
                WebDriverWait(driver, 15).until(
                    lambda d: "test-admin-crm.cd.xiaoxigroup.net" in d.current_url
                )
                logger.info("✅ 登录成功！页面已跳转到CRM系统")
            except:
                # 如果没有跳转，可能还在登录页面，检查是否有错误信息
                try:
                    error_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'错误') or contains(text(),'失败') or contains(text(),'验证码')]")
                    if error_elements:
                        error_msg = error_elements[0].text
                        logger.warning(f"⚠️ 可能的登录错误信息: {error_msg}")
                    else:
                        logger.warning("⚠️ 未检测到明确的错误信息")
                        
                    # 再次等待，以防页面响应较慢
                    WebDriverWait(driver, 10).until(
                        lambda d: "test-admin-crm.cd.xiaoxigroup.net" in d.current_url
                    )
                    logger.info("✅ 登录成功！（延迟跳转）")
                except:
                    logger.error("❌ 登录失败，页面未成功跳转到CRM系统")
                    logger.error("💡 请检查验证码是否正确输入，或重新尝试登录")
                    return False
        else:
            # 没有验证码时的原有流程
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