# -*- coding: utf-8 -*-

bill_state = [(1, '未审核'), (10, '已审核'), (20, '已完毕')]

create_type = [(1, '不生成'), (10, '未审核'), (20, '已审核')]

create_type2 = [(1, '不生成'), (10, '未确认'), (20, '已确认')]

available = [(1, '不启用'), (10, '启用')]

# 销售流程状态：
process_state = [(1, '未审核'), (10, '已审核'), (20, '已装货'), (30, '已复磅'), (40, '待付款'), (50, '已开票')]

# 活禽采购流程状态：
process_state_poultry_purchase = [(1, '未确认'), (10, '已确认')]

# 价格单类型
CLASS_PRICE_1 = 1  # 分类价
PRICE_BILL_TYPE = [
    # 销售
    (CLASS_PRICE_1, '分类价'),
]
