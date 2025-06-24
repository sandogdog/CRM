"""
页面元素定位器配置文件
使用页面对象模式管理所有页面元素的定位器
"""
from selenium.webdriver.common.by import By


class LoginPageLocators:
    """登录页面元素定位器"""
    
    # 登录方式切换按钮
    USERNAME_PASSWORD_LOGIN_BUTTON = (By.XPATH, "//span[text()='用户名密码登录']")
    
    # 输入框 - 使用更简单的定位器
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='用户名']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='密码']")
    
    # 按钮 - 使用更简单的定位器
    LOGIN_BUTTON = (By.XPATH, "//span[text()='登录']")
    FORGET_PASSWORD_LINK = (By.LINK_TEXT, "扫码登录")
    
    # 错误提示
    ERROR_MESSAGE = (By.CLASS_NAME, "el-message--error")
    
    # 验证码相关
    CAPTCHA_INPUT = (By.ID, "captcha")
    CAPTCHA_IMAGE = (By.ID, "captcha-img")
    REFRESH_CAPTCHA = (By.ID, "refresh-captcha")


class DashboardPageLocators:
    """主页/仪表板页面元素定位器"""
    
    # 导航菜单
    NAVIGATION_MENU = (By.CLASS_NAME, "nav-menu")
    USER_PROFILE = (By.CLASS_NAME, "user-profile")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), '退出')]")
    
    # 主要内容区域
    MAIN_CONTENT = (By.ID, "main-content")
    WELCOME_MESSAGE = (By.CLASS_NAME, "welcome-message")
    
    # 统计卡片
    TOTAL_CUSTOMERS = (By.XPATH, "//div[@class='stat-card']//span[contains(text(), '客户总数')]")
    TOTAL_ORDERS = (By.XPATH, "//div[@class='stat-card']//span[contains(text(), '订单总数')]")
    TOTAL_REVENUE = (By.XPATH, "//div[@class='stat-card']//span[contains(text(), '总收入')]")


class CustomerPageLocators:
    """客户管理页面元素定位器"""
    
    # 搜索和筛选
    SEARCH_INPUT = (By.ID, "customer-search")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(text(), '搜索')]")
    FILTER_DROPDOWN = (By.ID, "customer-filter")
    
    # 表格
    CUSTOMER_TABLE = (By.ID, "customer-table")
    TABLE_HEADERS = (By.XPATH, "//table[@id='customer-table']//th")
    TABLE_ROWS = (By.XPATH, "//table[@id='customer-table']//tbody//tr")
    
    # 操作按钮
    ADD_CUSTOMER_BUTTON = (By.XPATH, "//button[contains(text(), '添加客户')]")
    EDIT_BUTTON = (By.CLASS_NAME, "edit-btn")
    DELETE_BUTTON = (By.CLASS_NAME, "delete-btn")
    VIEW_BUTTON = (By.CLASS_NAME, "view-btn")
    
    # 分页
    PAGINATION = (By.CLASS_NAME, "pagination")
    NEXT_PAGE = (By.XPATH, "//a[contains(text(), '下一页')]")
    PREV_PAGE = (By.XPATH, "//a[contains(text(), '上一页')]")


class OrderPageLocators:
    """订单管理页面元素定位器"""
    
    # 搜索和筛选
    ORDER_SEARCH = (By.ID, "order-search")
    DATE_FROM = (By.ID, "date-from")
    DATE_TO = (By.ID, "date-to")
    STATUS_FILTER = (By.ID, "status-filter")
    
    # 表格
    ORDER_TABLE = (By.ID, "order-table")
    ORDER_ROWS = (By.XPATH, "//table[@id='order-table']//tbody//tr")
    
    # 操作按钮
    CREATE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), '创建订单')]")
    EXPORT_BUTTON = (By.XPATH, "//button[contains(text(), '导出')]")
    
    # 订单状态
    STATUS_PENDING = (By.XPATH, "//span[@class='status pending']")
    STATUS_CONFIRMED = (By.XPATH, "//span[@class='status confirmed']")
    STATUS_SHIPPED = (By.XPATH, "//span[@class='status shipped']")
    STATUS_DELIVERED = (By.XPATH, "//span[@class='status delivered']")


class CommonLocators:
    """通用元素定位器"""
    
    # 通用按钮
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), '保存')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), '取消')]")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), '确认')]")
    CLOSE_BUTTON = (By.XPATH, "//button[contains(text(), '关闭')]")
    
    # 通用提示
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    WARNING_MESSAGE = (By.CLASS_NAME, "warning-message")
    INFO_MESSAGE = (By.CLASS_NAME, "info-message")
    
    # 加载状态
    LOADING_SPINNER = (By.CLASS_NAME, "loading-spinner")
    LOADING_OVERLAY = (By.CLASS_NAME, "loading-overlay")
    
    # 模态框
    MODAL_DIALOG = (By.CLASS_NAME, "modal")
    MODAL_HEADER = (By.CLASS_NAME, "modal-header")
    MODAL_BODY = (By.CLASS_NAME, "modal-body")
    MODAL_FOOTER = (By.CLASS_NAME, "modal-footer") 