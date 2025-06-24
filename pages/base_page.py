"""
基础页面类
包含所有页面对象的共用方法和属性
"""
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config.config import Config
from utils.common_utils import CommonUtils


logger = logging.getLogger(__name__)


class BasePage:
    """基础页面类"""
    
    def __init__(self, driver):
        """
        初始化基础页面
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.utils = CommonUtils()
    
    def open_url(self, url):
        """
        打开指定URL
        
        Args:
            url: 要打开的URL
        """
        try:
            self.driver.get(url)
            logger.info(f"已打开页面: {url}")
        except Exception as e:
            logger.error(f"打开页面失败: {e}")
            raise
    
    def get_current_url(self):
        """
        获取当前页面URL
        
        Returns:
            当前页面URL
        """
        return self.driver.current_url
    
    def get_page_title(self):
        """
        获取页面标题
        
        Returns:
            页面标题
        """
        return self.driver.title
    
    def find_element(self, locator, timeout=None):
        """
        查找单个元素
        
        Args:
            locator: 元素定位器 (By, value)
            timeout: 超时时间
            
        Returns:
            WebElement对象
        """
        return self.utils.wait_for_element(self.driver, locator, timeout)
    
    def find_elements(self, locator):
        """
        查找多个元素
        
        Args:
            locator: 元素定位器 (By, value)
            
        Returns:
            WebElement列表
        """
        try:
            elements = self.driver.find_elements(*locator)
            logger.debug(f"找到 {len(elements)} 个元素: {locator}")
            return elements
        except Exception as e:
            logger.error(f"查找元素失败: {e}")
            return []
    
    def click_element(self, locator, timeout=None):
        """
        点击元素
        
        Args:
            locator: 元素定位器 (By, value)
            timeout: 超时时间
        """
        try:
            element = self.utils.wait_for_element_clickable(self.driver, locator, timeout)
            element.click()
            logger.debug(f"已点击元素: {locator}")
        except Exception as e:
            logger.error(f"点击元素失败: {e}")
            raise
    
    def input_text(self, locator, text, clear_first=True, timeout=None):
        """
        输入文本
        
        Args:
            locator: 元素定位器 (By, value)
            text: 要输入的文本
            clear_first: 是否先清空输入框
            timeout: 超时时间
        """
        try:
            element = self.utils.wait_for_element(self.driver, locator, timeout)
            
            if clear_first:
                element.clear()
            
            element.send_keys(text)
            logger.debug(f"已输入文本 '{text}' 到元素: {locator}")
        except Exception as e:
            logger.error(f"输入文本失败: {e}")
            raise
    
    def get_element_text(self, locator, timeout=None):
        """
        获取元素文本
        
        Args:
            locator: 元素定位器 (By, value)
            timeout: 超时时间
            
        Returns:
            元素文本内容
        """
        try:
            element = self.utils.wait_for_element(self.driver, locator, timeout)
            text = element.text
            logger.debug(f"获取元素文本 '{text}': {locator}")
            return text
        except Exception as e:
            logger.error(f"获取元素文本失败: {e}")
            return ""
    
    def get_element_attribute(self, locator, attribute_name, timeout=None):
        """
        获取元素属性值
        
        Args:
            locator: 元素定位器 (By, value)
            attribute_name: 属性名称
            timeout: 超时时间
            
        Returns:
            属性值
        """
        try:
            element = self.utils.wait_for_element(self.driver, locator, timeout)
            value = element.get_attribute(attribute_name)
            logger.debug(f"获取元素属性 '{attribute_name}' 值 '{value}': {locator}")
            return value
        except Exception as e:
            logger.error(f"获取元素属性失败: {e}")
            return None
    
    def is_element_displayed(self, locator, timeout=None):
        """
        检查元素是否显示
        
        Args:
            locator: 元素定位器 (By, value)
            timeout: 超时时间
            
        Returns:
            bool
        """
        try:
            element = self.utils.wait_for_element(self.driver, locator, timeout)
            is_displayed = element.is_displayed()
            logger.debug(f"元素显示状态: {is_displayed}, {locator}")
            return is_displayed
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"元素不存在或不可见: {locator}")
            return False
    
    def is_element_enabled(self, locator, timeout=None):
        """
        检查元素是否可用
        
        Args:
            locator: 元素定位器 (By, value)
            timeout: 超时时间
            
        Returns:
            bool
        """
        try:
            element = self.utils.wait_for_element(self.driver, locator, timeout)
            is_enabled = element.is_enabled()
            logger.debug(f"元素可用状态: {is_enabled}, {locator}")
            return is_enabled
        except (TimeoutException, NoSuchElementException):
            logger.debug(f"元素不存在: {locator}")
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """
        等待元素消失
        
        Args:
            locator: 元素定位器 (By, value)
            timeout: 超时时间
            
        Returns:
            bool
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        
        try:
            self.wait.until_not(EC.presence_of_element_located(locator))
            logger.debug(f"元素已消失: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"等待元素消失超时: {locator}")
            return False
    
    def scroll_to_element(self, locator, timeout=None):
        """
        滚动到指定元素
        
        Args:
            locator: 元素定位器 (By, value)
            timeout: 超时时间
        """
        try:
            element = self.utils.wait_for_element(self.driver, locator, timeout)
            self.utils.scroll_to_element(self.driver, element)
        except Exception as e:
            logger.error(f"滚动到元素失败: {e}")
            raise
    
    def take_screenshot(self, filename=None):
        """
        截取页面截图
        
        Args:
            filename: 截图文件名
            
        Returns:
            截图文件路径
        """
        return self.utils.take_screenshot(self.driver, filename)
    
    def refresh_page(self):
        """刷新页面"""
        try:
            self.driver.refresh()
            logger.info("页面已刷新")
        except Exception as e:
            logger.error(f"刷新页面失败: {e}")
            raise
    
    def go_back(self):
        """返回上一页"""
        try:
            self.driver.back()
            logger.info("已返回上一页")
        except Exception as e:
            logger.error(f"返回上一页失败: {e}")
            raise
    
    def go_forward(self):
        """前进到下一页"""
        try:
            self.driver.forward()
            logger.info("已前进到下一页")
        except Exception as e:
            logger.error(f"前进失败: {e}")
            raise
    
    def switch_to_frame(self, frame_locator_or_index):
        """
        切换到iframe
        
        Args:
            frame_locator_or_index: iframe定位器或索引
        """
        try:
            if isinstance(frame_locator_or_index, tuple):
                # 如果是定位器，先找到元素
                frame_element = self.find_element(frame_locator_or_index)
                self.driver.switch_to.frame(frame_element)
            else:
                # 如果是索引或名称
                self.driver.switch_to.frame(frame_locator_or_index)
            
            logger.debug(f"已切换到iframe: {frame_locator_or_index}")
        except Exception as e:
            logger.error(f"切换iframe失败: {e}")
            raise
    
    def switch_to_default_content(self):
        """切换回主页面内容"""
        try:
            self.driver.switch_to.default_content()
            logger.debug("已切换回主页面内容")
        except Exception as e:
            logger.error(f"切换回主页面失败: {e}")
            raise 