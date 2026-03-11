"""
改进的WebDriver管理帮助类
解决版本不匹配和网络连接问题
"""

import os
import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import zipfile
import tempfile
import subprocess

logger = logging.getLogger(__name__)

class ImprovedWebDriverManager:
    """改进的WebDriver管理器"""
    
    def __init__(self, drivers_folder="drivers"):
        self.drivers_folder = drivers_folder
        self.ensure_drivers_folder()
    
    def ensure_drivers_folder(self):
        """确保drivers文件夹存在"""
        if not os.path.exists(self.drivers_folder):
            os.makedirs(self.drivers_folder)
            logger.info(f"📁 创建drivers文件夹: {self.drivers_folder}")
    
    def get_edge_version(self):
        """获取当前Edge浏览器版本"""
        try:
            # Windows系统获取Edge版本
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Edge\BLBeacon")
            version = winreg.QueryValueEx(key, "version")[0]
            winreg.CloseKey(key)
            logger.info(f"🌐 检测到Edge浏览器版本: {version}")
            return version
        except Exception as e:
            logger.warning(f"⚠️ 无法检测Edge版本: {e}")
            return None
    
    def download_webdriver_manually(self, version):
        """手动下载指定版本的WebDriver"""
        try:
            url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"
            logger.info(f"🔄 尝试从官方源下载WebDriver版本 {version}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            # 解压到drivers文件夹
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                zip_ref.extractall(self.drivers_folder)
            
            os.unlink(temp_path)
            
            driver_path = os.path.join(self.drivers_folder, "msedgedriver.exe")
            if os.path.exists(driver_path):
                logger.info(f"✅ 成功下载WebDriver到: {driver_path}")
                return driver_path
            
        except Exception as e:
            logger.error(f"❌ 手动下载WebDriver失败: {e}")
        
        return None
    
    def get_webdriver_with_retry(self, max_retries=3):
        """带重试机制的WebDriver获取"""
        edge_version = self.get_edge_version()
        
        # 方法1: 尝试使用webdriver_manager
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 尝试使用webdriver_manager (第{attempt+1}次)")
                driver_path = EdgeChromiumDriverManager().install()
                return self.create_webdriver(driver_path)
            except Exception as e:
                logger.warning(f"⚠️ webdriver_manager失败 (第{attempt+1}次): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
        
        # 方法2: 手动下载匹配版本
        if edge_version:
            logger.info("🔄 尝试手动下载匹配版本的WebDriver")
            driver_path = self.download_webdriver_manually(edge_version)
            if driver_path:
                return self.create_webdriver(driver_path)
        
        # 方法3: 使用本地drivers文件夹中的驱动
        local_driver = os.path.join(self.drivers_folder, "msedgedriver.exe")
        if os.path.exists(local_driver):
            logger.info(f"🔄 尝试使用本地WebDriver: {local_driver}")
            return self.create_webdriver(local_driver)
        
        # 方法4: 使用系统PATH中的驱动（降级方案）
        try:
            logger.info("🔄 尝试使用系统PATH中的WebDriver")
            return self.create_webdriver()
        except Exception as e:
            logger.error(f"❌ 系统PATH中的WebDriver也失败: {e}")
        
        raise Exception("❌ 所有WebDriver获取方法都失败了")
    
    def create_webdriver(self, driver_path=None):
        """创建WebDriver实例"""
        options = EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=0")
        
        # 忽略证书错误
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--ignore-certificate-errors-spki")
        
        if driver_path and os.path.exists(driver_path):
            service = EdgeService(driver_path)
            driver = webdriver.Edge(service=service, options=options)
        else:
            driver = webdriver.Edge(options=options)
        
        logger.info("✅ WebDriver创建成功")
        return driver

def get_improved_webdriver():
    """获取改进的WebDriver实例"""
    manager = ImprovedWebDriverManager()
    return manager.get_webdriver_with_retry()

# 使用示例
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        driver = get_improved_webdriver()
        print("✅ WebDriver测试成功")
        driver.quit()
    except Exception as e:
        print(f"❌ WebDriver测试失败: {e}")
