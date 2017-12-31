# -*- coding: utf-8 -*-

# 销售
S_FORECAST_1 = 1
S_ORDER_2 = 2
S_RETURN_3 = 3

# 仓储
ST_OUT_STORE_20 = 20
ST_OTHER_IN_21 = 21
ST_OTHER_OUT_22 = 22
ST_SALE_RETURN_23 = 23
ST_STOCK_CHECK_24 = 24
ST_TRANSFER_IN_25 = 25
ST_TRANSFER_OUT_26 = 26

# 财务
F_SALE_ACCOUNT_40 = 40

# 活禽采购
PP_REQUEST_60 = 60
PP_DISPATCH_CAR_61 = 61

BILL_TYPE = [
    # 销售
    (S_FORECAST_1, '销售预报'),
    (S_ORDER_2, '销售订单'),
    (S_RETURN_3, '销售退单'),

    # 仓储
    (ST_OUT_STORE_20, '销售出库'),
    (ST_OTHER_IN_21, '其他入库'),
    (ST_OTHER_OUT_22, '其他出库'),
    (ST_SALE_RETURN_23, '销售退库'),
    (ST_STOCK_CHECK_24, '库存盘点'),
    (ST_TRANSFER_IN_25, '调拨入库'),
    (ST_TRANSFER_OUT_26, '调拨出库'),

    # 财务
    (F_SALE_ACCOUNT_40, '销售账单'),

    # 活禽采购
    (PP_REQUEST_60, '订购申请'),
    (PP_DISPATCH_CAR_61, '采购派车'),

]
