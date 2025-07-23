"""
WebDriver管理器
负责浏览器驱动的初始化、配置和清理
"""
import logging
import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# 尝试导入webdriver_manager，如果网络问题则使用离线模式
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from webdriver_manager.core.utils import ChromeType
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

from config.config import Config


logger = logging.getLogger(__name__)


class DriverManager:
    """WebDriver管理器类"""
    
    _instance = None
    _driver = None
    
    def __new__(cls):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(DriverManager, cls).__new__(cls)
        return cls._instance
    
    def get_driver(self, browser=None, headless=None):
        """
        获取WebDriver实例
        
        Args:
            browser: 浏览器类型 (chrome, firefox, edge)
            headless: 是否无头模式
            
        Returns:
            WebDriver实例
        """
        if self._driver:
            return self._driver
            
        browser = browser or Config.BROWSER
        headless = headless if headless is not None else Config.HEADLESS
        
        try:
            if browser.lower() == "chrome":
                self._driver = self._get_chrome_driver(headless)
            elif browser.lower() == "firefox":
                self._driver = self._get_firefox_driver(headless)
            elif browser.lower() == "edge":
                self._driver = self._get_edge_driver(headless)
            else:
                raise ValueError(f"不支持的浏览器类型: {browser}")
            
            # 设置浏览器配置
            self._configure_driver()
            
            logger.info(f"WebDriver 初始化成功: {browser}")
            return self._driver
            
        except Exception as e:
            logger.error(f"WebDriver 初始化失败: {e}")
            raise
    
    def _find_cached_edge_driver(self):
        """查找缓存的Edge WebDriver"""
        try:
            # webdriver_manager默认缓存路径
            cache_path = os.path.expanduser("~/.wdm/drivers/edgedriver/win64")
            
            if not os.path.exists(cache_path):
                logger.warning("WebDriver缓存目录不存在")
                return None
            
            # 查找所有版本目录
            version_dirs = [d for d in os.listdir(cache_path) if os.path.isdir(os.path.join(cache_path, d))]
            
            if not version_dirs:
                logger.warning("未找到缓存的WebDriver版本")
                return None
            
            # 获取最新版本（按版本号排序）
            latest_version = sorted(version_dirs, key=lambda x: [int(i) for i in x.split('.')], reverse=True)[0]
            driver_dir = os.path.join(cache_path, latest_version)
            
            # 查找msedgedriver.exe
            driver_path = os.path.join(driver_dir, "msedgedriver.exe")
            if os.path.exists(driver_path):
                logger.info(f"✅ 找到缓存的Edge WebDriver: {driver_path} (版本: {latest_version})")
                return driver_path
            
            # 如果没有找到，尝试查找任何.exe文件
            exe_files = glob.glob(os.path.join(driver_dir, "*.exe"))
            if exe_files:
                driver_path = exe_files[0]
                logger.info(f"✅ 找到缓存的WebDriver: {driver_path} (版本: {latest_version})")
                return driver_path
                
        except Exception as e:
            logger.warning(f"查找缓存WebDriver时出错: {e}")
        
        return None
    
    def _get_chrome_driver(self, headless):
        """获取Chrome驱动"""
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        # Chrome选项配置
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
        
        # 禁用日志
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 设置用户代理
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        if WEBDRIVER_MANAGER_AVAILABLE:
            try:
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
            except Exception as e:
                logger.warning(f"使用webdriver_manager失败: {e}")
        
        # 尝试使用系统PATH中的chromedriver
        return webdriver.Chrome(options=options)
    
    def _get_firefox_driver(self, headless):
        """获取Firefox驱动"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        # Firefox选项配置
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("media.volume_scale", "0.0")
        
        if WEBDRIVER_MANAGER_AVAILABLE:
            try:
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=options)
            except Exception as e:
                logger.warning(f"使用webdriver_manager失败: {e}")
        
        # 尝试使用系统PATH中的geckodriver
        return webdriver.Firefox(options=options)
    
    def _get_edge_driver(self, headless):
        """获取Edge驱动"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        # Edge选项配置
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
        
        # 方法1: 先尝试使用缓存的WebDriver
        cached_driver = self._find_cached_edge_driver()
        if cached_driver:
            try:
                service = EdgeService(cached_driver)
                return webdriver.Edge(service=service, options=options)
            except Exception as e:
                logger.warning(f"使用缓存WebDriver失败: {e}")
        
        # 方法2: 尝试使用webdriver_manager（可能会联网）
        if WEBDRIVER_MANAGER_AVAILABLE:
            try:
                logger.info("尝试使用webdriver_manager获取WebDriver...")
                service = EdgeService(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=service, options=options)
            except Exception as e:
                logger.warning(f"webdriver_manager失败 (可能是网络问题): {e}")
        
        # 方法3: 尝试使用系统PATH中的msedgedriver
        try:
            logger.info("尝试使用系统PATH中的WebDriver...")
            return webdriver.Edge(options=options)
        except Exception as e:
            logger.error("所有WebDriver获取方法都失败了")
            logger.error("解决方案:")
            logger.error("1. 检查网络连接")
            logger.error("2. 手动下载WebDriver并放在项目drivers文件夹中")
            logger.error("3. 将WebDriver添加到系统PATH环境变量")
            raise Exception(f"无法获取Edge WebDriver: {e}")
    
    def _configure_driver(self):
        """配置WebDriver"""
        if not self._driver:
            return
        
        # 设置超时时间
        self._driver.implicitly_wait(Config.IMPLICIT_WAIT)
        self._driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        # 最大化窗口
        if not Config.HEADLESS:
            self._driver.maximize_window()
    
    def quit_driver(self):
        """退出WebDriver"""
        if self._driver:
            try:
                self._driver.quit()
                logger.info("WebDriver 已退出")
            except Exception as e:
                logger.error(f"WebDriver 退出失败: {e}")
            finally:
                self._driver = None
    
    def restart_driver(self):
        """重启WebDriver"""
        self.quit_driver()
        return self.get_driver()
    
    @property
    def driver(self):
        """获取驱动实例"""
        return self._driver 