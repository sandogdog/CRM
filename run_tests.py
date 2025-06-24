#!/usr/bin/env python
"""
测试运行脚本
提供便捷的测试执行入口
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime


def run_command(command):
    """
    执行命令并输出结果
    
    Args:
        command: 要执行的命令
    """
    print(f"执行命令: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if result.stdout:
            print("输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"命令执行失败，退出码: {result.returncode}")
        else:
            print("命令执行成功!")
            
    except Exception as e:
        print(f"执行命令时发生异常: {e}")


def install_dependencies():
    """安装项目依赖"""
    print("🔧 安装项目依赖...")
    run_command("pip install -r requirements.txt")


def run_smoke_tests(browser="chrome", headless=False):
    """运行冒烟测试"""
    print("🔥 运行冒烟测试...")
    headless_flag = "--headless" if headless else ""
    command = f"pytest -m smoke --browser={browser} {headless_flag} -v"
    run_command(command)


def run_regression_tests(browser="chrome", headless=False):
    """运行回归测试"""
    print("🔄 运行回归测试...")
    headless_flag = "--headless" if headless else ""
    command = f"pytest -m regression --browser={browser} {headless_flag} -v"
    run_command(command)


def run_all_tests(browser="chrome", headless=False, parallel=False):
    """运行所有测试"""
    print("🚀 运行所有测试...")
    headless_flag = "--headless" if headless else ""
    parallel_flag = "-n auto" if parallel else ""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/report_{timestamp}.html"
    
    command = f"pytest --browser={browser} {headless_flag} {parallel_flag} --html={report_path} --self-contained-html -v"
    run_command(command)
    
    print(f"📊 测试报告已生成: {report_path}")


def run_specific_test(test_path, browser="chrome", headless=False):
    """运行指定测试"""
    print(f"🎯 运行指定测试: {test_path}")
    headless_flag = "--headless" if headless else ""
    command = f"pytest {test_path} --browser={browser} {headless_flag} -v -s"
    run_command(command)


def generate_allure_report():
    """生成Allure报告"""
    print("📈 生成Allure报告...")
    run_command("pytest --alluredir=reports/allure-results")
    run_command("allure serve reports/allure-results")


def check_environment():
    """检查测试环境"""
    print("🔍 检查测试环境...")
    
    # 检查Python版本
    python_version = sys.version
    print(f"Python版本: {python_version}")
    
    # 检查必要目录
    required_dirs = ["config", "pages", "tests", "utils", "reports", "screenshots"]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name} 目录存在")
        else:
            print(f"✗ {dir_name} 目录不存在")
    
    # 检查必要文件
    required_files = ["requirements.txt", "pytest.ini", "README.md"]
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✓ {file_name} 文件存在")
        else:
            print(f"✗ {file_name} 文件不存在")


def clean_reports():
    """清理测试报告和截图"""
    print("🧹 清理测试报告和截图...")
    
    import glob
    import shutil
    
    # 清理报告文件
    report_files = glob.glob("reports/*.html") + glob.glob("reports/*.xml")
    for file_path in report_files:
        try:
            os.remove(file_path)
            print(f"已删除: {file_path}")
        except Exception as e:
            print(f"删除失败 {file_path}: {e}")
    
    # 清理截图文件
    screenshot_files = glob.glob("screenshots/*.png")
    for file_path in screenshot_files:
        try:
            os.remove(file_path)
            print(f"已删除: {file_path}")
        except Exception as e:
            print(f"删除失败 {file_path}: {e}")
    
    # 清理日志文件
    if os.path.exists("test.log"):
        try:
            os.remove("test.log")
            print("已删除: test.log")
        except Exception as e:
            print(f"删除日志文件失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="CRM UI自动化测试运行脚本")
    parser.add_argument("--action", choices=[
        "install", "check", "smoke", "regression", "all", "specific", "allure", "clean"
    ], default="all", help="要执行的操作")
    
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge"], 
                       default="chrome", help="浏览器类型")
    parser.add_argument("--headless", action="store_true", help="启用无头模式")
    parser.add_argument("--parallel", action="store_true", help="并行执行测试")
    parser.add_argument("--test", help="指定要运行的测试路径")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎯 CRM UI自动化测试框架")
    print("=" * 60)
    
    if args.action == "install":
        install_dependencies()
    elif args.action == "check":
        check_environment()
    elif args.action == "smoke":
        run_smoke_tests(args.browser, args.headless)
    elif args.action == "regression":
        run_regression_tests(args.browser, args.headless)
    elif args.action == "all":
        run_all_tests(args.browser, args.headless, args.parallel)
    elif args.action == "specific":
        if args.test:
            run_specific_test(args.test, args.browser, args.headless)
        else:
            print("❌ 请使用 --test 参数指定要运行的测试路径")
    elif args.action == "allure":
        generate_allure_report()
    elif args.action == "clean":
        clean_reports()
    
    print("=" * 60)
    print("✅ 操作完成!")


if __name__ == "__main__":
    main() 