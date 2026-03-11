"""
智能WebDriver下载脚本
支持多种下载源和网络检测
"""

import os
import sys
import requests
import zipfile
import tempfile
import subprocess
from urllib.parse import urlparse
import time

class WebDriverDownloader:
    def __init__(self):
        self.drivers_folder = "drivers"
        self.edge_version = None
        
    def get_edge_version(self):
        """获取Edge浏览器版本"""
        try:
            # 方法1：通过注册表获取版本
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Edge\BLBeacon")
            version = winreg.QueryValueEx(key, "version")[0]
            winreg.CloseKey(key)
            print(f"✅ 检测到Edge浏览器版本: {version}")
            return version
        except Exception as e:
            print(f"⚠️ 无法从注册表获取Edge版本: {e}")
            
        # 方法2：通过PowerShell获取
        try:
            result = subprocess.run([
                'powershell', '-Command', 
                '(Get-Item "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe").VersionInfo.ProductVersion'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ 通过PowerShell检测到Edge版本: {version}")
                return version
        except Exception as e:
            print(f"⚠️ 无法通过PowerShell获取Edge版本: {e}")
        
        return None
    
    def test_network_connectivity(self):
        """测试网络连接"""
        test_urls = [
            "https://www.google.com",
            "https://www.baidu.com",
            "https://developer.microsoft.com"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ 网络连接正常 ({urlparse(url).netloc})")
                    return True
            except Exception:
                continue
        
        print("❌ 网络连接异常")
        return False
    
    def download_webdriver(self, version):
        """下载WebDriver，支持多个下载源"""
        if not os.path.exists(self.drivers_folder):
            os.makedirs(self.drivers_folder)
            print(f"📁 创建文件夹: {self.drivers_folder}")
        
        # 多个下载源
        download_urls = [
            f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip",
            f"https://msedgewebdriver.azureedge.net/stable/{version}/edgedriver_win64.zip",
        ]
        
        # 如果是主版本号，尝试获取最新的稳定版本
        major_version = version.split('.')[0]
        download_urls.append(f"https://msedgedriver.azureedge.net/LATEST_STABLE_{major_version}/edgedriver_win64.zip")
        
        for i, url in enumerate(download_urls, 1):
            print(f"🔄 尝试下载源 {i}/{len(download_urls)}: {url}")
            
            try:
                response = requests.get(url, timeout=60, stream=True)
                response.raise_for_status()
                
                # 保存到临时文件
                with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    
                    for chunk in response.iter_content(chunk_size=8192):
                        temp_file.write(chunk)
                        downloaded += len(chunk)
                        
                        # 显示下载进度
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r📥 下载进度: {progress:.1f}%", end="")
                    
                    temp_path = temp_file.name
                    print(f"\n✅ 下载完成，正在解压...")
                
                # 解压文件
                with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                    zip_ref.extractall(self.drivers_folder)
                
                # 清理临时文件
                os.unlink(temp_path)
                
                # 检查解压结果
                driver_path = os.path.join(self.drivers_folder, "msedgedriver.exe")
                if os.path.exists(driver_path):
                    print(f"✅ WebDriver成功安装到: {driver_path}")
                    return driver_path
                else:
                    print(f"❌ 解压后未找到msedgedriver.exe")
                    continue
                    
            except requests.exceptions.RequestException as e:
                print(f"\n❌ 下载源 {i} 失败: {e}")
                continue
            except Exception as e:
                print(f"\n❌ 处理下载源 {i} 时出错: {e}")
                continue
        
        return None
    
    def clean_old_drivers(self):
        """清理旧版本的WebDriver"""
        if os.path.exists(self.drivers_folder):
            for file in os.listdir(self.drivers_folder):
                if file.endswith('.exe'):
                    old_path = os.path.join(self.drivers_folder, file)
                    try:
                        os.remove(old_path)
                        print(f"🧹 清理旧驱动: {file}")
                    except Exception as e:
                        print(f"⚠️ 无法删除 {file}: {e}")
    
    def run(self):
        """执行下载流程"""
        print("🚀 智能WebDriver下载工具")
        print("=" * 50)
        
        # 1. 检测Edge版本
        self.edge_version = self.get_edge_version()
        if not self.edge_version:
            print("❌ 无法检测Edge浏览器版本")
            return False
        
        # 2. 检测网络连接
        if not self.test_network_connectivity():
            print("💡 网络连接异常，请检查网络设置")
            print("💡 或者手动下载WebDriver:")
            print(f"   https://msedgedriver.azureedge.net/{self.edge_version}/edgedriver_win64.zip")
            return False
        
        # 3. 清理旧驱动
        print("\n🧹 清理旧版本驱动...")
        self.clean_old_drivers()
        
        # 4. 下载新驱动
        print(f"\n📥 下载匹配版本的WebDriver...")
        driver_path = self.download_webdriver(self.edge_version)
        
        if driver_path:
            print(f"\n🎉 WebDriver修复成功！")
            print(f"📍 驱动位置: {driver_path}")
            print(f"✅ 现在可以重新运行测试了")
            return True
        else:
            print(f"\n❌ 自动修复失败")
            print(f"💡 手动解决方案:")
            print(f"   1. 访问: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
            print(f"   2. 下载版本 {self.edge_version} 的WebDriver")
            print(f"   3. 解压到 {self.drivers_folder}/ 文件夹")
            print(f"   4. 确保文件名为 msedgedriver.exe")
            return False

def main():
    try:
        downloader = WebDriverDownloader()
        success = downloader.run()
        
        print("\n" + "=" * 50)
        if success:
            print("🎯 修复完成！可以重新运行 python main.py")
        else:
            print("⚠️ 需要手动处理")
        
        input("按回车键退出...")
        
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"\n💥 程序异常: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
