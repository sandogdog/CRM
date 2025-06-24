"""
登录功能测试用例
包含正常登录、异常登录、界面元素验证等测试场景
"""
import pytest
import logging
import time

from pages.login_page import LoginPage
from config.config import Config


logger = logging.getLogger(__name__)


class TestLogin:
    """登录功能测试类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        logger.info("设置测试环境")
    
    def teardown_method(self):
        """每个测试方法执行后的清理"""
        logger.info("清理测试环境")
    
    @pytest.mark.smoke
    def test_successful_login_with_admin(self, driver):
        """
        测试管理员账户成功登录
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        
        # 等待页面加载
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 使用管理员账户登录
        admin_user = Config.get_test_user("admin")
        result = login_page.login(admin_user["username"], admin_user["password"])
        
        # 验证登录成功
        assert result, "管理员登录失败"
        
        # 验证页面跳转
        current_url = login_page.get_current_url()
        assert "test-admin-crm.cd.xiaoxigroup.net" in current_url or "sso.xiaoxitech.com" not in current_url, "登录后未正确跳转"
        
        logger.info("管理员登录测试通过")
    
    @pytest.mark.smoke
    def test_successful_login_with_regular_user(self, driver):
        """
        测试普通用户成功登录
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        
        # 等待页面加载
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 使用普通用户账户登录
        regular_user = Config.get_test_user("user")
        result = login_page.login(regular_user["username"], regular_user["password"])
        
        # 验证登录成功
        assert result, "普通用户登录失败"
        
        # 验证页面跳转
        current_url = login_page.get_current_url()
        assert "test-admin-crm.cd.xiaoxigroup.net" in current_url or "sso.xiaoxitech.com" not in current_url, "登录后未正确跳转"
        
        logger.info("普通用户登录测试通过")
    
    @pytest.mark.regression
    def test_login_with_invalid_username(self, driver):
        """
        测试无效用户名登录
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 使用无效用户名登录
        result = login_page.login("invalid_user@test.com", "password123")
        
        # 验证登录失败
        assert not result, "无效用户名应该登录失败"
        
        # 验证错误信息
        error_message = login_page.get_error_message()
        assert error_message, "应该显示错误信息"
        
        logger.info("无效用户名登录测试通过")
    
    @pytest.mark.regression
    def test_login_with_invalid_password(self, driver):
        """
        测试无效密码登录
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 使用正确用户名但错误密码登录
        admin_user = Config.get_test_user("admin")
        result = login_page.login(admin_user["username"], "wrong_password")
        
        # 验证登录失败
        assert not result, "错误密码应该登录失败"
        
        # 验证错误信息
        error_message = login_page.get_error_message()
        assert error_message, "应该显示错误信息"
        
        logger.info("无效密码登录测试通过")
    
    @pytest.mark.regression
    def test_login_with_empty_username(self, driver):
        """
        测试空用户名登录
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 使用空用户名登录
        result = login_page.login("", "password123")
        
        # 验证登录失败
        assert not result, "空用户名应该登录失败"
        
        logger.info("空用户名登录测试通过")
    
    @pytest.mark.regression
    def test_login_with_empty_password(self, driver):
        """
        测试空密码登录
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 使用空密码登录
        admin_user = Config.get_test_user("admin")
        result = login_page.login(admin_user["username"], "")
        
        # 验证登录失败
        assert not result, "空密码应该登录失败"
        
        logger.info("空密码登录测试通过")
    
    @pytest.mark.regression
    def test_login_with_both_empty_fields(self, driver):
        """
        测试用户名和密码都为空的登录
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 使用空用户名和密码登录
        result = login_page.login("", "")
        
        # 验证登录失败
        assert not result, "空用户名和密码应该登录失败"
        
        logger.info("空字段登录测试通过")
    
    def test_login_page_elements_visibility(self, driver):
        """
        测试登录页面元素可见性
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 验证页面标题
        page_title = login_page.get_page_title()
        assert page_title, "页面标题不能为空"
        
        # 验证关键元素可见性
        from config.locators import LoginPageLocators
        
        assert login_page.is_element_displayed(LoginPageLocators.USERNAME_INPUT), "用户名输入框不可见"
        assert login_page.is_element_displayed(LoginPageLocators.PASSWORD_INPUT), "密码输入框不可见"
        assert login_page.is_element_displayed(LoginPageLocators.LOGIN_BUTTON), "登录按钮不可见"
        
        logger.info("登录页面元素可见性测试通过")
    
    def test_login_button_status(self, driver):
        """
        测试登录按钮状态
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 验证登录按钮是否可用
        assert login_page.is_login_button_enabled(), "登录按钮应该是可用的"
        
        logger.info("登录按钮状态测试通过")
    
    def test_clear_login_form(self, driver):
        """
        测试清空登录表单功能
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 输入测试数据
        test_username = "test_user"
        test_password = "test_password"
        
        login_page.enter_username(test_username)
        login_page.enter_password(test_password)
        
        # 验证数据已输入
        from config.locators import LoginPageLocators
        username_value = login_page.get_element_attribute(LoginPageLocators.USERNAME_INPUT, "value")
        password_value = login_page.get_element_attribute(LoginPageLocators.PASSWORD_INPUT, "value")
        
        assert username_value == test_username, "用户名输入失败"
        assert password_value == test_password, "密码输入失败"
        
        # 清空表单
        login_page.clear_login_form()
        
        # 验证表单已清空
        username_value_after = login_page.get_element_attribute(LoginPageLocators.USERNAME_INPUT, "value")
        password_value_after = login_page.get_element_attribute(LoginPageLocators.PASSWORD_INPUT, "value")
        
        assert username_value_after == "", "用户名字段未清空"
        assert password_value_after == "", "密码字段未清空"
        
        logger.info("清空登录表单测试通过")
    
    @pytest.mark.parametrize("username,password,expected_result", [
        ("qinrenchi", "Sandog031220@", True),  # 正确的管理员账户
        ("qinrenchi", "Sandog031220@", True),    # 正确的普通用户账户
        ("wrong_user", "Sandog031220@", False), # 错误的用户名
        ("qinrenchi", "wrong_password", False),    # 错误的密码
        ("", "Sandog031220@", False),              # 空用户名
        ("qinrenchi", "", False),         # 空密码
        ("", "", False),                      # 空用户名和密码
    ])
    def test_login_scenarios(self, driver, username, password, expected_result):
        """
        参数化测试：多种登录场景
        
        Args:
            driver: WebDriver实例
            username: 测试用户名
            password: 测试密码
            expected_result: 预期结果
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 执行登录
        actual_result = login_page.login(username, password)
        
        # 验证结果
        assert actual_result == expected_result, f"登录结果不符合预期，用户名: {username}"
        
        # 如果测试失败，清空表单以便下次测试
        if not actual_result:
            login_page.clear_login_form()
        
        logger.info(f"参数化登录测试通过 - 用户名: {username}, 结果: {actual_result}")
    
    def test_forgot_password_link(self, driver):
        """
        测试忘记密码链接（如果存在）
        
        Args:
            driver: WebDriver实例
        """
        login_page = LoginPage(driver)
        
        # 打开登录页面
        login_page.open()
        assert login_page.wait_for_page_load(), "登录页面加载失败"
        
        # 检查忘记密码链接是否存在
        from config.locators import LoginPageLocators
        if login_page.is_element_displayed(LoginPageLocators.FORGET_PASSWORD_LINK, timeout=2):
            # 点击忘记密码链接
            current_url_before = login_page.get_current_url()
            login_page.click_forget_password_link()
            
            # 等待页面变化
            time.sleep(2)
            current_url_after = login_page.get_current_url()
            
            # 验证页面已跳转
            assert current_url_before != current_url_after, "点击忘记密码链接后页面未跳转"
            
            logger.info("忘记密码链接测试通过")
        else:
            logger.info("忘记密码链接不存在，跳过测试") 