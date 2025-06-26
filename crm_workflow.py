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
from crm_private_sea_add import navigate_to_private_sea, add_private_sea_clue
from crm_private_sea_launch import handle_launch_operation
from crm_private_sea_follow_up import click_quick_follow_up, handle_follow_up_panel, complete_follow_up_process

# 配置日志
logger = logging.getLogger(__name__)


def login_and_switch_role(driver=None):
    """
    基础工作流程：登录 + 职位切换
    
    Args:
        driver: 可选的WebDriver实例，如果不提供则创建新的
    
    Returns:
        WebDriver实例或False
    """
    if driver is None:
        driver = setup_browser()
    
    try:
        logger.info("🚀 开始基础工作流程：登录 + 职位切换")
        
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
            logger.info("🎉 基础工作流程执行成功！")
        else:
            logger.warning("⚠️ 职位切换可能未完全成功")
        
        return driver
        
    except Exception as e:
        logger.error(f"基础工作流程执行异常: {e}")
        return False


def login_switch_and_navigate_to_private_sea(driver=None):
    """
    扩展工作流程：登录 + 职位切换 + 导航到私海线索页面
    
    Args:
        driver: 可选的WebDriver实例
    
    Returns:
        WebDriver实例或False
    """
    try:
        logger.info("🚀 开始扩展工作流程：登录 + 职位切换 + 私海线索导航")
        
        # 执行基础工作流程
        driver = login_and_switch_role(driver)
        if not driver:
            return False
        
        # 导航到私海线索页面
        logger.info("开始导航到私海线索页面...")
        navigate_success = navigate_to_private_sea(driver)
        
        if navigate_success:
            logger.info("🎉 扩展工作流程执行成功！")
            return driver
        else:
            logger.warning("⚠️ 私海线索页面导航失败")
            return driver  # 仍然返回driver，因为前面的步骤成功了
        
    except Exception as e:
        logger.error(f"扩展工作流程执行异常: {e}")
        return False


def full_workflow_with_clue_creation(driver=None):
    """
    完整工作流程：登录 + 职位切换 + 私海线索导航 + 添加线索
    
    Args:
        driver: 可选的WebDriver实例
    
    Returns:
        tuple: (driver实例, 客户名称, 电话号码)
    """
    try:
        logger.info("🚀 开始完整工作流程：包含线索创建")
        
        # 执行扩展工作流程
        driver = login_switch_and_navigate_to_private_sea(driver)
        if not driver:
            return False, None, None
        
        # 添加私海线索
        logger.info("开始添加私海线索...")
        clue_success, customer_name, phone = add_private_sea_clue(driver)
        
        if clue_success:
            logger.info("🎉 完整工作流程（含线索创建）执行成功！")
            return driver, customer_name, phone
        else:
            logger.warning("⚠️ 私海线索添加失败")
            return driver, None, None
        
    except Exception as e:
        logger.error(f"完整工作流程（含线索创建）执行异常: {e}")
        return False, None, None


def full_workflow_with_follow_up(driver=None, skip_clue_creation=False):
    """
    最完整工作流程：登录 + 职位切换 + 私海线索导航 + (可选)添加线索 + 快速跟进
    
    Args:
        driver: 可选的WebDriver实例
        skip_clue_creation: 是否跳过线索创建步骤
    
    Returns:
        tuple: (driver实例, 客户名称, 电话号码, 跟进成功状态)
    """
    try:
        logger.info("🚀 开始最完整工作流程：包含快速跟进")
        
        customer_name = None
        phone = None
        
        if skip_clue_creation:
            # 跳过线索创建，直接导航到私海线索页面
            driver = login_switch_and_navigate_to_private_sea(driver)
            if not driver:
                return False, None, None, False
            logger.info("⏭️ 跳过线索创建步骤")
        else:
            # 包含线索创建
            driver, customer_name, phone = full_workflow_with_clue_creation(driver)
            if not driver:
                return False, None, None, False
        
        # 执行完整快速跟进流程
        logger.info("开始完整快速跟进流程...")
        follow_up_success = complete_follow_up_process(driver)
        
        if follow_up_success:
            logger.info("🎉 最完整工作流程执行成功！")
            return driver, customer_name, phone, True
        else:
            logger.warning("⚠️ 快速跟进流程失败")
            return driver, customer_name, phone, False
        
    except Exception as e:
        logger.error(f"最完整工作流程执行异常: {e}")
        return False, None, None, False


# 保持向后兼容的函数名
def login_and_complete_workflow():
    """
    完整的自动化工作流程（向后兼容）
    
    Returns:
        tuple: (driver实例, 客户名称, 电话号码, 快速跟进成功状态)
    """
    return full_workflow_with_follow_up()


def login_and_switch_role_fixed_v2():
    """
    修复版完整流程 v2（仅登录和职位切换）- 向后兼容
    
    Returns:
        WebDriver实例或False
    """
    return login_and_switch_role()


def test_quick_follow_up_only():
    """
    仅测试快速跟进功能（需要先登录到私海线索页面）
    
    Returns:
        WebDriver实例或False
    """
    try:
        logger.info("🚀 开始快速跟进功能测试")
        
        # 导航到私海线索页面
        driver = login_switch_and_navigate_to_private_sea()
        if not driver:
            return False
        
        # 执行完整快速跟进流程
        follow_up_success = complete_follow_up_process(driver)
        
        if follow_up_success:
            logger.info("🎉 快速跟进功能测试成功！")
            return driver
        else:
            logger.warning("⚠️ 快速跟进功能测试失败")
            return False
        
    except Exception as e:
        logger.error(f"快速跟进功能测试异常: {e}")
        return False 