#!/usr/bin/env python
"""
CRM自动化测试 - 私海线索管理模块（向后兼容版本）

此文件已被模块化拆分为以下新模块：
- crm_private_sea_add.py：线索添加功能
- crm_private_sea_launch.py：投放功能  
- crm_private_sea_follow_up.py：快速跟进功能

此文件提供向后兼容性支持，重新导出所有功能。
建议直接使用新的模块化版本。
"""

# 从新模块导入所有功能
from crm_private_sea_add import (
    navigate_to_private_sea,
    add_private_sea_clue,
    test_private_sea_add_workflow
)

from crm_private_sea_launch import (
    handle_launch_operation,
    test_private_sea_launch_workflow
)

from crm_private_sea_follow_up import (
    click_quick_follow_up,
    handle_follow_up_panel,
    handle_quotation_tab,
    complete_follow_up_process,
    test_private_sea_follow_up_workflow
)

# 重新导出所有功能以保持兼容性
__all__ = [
    # 导航和添加功能
    'navigate_to_private_sea',
    'add_private_sea_clue',
    'test_private_sea_add_workflow',
    
    # 投放功能
    'handle_launch_operation', 
    'test_private_sea_launch_workflow',
    
    # 快速跟进功能
    'click_quick_follow_up',
    'handle_follow_up_panel',
    'handle_quotation_tab',
    'complete_follow_up_process',
    'test_private_sea_follow_up_workflow'
] 