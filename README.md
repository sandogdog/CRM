# CRM UI自动化测试框架

基于Python + Selenium的CRM系统UI自动化测试框架，采用**模块化架构**设计，支持多浏览器、多环境测试。

## 🎯 项目特点

- **🔥 全新模块化架构**：将大型单体文件拆分为专门的功能模块，提高可维护性
- **⚡ 简化的交互界面**：新版main.py提供4个清晰的功能选择
- **🔄 向后兼容性**：保持所有原有API不变，可以无缝迁移
- **🧪 独立测试能力**：每个模块都可以独立测试和使用
- **📝 完整的业务流程**：涵盖登录、角色切换、线索管理、跟进等完整CRM操作

## 🚀 功能特性

- **页面对象模式(POM)**: 良好的代码组织结构，易于维护
- **多浏览器支持**: 支持Chrome、Firefox、Edge浏览器
- **多环境配置**: 支持开发、测试、预发布、生产环境
- **自动截图**: 测试失败时自动截图
- **详细日志**: 完整的测试执行日志记录
- **HTML报告**: 生成详细的HTML测试报告
- **并行执行**: 支持多线程并行测试
- **参数化测试**: 支持数据驱动测试
- **模块化架构**: 代码结构清晰，功能模块化，便于维护和扩展

## 📁 项目结构

```
CRM/
├── 🚀 核心模块（新架构）
│   ├── main.py                      # 主入口文件（简化菜单）
│   ├── crm_login.py                # 登录功能模块
│   ├── crm_role_switch.py          # 角色切换功能模块
│   ├── crm_utils.py                # 工具函数模块
│   ├── crm_private_sea_add.py      # 线索添加模块
│   ├── crm_private_sea_launch.py   # 投放模块
│   ├── crm_private_sea_follow_up.py # 快速跟进模块
│   ├── crm_workflow.py             # 工作流程编排
│   └── crm_private_sea.py          # 向后兼容层
│
├── 🧪 测试和验证
│   ├── test_modules.py             # 模块测试脚本
│   ├── auto_run.py                 # 自动化执行包装器
│   ├── run_tests.py                # Pytest运行脚本（传统）
│   ├── pytest.ini                 # Pytest配置
│   └── tests/                      # Pytest测试目录
│
├── 📚 传统框架（保留兼容）
│   ├── config/                     # 配置文件
│   ├── pages/                      # Page Object模式页面对象
│   ├── utils/                      # 原版工具函数
│   └── reports/                    # 测试报告目录
│
├── 📖 文档
│   ├── README.md                   # 项目说明（本文件）
│   ├── CLEANUP_SUMMARY.md          # 模块化重构总结
│   └── PROJECT_CLEANUP_PLAN.md     # 项目清理计划
│
└── 📸 输出
    ├── requirements.txt            # 依赖包
    └── screenshots/                # 截图目录
```

## 🛠️ 环境要求

- Python 3.8+
- Chrome/Firefox/Edge浏览器

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/sandogdog/CRM.git
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

## 🏃‍♂️ 快速开始

### 🚀 新版模块化架构（推荐）

使用全新的模块化架构，功能清晰，易于维护：

```bash
# 运行主程序（推荐）
python main.py
```

**提供4种测试选择：**
1. **测试私海线索添加功能** - 登录 → 角色切换 → 导航 → 添加线索
2. **测试私海线索投放功能** - 完整流程 + 投放操作
3. **测试私海线索快速跟进功能** - 完整流程 + 快速跟进 + 跟进面板 + 报价单
4. **测试所有私海线索功能** - 包含所有功能的完整测试

**模块化使用示例：**
```python
# 直接导入需要的模块
from crm_private_sea_add import add_private_sea_clue
from crm_private_sea_follow_up import complete_follow_up_process

# 或者使用向后兼容方式
from crm_private_sea import add_private_sea_clue, complete_follow_up_process
```

### 🔧 自动化模式

完全自动化执行，适合生产环境：

```bash
# 使用简化的自动化入口
python auto_run.py
```

**自动化流程包含：**
1. ✅ SSO登录
2. ✅ 职位切换  
3. ✅ 私海线索页面导航
4. ✅ 添加私海线索
5. ✅ 投放操作
6. ✅ 快速跟进按钮点击
7. ✅ 跟进面板配置（电话/商机转化）
8. ✅ 报价单填写

### 🧪 运行传统测试框架

保持向后兼容，仍支持原有的测试方式：

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_login.py

# 使用测试运行脚本
python run_tests.py --action all
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

## ✨ 模块化架构特性

### 新的模块化架构优势

- **代码结构清晰**: 从700行单一文件拆分为多个专门模块
- **易于维护**: 每个模块专注特定功能
- **代码重用**: 各模块可单独调用
- **易于测试**: 可以单独测试每个功能
- **扩展性强**: 可以轻松添加新功能模块

### 模块说明

- `crm_utils.py`: 工具函数（随机数据生成、浏览器初始化）
- `crm_login.py`: SSO登录功能
- `crm_role_switch.py`: 用户职位切换功能
- `crm_private_sea.py`: 私海线索操作和快速跟进功能
- `crm_workflow.py`: 集成所有功能的完整工作流程

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
7. **模块化**: 将功能拆分为独立模块，提高代码可维护性

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

- GitHub: [@sandogdog](https://github.com/sandogdog)
- 项目地址: [https://github.com/sandogdog/CRM](https://github.com/sandogdog/CRM)
