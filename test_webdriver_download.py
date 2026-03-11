#!/usr/bin/env python3
"""
WebDriver下载测试脚本
用于解决网络问题并手动下载WebDriver
"""

import os
import sys
import subprocess
import logging
import requests
import zipfile
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('webdriver_download.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def check_network_connection():
    """检查网络连接"""
    logger.info("🔍 检查网络连接...")
    
    test_urls = [
        "https://www.baidu.com",
        "https://github.com", 
        "https://msedgedriver.azureedge.net"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                logger.info(f"✅ 网络连接正常: {url}")
                return True
        except Exception as e:
            logger.warning(f"⚠️ 无法连接到 {url}: {e}")
    
    logger.error("❌ 网络连接异常，请检查网络设置")
    return False


def get_edge_version():
    """获取Edge浏览器版本"""
    logger.info("🔍 检测Edge浏览器版本...")
    
    try:
        # 方法1: 通过注册表查询
        cmd = r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'version' in line.lower():
                    version = line.split()[-1]
                    logger.info(f"✅ 检测到Edge版本: {version}")
                    return version
        
        # 方法2: 通过命令行查询
        cmd = r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --version'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            version = result.stdout.strip().split()[-1]
            logger.info(f"✅ 检测到Edge版本: {version}")
            return version
            
        # 方法3: 查找Edge安装目录
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application",
            r"C:\Program Files\Microsoft\Edge\Application"
        ]
        
        for edge_path in edge_paths:
            if os.path.exists(edge_path):
                for item in os.listdir(edge_path):
                    if item.replace('.', '').replace('-', '').isdigit():
                        logger.info(f"✅ 从目录检测到Edge版本: {item}")
                        return item
                        
    except Exception as e:
        logger.error(f"❌ 获取Edge版本失败: {e}")
    
    logger.warning("⚠️ 无法检测Edge版本，将使用最新版本")
    return None


def download_edge_webdriver(version=None):
    """下载Edge WebDriver"""
    logger.info("📥 开始下载Edge WebDriver...")
    
    try:
        if not version:
            # 获取最新版本信息
            logger.info("获取最新WebDriver版本...")
            api_url = "https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/LATEST_RELEASE"
            response = requests.get(api_url, timeout=30)
            if response.status_code == 200:
                version = response.text.strip()
                logger.info(f"最新版本: {version}")
            else:
                # 如果无法获取最新版本，使用一个通用版本
                version = "119.0.2151.72"
                logger.warning(f"无法获取最新版本，使用默认版本: {version}")
        
        # 下载URL
        download_url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"
        logger.info(f"下载地址: {download_url}")
        
        # 创建drivers目录
        drivers_dir = Path("drivers")
        drivers_dir.mkdir(exist_ok=True)
        
        # 下载文件
        logger.info("正在下载WebDriver...")
        response = requests.get(download_url, timeout=120)
        
        if response.status_code == 200:
            zip_path = drivers_dir / "edgedriver.zip"
            
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"下载完成，大小: {len(response.content)} 字节")
            
            # 解压文件
            logger.info("正在解压WebDriver...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(drivers_dir)
            
            # 删除zip文件
            zip_path.unlink()
            
            # 检查解压结果
            driver_exe = drivers_dir / "msedgedriver.exe"
            if driver_exe.exists():
                logger.info(f"✅ WebDriver下载成功: {driver_exe.absolute()}")
                return str(driver_exe.absolute())
            else:
                logger.error("❌ 解压后未找到msedgedriver.exe")
                return None
        else:
            logger.error(f"❌ 下载失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"❌ 下载WebDriver异常: {e}")
        return None


def find_existing_webdriver():
    """查找已存在的WebDriver"""
    logger.info("🔍 查找已存在的WebDriver...")
    
    possible_paths = [
        # 项目目录
        "drivers/msedgedriver.exe",
        "msedgedriver.exe",
        # 系统常见路径
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedgedriver.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            abs_path = os.path.abspath(path)
            logger.info(f"✅ 找到现有WebDriver: {abs_path}")
            return abs_path
    
    # 检查PATH环境变量
    try:
        result = subprocess.run("where msedgedriver", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            path = result.stdout.strip().split('\n')[0]
            logger.info(f"✅ 在PATH中找到WebDriver: {path}")
            return path
    except:
        pass
    
    logger.warning("⚠️ 未找到现有的WebDriver")
    return None


def test_webdriver():
    """测试WebDriver是否可用"""
    logger.info("🧪 测试WebDriver...")
    
    try:
        # 先查找现有的WebDriver
        driver_path = find_existing_webdriver()
        
        if not driver_path:
            # 检查网络连接
            if check_network_connection():
                # 获取Edge版本并下载WebDriver
                edge_version = get_edge_version()
                driver_path = download_edge_webdriver(edge_version)
            else:
                logger.error("❌ 网络连接异常，无法下载WebDriver")
                return False
        
        if not driver_path:
            logger.error("❌ 无法获取WebDriver")
            return False
        
        # 测试WebDriver是否可用
        from selenium import webdriver
        from selenium.webdriver.edge.service import Service as EdgeService
        from selenium.webdriver.edge.options import Options as EdgeOptions
        
        options = EdgeOptions()
        options.add_argument("--headless")  # 无头模式测试
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = EdgeService(driver_path)
        
        logger.info("启动Edge WebDriver进行测试...")
        driver = webdriver.Edge(service=service, options=options)
        
        # 简单测试
        driver.get("https://www.baidu.com")
        title = driver.title
        logger.info(f"✅ WebDriver测试成功，页面标题: {title}")
        
        driver.quit()
        logger.info("✅ WebDriver测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ WebDriver测试失败: {e}")
        return False


def show_solutions():
    """显示解决方案"""
    print("=" * 80)
    print("🔧 WebDriver网络问题解决方案")
    print("=" * 80)
    print()
    print("如果自动下载失败，您可以尝试以下手动解决方案：")
    print()
    print("1️⃣ 手动下载WebDriver:")
    print("   - 访问: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
    print("   - 下载与您的Edge版本匹配的WebDriver")
    print("   - 解压后将msedgedriver.exe放到项目的drivers文件夹中")
    print()
    print("2️⃣ 使用离线安装包:")
    print("   - 从其他有网络的机器下载WebDriver")
    print("   - 通过U盘等方式传输到当前机器")
    print()
    print("3️⃣ 配置网络代理:")
    print("   - 如果使用公司网络，可能需要配置代理设置")
    print("   - 联系网络管理员获取代理配置信息")
    print()
    print("4️⃣ 使用系统自带的WebDriver:")
    print("   - 某些Edge版本会自带WebDriver")
    print("   - 将msedgedriver.exe添加到系统PATH环境变量中")
    print()
    print("=" * 80)


def main():
    """主函数"""
    print("🚀 WebDriver下载测试工具")
    print("=" * 50)
    
    try:
        # 测试WebDriver
        if test_webdriver():
            print("\n🎉 WebDriver配置成功！可以正常运行CRM测试了。")
        else:
            print("\n❌ WebDriver配置失败！")
            show_solutions()
            
    except KeyboardInterrupt:
        print("\n👋 用户中断测试")
    except Exception as e:
        logger.error(f"程序异常: {e}")
        print(f"\n❌ 程序异常: {e}")
        show_solutions()


if __name__ == "__main__":
    main() 