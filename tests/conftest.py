"""
pytest配置文件
包含测试夹具(fixtures)和钩子函数(hooks)
"""
import pytest
import logging
import os
from datetime import datetime

from utils.driver_manager import DriverManager
from config.config import Config


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def driver_manager():
    """
    会话级别的WebDriver管理器夹具
    
    Returns:
        DriverManager实例
    """
    manager = DriverManager()
    yield manager
    manager.quit_driver()


@pytest.fixture(scope="function")
def driver(driver_manager):
    """
    函数级别的WebDriver夹具
    每个测试函数都会获得一个新的driver实例
    
    Args:
        driver_manager: WebDriver管理器
        
    Returns:
        WebDriver实例
    """
    driver = driver_manager.get_driver()
    yield driver
    # 测试完成后不退出driver，由session级别的夹具处理


@pytest.fixture(scope="function")
def fresh_driver(driver_manager):
    """
    获取全新的WebDriver实例
    用于需要重新启动浏览器的测试
    
    Args:
        driver_manager: WebDriver管理器
        
    Returns:
        WebDriver实例
    """
    driver = driver_manager.restart_driver()
    yield driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest钩子：生成测试报告
    在测试失败时自动截图
    """
    outcome = yield
    rep = outcome.get_result()
    
    # 只在测试失败时处理
    if rep.when == "call" and rep.failed:
        # 获取driver夹具
        driver = None
        for fixture_name in item.fixturenames:
            if fixture_name in ['driver', 'fresh_driver']:
                driver = item.funcargs.get(fixture_name)
                break
        
        if driver:
            # 生成截图文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("::", "_").replace(" ", "_")
            screenshot_name = f"failed_{test_name}_{timestamp}.png"
            
            # 截图
            try:
                os.makedirs(Config.SCREENSHOTS_PATH, exist_ok=True)
                screenshot_path = os.path.join(Config.SCREENSHOTS_PATH, screenshot_name)
                driver.save_screenshot(screenshot_path)
                logger.info(f"测试失败截图已保存: {screenshot_path}")
                
                # 将截图路径添加到测试报告中
                if hasattr(rep, 'extra'):
                    rep.extra = []
                rep.extra.append({'name': 'screenshot', 'path': screenshot_path})
                
            except Exception as e:
                logger.error(f"保存失败截图时出错: {e}")


def pytest_configure(config):
    """
    pytest配置钩子
    在测试开始前执行的配置
    """
    # 确保必要的目录存在
    os.makedirs(Config.SCREENSHOTS_PATH, exist_ok=True)
    os.makedirs(Config.REPORTS_PATH, exist_ok=True)
    
    logger.info("测试环境配置完成")
    logger.info(f"当前环境: {Config.CURRENT_ENV.value}")
    logger.info(f"基础URL: {Config.get_base_url()}")
    logger.info(f"浏览器: {Config.BROWSER}")
    logger.info(f"无头模式: {Config.HEADLESS}")


def pytest_unconfigure(config):
    """
    pytest清理钩子
    在所有测试完成后执行清理
    """
    logger.info("测试执行完成，开始清理...")


@pytest.fixture(scope="function")
def login_user_data():
    """
    登录用户数据夹具
    
    Returns:
        dict: 用户登录数据
    """
    return {
        "admin": Config.get_test_user("admin"),
        "user": Config.get_test_user("user")
    }


@pytest.fixture(scope="function", autouse=True)
def test_logger(request):
    """
    自动使用的测试日志夹具
    为每个测试记录开始和结束日志
    
    Args:
        request: pytest请求对象
    """
    test_name = request.node.name
    logger.info(f"开始执行测试: {test_name}")
    
    yield
    
    logger.info(f"测试执行完成: {test_name}")


@pytest.fixture(scope="function")
def base_url():
    """
    基础URL夹具
    
    Returns:
        str: 当前环境的基础URL
    """
    return Config.get_base_url()


# 添加命令行选项
def pytest_addoption(parser):
    """
    添加自定义命令行选项
    
    Args:
        parser: pytest参数解析器
    """
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome",
        help="指定浏览器类型: chrome, firefox, edge"
    )
    
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=False,
        help="启用无头模式"
    )
    
    parser.addoption(
        "--env", 
        action="store", 
        default="test",
        help="指定测试环境: dev, test, staging, prod"
    )


@pytest.fixture(scope="session", autouse=True)
def configure_from_cli(request):
    """
    从命令行参数配置测试环境
    
    Args:
        request: pytest请求对象
    """
    # 获取命令行参数
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    env = request.config.getoption("--env")
    
    # 更新配置
    Config.BROWSER = browser
    Config.HEADLESS = headless
    
    # 更新环境配置
    from config.config import Environment
    env_mapping = {
        "dev": Environment.DEV,
        "test": Environment.TEST,
        "staging": Environment.STAGING,
        "prod": Environment.PROD
    }
    
    if env in env_mapping:
        Config.CURRENT_ENV = env_mapping[env]
    
    logger.info(f"已从命令行更新配置 - 浏览器: {browser}, 无头模式: {headless}, 环境: {env}")


# 测试分组标记
@pytest.fixture(scope="function")
def smoke_test():
    """冒烟测试标记夹具"""
    pass


@pytest.fixture(scope="function") 
def regression_test():
    """回归测试标记夹具"""
    pass 