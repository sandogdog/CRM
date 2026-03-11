"""
WebDriver版本修复脚本
快速解决WebDriver版本不匹配问题
"""

import os
import sys
import requests
import zipfile
import subprocess
import tempfile

def get_edge_version():
    """获取Edge浏览器版本"""
    try:
        # 尝试通过注册表获取版本
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Edge\BLBeacon")
        version = winreg.QueryValueEx(key, "version")[0]
        winreg.CloseKey(key)
        print(f"✅ 检测到Edge浏览器版本: {version}")
        return version
    except Exception as e:
        print(f"⚠️ 无法从注册表获取Edge版本: {e}")
        
    # 备用方法：通过命令行获取
    try:
        result = subprocess.run([
            'powershell', '-Command', 
            '(Get-Item "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe").VersionInfo.ProductVersion'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ 通过PowerShell检测到Edge版本: {version}")
            return version
    except Exception as e:
        print(f"⚠️ 无法通过PowerShell获取Edge版本: {e}")
    
    return None

def download_webdriver(version, drivers_folder="drivers"):
    """下载指定版本的WebDriver"""
    if not os.path.exists(drivers_folder):
        os.makedirs(drivers_folder)
        print(f"📁 创建文件夹: {drivers_folder}")
    
    # 构建下载URL
    url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"
    print(f"🔄 正在下载WebDriver版本 {version}")
    print(f"📍 下载地址: {url}")
    
    try:
        # 下载文件
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_path = temp_file.name
        
        print(f"✅ 下载完成，正在解压...")
        
        # 解压文件
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            zip_ref.extractall(drivers_folder)
        
        # 清理临时文件
        os.unlink(temp_path)
        
        # 检查解压结果
        driver_path = os.path.join(drivers_folder, "msedgedriver.exe")
        if os.path.exists(driver_path):
            print(f"✅ WebDriver成功安装到: {driver_path}")
            return driver_path
        else:
            print(f"❌ 解压后未找到msedgedriver.exe")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return None
    except Exception as e:
        print(f"❌ 下载过程出错: {e}")
        return None

def clean_old_drivers(drivers_folder="drivers"):
    """清理旧版本的WebDriver"""
    if os.path.exists(drivers_folder):
        for file in os.listdir(drivers_folder):
            if file.endswith('.exe'):
                old_path = os.path.join(drivers_folder, file)
                try:
                    os.remove(old_path)
                    print(f"🧹 清理旧驱动: {file}")
                except Exception as e:
                    print(f"⚠️ 无法删除 {file}: {e}")

def main():
    print("🚀 WebDriver版本修复工具")
    print("=" * 50)
    
    # 1. 获取Edge浏览器版本
    edge_version = get_edge_version()
    if not edge_version:
        print("❌ 无法检测Edge浏览器版本")
        print("💡 请手动下载WebDriver:")
        print("   1. 访问: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
        print("   2. 下载对应版本的WebDriver")
        print("   3. 解压到项目的drivers文件夹中")
        return False
    
    # 2. 清理旧驱动
    print("\n🧹 清理旧版本驱动...")
    clean_old_drivers()
    
    # 3. 下载新驱动
    print(f"\n📥 下载匹配版本的WebDriver...")
    driver_path = download_webdriver(edge_version)
    
    if driver_path:
        print(f"\n✅ WebDriver修复成功！")
        print(f"📍 驱动位置: {driver_path}")
        print(f"🎉 现在可以重新运行测试了")
        return True
    else:
        print(f"\n❌ 自动修复失败")
        print(f"💡 手动解决方案:")
        print(f"   1. 打开浏览器访问: https://msedgedriver.azureedge.net/{edge_version}/edgedriver_win64.zip")
        print(f"   2. 下载并解压到 drivers/ 文件夹")
        print(f"   3. 确保文件名为 msedgedriver.exe")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 修复完成，按任意键退出...")
        else:
            print("\n⚠️ 需要手动处理，按任意键退出...")
        input()
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"\n💥 程序异常: {e}")
        input("按任意键退出...")
