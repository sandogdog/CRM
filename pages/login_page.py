"""
登录页面对象类
实现登录页面的所有业务操作
"""
import logging
from pages.base_page import BasePage
from config.locators import LoginPageLocators
from config.config import Config

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """登录页面类"""
    
    def __init__(self, driver):
        """
        初始化登录页面
        
        Args:
            driver: WebDriver实例
        """
        super().__init__(driver)
        self.url = Config.get_base_url()
    
    def open(self):
        """打开登录页面"""
        self.open_url(self.url)
        logger.info("已打开登录页面")
        
        # 点击用户名密码登录按钮（如果存在）
        self.switch_to_username_password_login()
    
    def switch_to_username_password_login(self):
        """切换到用户名密码登录模式"""
        try:
            # 检查是否存在用户名密码登录按钮
            if self.is_element_displayed(LoginPageLocators.USERNAME_PASSWORD_LOGIN_BUTTON, timeout=3):
                logger.info("发现用户名密码登录按钮，正在点击...")
                self.click_element(LoginPageLocators.USERNAME_PASSWORD_LOGIN_BUTTON)
                logger.info("已切换到用户名密码登录模式")
                
                # 等待页面元素加载
                import time
                time.sleep(1)
            else:
                logger.info("未发现用户名密码登录按钮，可能已在用户名密码登录模式")
        except Exception as e:
            logger.warning(f"切换到用户名密码登录模式时出现异常: {e}")
    
    def enter_username(self, username):
        """
        输入用户名
        
        Args:
            username: 用户名
        """
        self.input_text(LoginPageLocators.USERNAME_INPUT, username)
        logger.info(f"已输入用户名: {username}")
    
    def enter_password(self, password):
        """
        输入密码
        
        Args:
            password: 密码
        """
        self.input_text(LoginPageLocators.PASSWORD_INPUT, password)
        logger.info("已输入密码")
    
    def enter_captcha(self, captcha):
        """
        输入验证码
        
        Args:
            captcha: 验证码
        """
        if self.is_element_displayed(LoginPageLocators.CAPTCHA_INPUT):
            self.input_text(LoginPageLocators.CAPTCHA_INPUT, captcha)
            logger.info(f"已输入验证码: {captcha}")
        else:
            logger.info("验证码输入框不存在，跳过验证码输入")
    
    def click_login_button(self):
        """点击登录按钮"""
        self.click_element(LoginPageLocators.LOGIN_BUTTON)
        logger.info("已点击登录按钮")
    
    def click_forget_password_link(self):
        """点击忘记密码链接"""
        self.click_element(LoginPageLocators.FORGET_PASSWORD_LINK)
        logger.info("已点击忘记密码链接")
    
    def refresh_captcha(self):
        """刷新验证码"""
        if self.is_element_displayed(LoginPageLocators.REFRESH_CAPTCHA):
            self.click_element(LoginPageLocators.REFRESH_CAPTCHA)
            logger.info("已刷新验证码")
        else:
            logger.info("验证码刷新按钮不存在")
    
    def get_error_message(self):
        """
        获取错误提示信息
        
        Returns:
            错误提示文本
        """
        if self.is_element_displayed(LoginPageLocators.ERROR_MESSAGE, timeout=5):
            error_text = self.get_element_text(LoginPageLocators.ERROR_MESSAGE)
            logger.info(f"获取到错误信息: {error_text}")
            return error_text
        else:
            logger.info("没有发现错误信息")
            return ""
    
    def is_login_button_enabled(self):
        """
        检查登录按钮是否可用
        
        Returns:
            bool
        """
        return self.is_element_enabled(LoginPageLocators.LOGIN_BUTTON)
    
    def is_captcha_required(self):
        """
        检查是否需要验证码
        
        Returns:
            bool
        """
        return self.is_element_displayed(LoginPageLocators.CAPTCHA_INPUT, timeout=2)
    
    def login(self, username, password, captcha=None):
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
            captcha: 验证码（可选）
            
        Returns:
            bool: 登录是否成功
        """
        try:
            logger.info(f"开始登录，用户名: {username}")
            
            # 输入用户名
            self.enter_username(username)
            
            # 输入密码
            self.enter_password(password)
            
            # 如果需要验证码，输入验证码
            if self.is_captcha_required() and captcha:
                self.enter_captcha(captcha)
            
            # 点击登录按钮
            self.click_login_button()
            
            # 等待页面跳转或错误信息出现
            import time
            time.sleep(2)
            
            # 检查是否有错误信息
            error_message = self.get_error_message()
            if error_message:
                logger.error(f"登录失败: {error_message}")
                return False
            
            # 检查是否成功跳转（URL变化）
            current_url = self.get_current_url()
            if "test-admin-crm.cd.xiaoxigroup.net" in current_url or "sso.xiaoxitech.com" not in current_url:
                logger.info("登录成功，页面已跳转")
                return True
            else:
                logger.error("登录失败，仍在登录页面")
                return False
                
        except Exception as e:
            logger.error(f"登录过程中发生异常: {e}")
            return False
    
    def login_with_admin_user(self):
        """
        使用管理员账户登录
        
        Returns:
            bool: 登录是否成功
        """
        admin_user = Config.get_test_user("admin")
        return self.login(admin_user["username"], admin_user["password"])
    
    def login_with_regular_user(self):
        """
        使用普通用户账户登录
        
        Returns:
            bool: 登录是否成功
        """
        regular_user = Config.get_test_user("user")
        return self.login(regular_user["username"], regular_user["password"])
    
    def clear_login_form(self):
        """清空登录表单"""
        try:
            # 清空用户名
            username_element = self.find_element(LoginPageLocators.USERNAME_INPUT)
            username_element.clear()
            
            # 清空密码
            password_element = self.find_element(LoginPageLocators.PASSWORD_INPUT)
            password_element.clear()
            
            # 清空验证码（如果存在）
            if self.is_captcha_required():
                captcha_element = self.find_element(LoginPageLocators.CAPTCHA_INPUT)
                captcha_element.clear()
            
            logger.info("已清空登录表单")
            
        except Exception as e:
            logger.error(f"清空登录表单失败: {e}")
    
    def get_username_placeholder(self):
        """
        获取用户名输入框的占位符文本
        
        Returns:
            占位符文本
        """
        return self.get_element_attribute(LoginPageLocators.USERNAME_INPUT, "placeholder")
    
    def get_password_placeholder(self):
        """
        获取密码输入框的占位符文本
        
        Returns:
            占位符文本
        """
        return self.get_element_attribute(LoginPageLocators.PASSWORD_INPUT, "placeholder")
    
    def wait_for_page_load(self, timeout=10):
        """
        等待登录页面加载完成
        
        Args:
            timeout: 超时时间
            
        Returns:
            bool: 页面是否加载完成
        """
        try:
            # 等待关键元素出现
            self.utils.wait_for_element(self.driver, LoginPageLocators.USERNAME_INPUT, timeout)
            self.utils.wait_for_element(self.driver, LoginPageLocators.PASSWORD_INPUT, timeout)
            self.utils.wait_for_element(self.driver, LoginPageLocators.LOGIN_BUTTON, timeout)
            
            logger.info("登录页面加载完成")
            return True
            
        except Exception as e:
            logger.error(f"等待登录页面加载超时: {e}")
            return False 