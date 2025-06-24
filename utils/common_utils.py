"""
通用工具类
包含截图、等待、文件操作、日期时间等常用功能
"""
import os
import time
import logging
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config.config import Config


logger = logging.getLogger(__name__)


class CommonUtils:
    """通用工具类"""
    
    @staticmethod
    def take_screenshot(driver, filename=None):
        """
        截取屏幕截图
        
        Args:
            driver: WebDriver实例
            filename: 截图文件名，如果不提供则自动生成
            
        Returns:
            截图文件路径
        """
        try:
            # 确保截图目录存在
            os.makedirs(Config.SCREENSHOTS_PATH, exist_ok=True)
            
            # 生成文件名
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            # 确保文件名以.png结尾
            if not filename.endswith('.png'):
                filename += '.png'
            
            filepath = os.path.join(Config.SCREENSHOTS_PATH, filename)
            
            # 截图
            driver.save_screenshot(filepath)
            logger.info(f"截图已保存: {filepath}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    @staticmethod
    def wait_for_element(driver, locator, timeout=None):
        """
        等待元素出现
        
        Args:
            driver: WebDriver实例
            locator: 元素定位器 (By, value)
            timeout: 超时时间，默认使用配置中的值
            
        Returns:
            WebElement对象
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"元素已找到: {locator}")
            return element
        except TimeoutException:
            logger.error(f"等待元素超时: {locator}")
            raise
    
    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=None):
        """
        等待元素可点击
        
        Args:
            driver: WebDriver实例
            locator: 元素定位器 (By, value)
            timeout: 超时时间
            
        Returns:
            WebElement对象
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            logger.debug(f"元素可点击: {locator}")
            return element
        except TimeoutException:
            logger.error(f"等待元素可点击超时: {locator}")
            raise
    
    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=None):
        """
        等待元素可见
        
        Args:
            driver: WebDriver实例
            locator: 元素定位器 (By, value)
            timeout: 超时时间
            
        Returns:
            WebElement对象
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"元素可见: {locator}")
            return element
        except TimeoutException:
            logger.error(f"等待元素可见超时: {locator}")
            raise
    
    @staticmethod
    def wait_for_text_in_element(driver, locator, text, timeout=None):
        """
        等待元素包含指定文本
        
        Args:
            driver: WebDriver实例
            locator: 元素定位器 (By, value)
            text: 期望的文本
            timeout: 超时时间
            
        Returns:
            bool
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        
        try:
            wait = WebDriverWait(driver, timeout)
            result = wait.until(EC.text_to_be_present_in_element(locator, text))
            logger.debug(f"元素包含文本 '{text}': {locator}")
            return result
        except TimeoutException:
            logger.error(f"等待元素包含文本 '{text}' 超时: {locator}")
            return False
    
    @staticmethod
    def is_element_present(driver, locator):
        """
        检查元素是否存在
        
        Args:
            driver: WebDriver实例
            locator: 元素定位器 (By, value)
            
        Returns:
            bool
        """
        try:
            driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    @staticmethod
    def scroll_to_element(driver, element):
        """
        滚动到指定元素
        
        Args:
            driver: WebDriver实例
            element: WebElement对象
        """
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # 等待滚动完成
            logger.debug("已滚动到元素位置")
        except Exception as e:
            logger.error(f"滚动到元素失败: {e}")
    
    @staticmethod
    def scroll_to_top(driver):
        """
        滚动到页面顶部
        
        Args:
            driver: WebDriver实例
        """
        try:
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            logger.debug("已滚动到页面顶部")
        except Exception as e:
            logger.error(f"滚动到页面顶部失败: {e}")
    
    @staticmethod
    def scroll_to_bottom(driver):
        """
        滚动到页面底部
        
        Args:
            driver: WebDriver实例
        """
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            logger.debug("已滚动到页面底部")
        except Exception as e:
            logger.error(f"滚动到页面底部失败: {e}")
    
    @staticmethod
    def get_current_timestamp():
        """
        获取当前时间戳字符串
        
        Returns:
            时间戳字符串 (格式: YYYYmmdd_HHMMSS)
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def get_current_date():
        """
        获取当前日期字符串
        
        Returns:
            日期字符串 (格式: YYYY-MM-DD)
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_current_datetime():
        """
        获取当前日期时间字符串
        
        Returns:
            日期时间字符串 (格式: YYYY-MM-DD HH:MM:SS)
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def clear_and_send_keys(element, text):
        """
        清空输入框并输入文本
        
        Args:
            element: WebElement对象
            text: 要输入的文本
        """
        try:
            element.clear()
            element.send_keys(text)
            logger.debug(f"已输入文本: {text}")
        except Exception as e:
            logger.error(f"输入文本失败: {e}")
            raise
    
    @staticmethod
    def switch_to_new_window(driver):
        """
        切换到新打开的窗口
        
        Args:
            driver: WebDriver实例
            
        Returns:
            新窗口句柄
        """
        try:
            # 获取所有窗口句柄
            all_windows = driver.window_handles
            
            # 切换到最新的窗口
            if len(all_windows) > 1:
                driver.switch_to.window(all_windows[-1])
                logger.debug("已切换到新窗口")
                return all_windows[-1]
            else:
                logger.warning("没有找到新窗口")
                return None
                
        except Exception as e:
            logger.error(f"切换窗口失败: {e}")
            raise
    
    @staticmethod
    def close_current_window_and_switch_back(driver, main_window_handle):
        """
        关闭当前窗口并切换回主窗口
        
        Args:
            driver: WebDriver实例
            main_window_handle: 主窗口句柄
        """
        try:
            driver.close()
            driver.switch_to.window(main_window_handle)
            logger.debug("已关闭当前窗口并切换回主窗口")
        except Exception as e:
            logger.error(f"关闭窗口失败: {e}")
            raise 