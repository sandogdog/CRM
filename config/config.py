"""
项目配置文件
包含测试环境配置、浏览器设置、超时时间等
"""
import os
from enum import Enum


class Environment(Enum):
    """环境枚举"""
    DEV = "dev"
    TEST = "test" 
    STAGING = "staging"
    PROD = "prod"


class Config:
    """配置类"""
    
    # 环境配置
    CURRENT_ENV = Environment.TEST
    
    # URL配置
    BASE_URLS = {
        Environment.DEV: "https://sso.xiaoxitech.com/login?project=hqhtmsb1&cb=https%3A%2F%2Ftest-admin-crm.cd.xiaoxigroup.net%2Flogin",
        Environment.TEST: "https://sso.xiaoxitech.com/login?project=hqhtmsb1&cb=https%3A%2F%2Ftest-admin-crm.cd.xiaoxigroup.net%2Flogin", 
        Environment.STAGING: "https://sso.xiaoxitech.com/login?project=hqhtmsb1&cb=https%3A%2F%2Ftest-admin-crm.cd.xiaoxigroup.net%2Flogin",
        Environment.PROD: "https://sso.xiaoxitech.com/login?project=hqhtmsb1&cb=https%3A%2F%2Ftest-admin-crm.cd.xiaoxigroup.net%2Flogin"
    }
    
    # 浏览器配置
    BROWSER = "edge"  # chrome, firefox, edge
    HEADLESS = False
    WINDOW_SIZE = "1920,1080"
    
    # 超时配置(秒)
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    
    # 测试数据配置
    TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "../test_data")
    SCREENSHOTS_PATH = os.path.join(os.path.dirname(__file__), "../screenshots")
    REPORTS_PATH = os.path.join(os.path.dirname(__file__), "../reports")
    
    # 测试用户配置
    TEST_USERS = {
        "admin": {
            "username": "qinrenchi",
            "password": "Sandog031220@"
        },
        "user": {
            "username": "qinrenchi", 
            "password": "Sandog031220@"
        }
    }
    
    @classmethod
    def get_base_url(cls):
        """获取当前环境的基础URL"""
        return cls.BASE_URLS[cls.CURRENT_ENV]
    
    @classmethod
    def get_test_user(cls, user_type="admin"):
        """获取测试用户信息"""
        return cls.TEST_USERS.get(user_type, cls.TEST_USERS["admin"]) 