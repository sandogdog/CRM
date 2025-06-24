#!/usr/bin/env python
"""
CRM自动化测试 - 主工作流程模块
集成登录、职位切换、私海线索等功能
"""
import os
import time
import logging
from crm_utils import setup_browser
from crm_login import login_to_crm
from crm_role_switch import switch_role_fixed_v2
from crm_private_sea import add_private_sea_clue, click_quick_follow_up

# 配置日志
logger = logging.getLogger(__name__)


def login_and_complete_workflow():
    """
    完整的自动化工作流程：登录 -> 职位切换 -> 私海线索测试 -> 点击快速跟进
    
    Returns:
        tuple: (driver实例, 客户名称, 电话号码, 快速跟进成功状态)
    """
    driver = None
    
    try:
        logger.info("🚀 开始完整自动化工作流程")
        
        # 初始化浏览器
        driver = setup_browser()
        
        # 登录
        login_success = login_to_crm(driver)
        if not login_success:
            logger.error("❌ 登录失败，终止流程")
            return False, None, None, False
        
        # 创建截图目录
        os.makedirs("screenshots", exist_ok=True)
        
        # 执行职位切换
        logger.info("开始职位切换...")
        switch_success = switch_role_fixed_v2(driver)
        
        if not switch_success:
            logger.warning("⚠️ 职位切换失败，但继续执行私海线索测试")
        
        # 执行私海线索测试
        logger.info("开始私海线索测试...")
        clue_success, customer_name, phone = add_private_sea_clue(driver)
        
        if not clue_success:
            logger.warning("⚠️ 私海线索测试失败，但继续尝试点击快速跟进")
        
        # 点击快速跟进按钮
        logger.info("开始点击快速跟进按钮...")
        quick_follow_success = click_quick_follow_up(driver)
        
        # 返回完整结果
        if clue_success and quick_follow_success:
            logger.info("🎉 完整工作流程执行成功！")
            return driver, customer_name, phone, True
        elif quick_follow_success:
            logger.info("🎉 快速跟进功能执行成功！")
            return driver, customer_name, phone, True
        else:
            logger.warning("⚠️ 部分功能执行失败")
            return driver, customer_name, phone, False
        
    except Exception as e:
        logger.error(f"工作流程执行异常: {e}")
        return False, None, None, False


def login_and_switch_role_fixed_v2():
    """
    修复版完整流程 v2（仅登录和职位切换）
    
    Returns:
        WebDriver实例或False
    """
    driver = None
    
    try:
        logger.info("🚀 开始修复版自动化流程 v2")
        
        # 初始化浏览器
        driver = setup_browser()
        
        # 登录
        login_success = login_to_crm(driver)
        if not login_success:
            logger.error("❌ 登录失败，终止流程")
            return False
        
        # 创建截图目录
        os.makedirs("screenshots", exist_ok=True)
        
        # 执行职位切换
        logger.info("开始职位切换...")
        switch_success = switch_role_fixed_v2(driver)
        
        if switch_success:
            logger.info("🎉 完整流程执行成功！")
        else:
            logger.warning("⚠️ 职位切换可能未完全成功")
        
        return driver
        
    except Exception as e:
        logger.error(f"流程执行异常: {e}")
        return False


def test_quick_follow_up_only():
    """
    仅测试快速跟进功能（需要先登录到私海线索页面）
    
    Returns:
        WebDriver实例或False
    """
    driver = None
    
    try:
        logger.info("🚀 开始快速跟进功能测试")
        
        # 初始化浏览器
        driver = setup_browser()
        
        # 登录
        login_success = login_to_crm(driver)
        if not login_success:
            logger.error("❌ 登录失败，终止流程")
            return False
        
        # 创建截图目录
        os.makedirs("screenshots", exist_ok=True)
        
        # 直接导航到私海线索页面
        logger.info("导航到私海线索页面...")
        private_sea_url = "https://test-admin-crm.cd.xiaoxigroup.net/customerManagement/clews/privateSea"
        driver.get(private_sea_url)
        time.sleep(3)
        
        # 点击快速跟进按钮
        logger.info("开始点击快速跟进按钮...")
        quick_follow_success = click_quick_follow_up(driver)
        
        if quick_follow_success:
            logger.info("🎉 快速跟进功能测试成功！")
            return driver
        else:
            logger.warning("⚠️ 快速跟进功能测试失败")
            return False
        
    except Exception as e:
        logger.error(f"快速跟进功能测试异常: {e}")
        return False 