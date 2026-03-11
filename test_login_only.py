"""
单独测试登录功能 - 验证验证码处理逻辑
"""

import logging
import time
from utils.driver_manager import DriverManager
from crm_login import login_to_crm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_login_with_captcha():
    """测试带验证码的登录流程"""
    driver = None
    try:
        logger.info("🧪 开始测试登录功能（支持验证码）")
        logger.info("=" * 50)
        
        # 初始化WebDriver
        logger.info("🚀 初始化浏览器...")
        driver_manager = DriverManager()
        driver = driver_manager.get_driver()
        
        # 测试登录
        logger.info("🔑 开始登录测试...")
        success = login_to_crm(driver)
        
        if success:
            logger.info("✅ 登录测试成功！")
            logger.info("🌟 当前页面URL: " + driver.current_url)
            logger.info("📄 页面标题: " + driver.title)
        else:
            logger.error("❌ 登录测试失败！")
            return False
            
        # 保持浏览器打开一会儿，让用户查看结果
        logger.info("⏳ 浏览器将在10秒后关闭...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        logger.error(f"测试过程异常: {e}")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("🚪 浏览器已关闭")
            except Exception as e:
                logger.warning(f"⚠️ 关闭浏览器时出现异常: {e}")

def main():
    """主函数"""
    try:
        print("🔑 CRM登录功能测试")
        print("=" * 40)
        print("📋 测试内容：")
        print("   ✅ WebDriver初始化")
        print("   ✅ 自动填入用户名密码")
        print("   ✅ 验证码检测与处理")
        print("   ✅ 登录状态验证")
        print("=" * 40)
        print("💡 如果有验证码，脚本会提示你在10秒内手动输入")
        print("💡 脚本会自动检测登录是否成功")
        print("=" * 40)
        print("🚀 开始测试...")
        
        success = test_login_with_captcha()
        
        if success:
            print("\n🎉 登录功能测试完成！")
        else:
            print("\n❌ 登录功能测试失败！")
            
    except KeyboardInterrupt:
        print("\n👋 用户中断测试")
    except Exception as e:
        print(f"\n💥 程序异常: {e}")

if __name__ == "__main__":
    main()
