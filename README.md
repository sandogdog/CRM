# CRM UI自动化测试框架

基于Python + Selenium的CRM系统UI自动化测试框架，采用页面对象模式(POM)设计，支持多浏览器、多环境测试。

## 🚀 功能特性

- **页面对象模式(POM)**: 良好的代码组织结构，易于维护
- **多浏览器支持**: 支持Chrome、Firefox、Edge浏览器
- **多环境配置**: 支持开发、测试、预发布、生产环境
- **自动截图**: 测试失败时自动截图
- **详细日志**: 完整的测试执行日志记录
- **HTML报告**: 生成详细的HTML测试报告
- **并行执行**: 支持多线程并行测试
- **参数化测试**: 支持数据驱动测试

## 📁 项目结构

```
CRM/
├── config/                 # 配置文件目录
│   ├── __init__.py
│   ├── config.py          # 项目配置
│   └── locators.py        # 页面元素定位器
├── pages/                 # 页面对象目录
│   ├── __init__.py
│   ├── base_page.py       # 基础页面类
│   └── login_page.py      # 登录页面类
├── tests/                 # 测试用例目录
│   ├── __init__.py
│   ├── conftest.py        # pytest配置
│   └── test_login.py      # 登录功能测试
├── utils/                 # 工具类目录
│   ├── __init__.py
│   ├── driver_manager.py  # WebDriver管理器
│   └── common_utils.py    # 通用工具类
├── reports/               # 测试报告目录
├── screenshots/           # 截图目录
├── requirements.txt       # 项目依赖
├── pytest.ini           # pytest配置文件
└── README.md             # 项目说明文档
```

## 🛠️ 环境要求

- Python 3.8+
- Chrome/Firefox/Edge浏览器

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone <项目地址>
cd CRM
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置测试环境

编辑 `config/config.py` 文件，更新以下配置：

- **BASE_URLS**: 各环境的CRM系统地址
- **TEST_USERS**: 测试用户账号信息
- **浏览器设置**: 默认浏览器类型、窗口大小等

## 🏃‍♂️ 运行测试

### 基本运行

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_login.py

# 运行指定测试方法
pytest tests/test_login.py::TestLogin::test_successful_login_with_admin
```

### 标记测试

```bash
# 运行冒烟测试
pytest -m smoke

# 运行回归测试
pytest -m regression

# 运行登录相关测试
pytest -m login
```

### 指定浏览器

```bash
# 使用Chrome浏览器
pytest --browser=chrome

# 使用Firefox浏览器
pytest --browser=firefox

# 使用Edge浏览器
pytest --browser=edge

# 启用无头模式
pytest --headless
```

### 指定环境

```bash
# 测试环境
pytest --env=test

# 开发环境
pytest --env=dev

# 预发布环境
pytest --env=staging
```

### 并行执行

```bash
# 使用4个进程并行执行
pytest -n 4

# 自动检测CPU核数并行执行
pytest -n auto
```

### 生成报告

```bash
# 生成HTML报告
pytest --html=reports/report.html --self-contained-html

# 生成Allure报告
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 📊 测试报告

测试执行完成后，可以查看以下报告：

- **HTML报告**: `reports/report.html`
- **测试日志**: `test.log`
- **失败截图**: `screenshots/` 目录下的PNG文件

## 🔧 配置说明

### 环境配置

在 `config/config.py` 中配置不同环境的URL：

```python
BASE_URLS = {
    Environment.DEV: "http://dev-crm.example.com",
    Environment.TEST: "http://test-crm.example.com", 
    Environment.STAGING: "http://staging-crm.example.com",
    Environment.PROD: "http://crm.example.com"
}
```

### 用户配置

配置测试用户账号：

```python
TEST_USERS = {
    "admin": {
        "username": "admin@crm.com",
        "password": "admin123"
    },
    "user": {
        "username": "user@crm.com", 
        "password": "user123"
    }
}
```

### 浏览器配置

```python
BROWSER = "chrome"          # 默认浏览器
HEADLESS = False           # 是否无头模式
WINDOW_SIZE = "1920,1080"  # 窗口大小
IMPLICIT_WAIT = 10         # 隐式等待时间
EXPLICIT_WAIT = 20         # 显式等待时间
```

## 📝 编写测试用例

### 1. 创建页面对象

```python
from pages.base_page import BasePage
from config.locators import YourPageLocators

class YourPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = Config.get_base_url() + "/your-page"
    
    def your_action(self):
        self.click_element(YourPageLocators.YOUR_BUTTON)
```

### 2. 添加元素定位器

在 `config/locators.py` 中添加：

```python
class YourPageLocators:
    YOUR_BUTTON = (By.ID, "your-button-id")
    YOUR_INPUT = (By.NAME, "your-input-name")
```

### 3. 编写测试用例

```python
import pytest
from pages.your_page import YourPage

class TestYourFeature:
    def test_your_function(self, driver):
        your_page = YourPage(driver)
        your_page.open()
        your_page.your_action()
        assert your_page.is_element_displayed(YourPageLocators.RESULT)
```

## 🐛 调试技巧

### 1. 查看详细日志

```bash
pytest -v -s
```

### 2. 在失败时暂停

```bash
pytest --pdb
```

### 3. 只运行失败的测试

```bash
pytest --lf
```

### 4. 截图调试

```python
# 在测试代码中手动截图
login_page.take_screenshot("debug_screenshot")
```

## 🔍 常见问题

### Q: 如何处理验证码？
A: 在 `login_page.py` 中已经包含验证码处理逻辑，可以根据实际情况调整。

### Q: 如何添加新的页面对象？
A: 参考 `pages/login_page.py`，继承 `BasePage` 类，实现具体的页面操作方法。

### Q: 如何配置不同的测试数据？
A: 可以创建 `test_data` 目录，使用JSON或YAML文件存储测试数据。

### Q: 浏览器驱动下载失败怎么办？
A: 框架使用 `webdriver-manager` 自动下载驱动，确保网络连接正常。

## 📈 最佳实践

1. **页面对象**: 每个页面创建对应的页面对象类
2. **元素定位**: 统一在 `locators.py` 中管理元素定位器
3. **测试数据**: 使用参数化测试处理多组测试数据
4. **断言**: 使用有意义的断言信息
5. **日志**: 在关键步骤记录日志信息
6. **截图**: 测试失败时自动截图便于调试

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

 