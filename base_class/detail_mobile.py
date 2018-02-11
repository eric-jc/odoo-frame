# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import detail


# 提取的类不能直接使用，否则会出现错误。举例：应用到【销售订单】中时，{金额}在保存时，还是保持保存前的值。
# 这是因为depends没有生效。正常情况下，在执行保持操作时，会执行对应的depends方法。但是，继承这个基类，就不会执行。有时间时，查明该问题的原因
class DetailMobileBase(detail.DetailBase):  # 存货明细，含数量单价金额，用于手机
    _auto = False
    _abstract = True
    _transient = False
    _register = False

    second_unit_number_tmp = fields.Char(string=u'辅数量')
    main_unit_number_tmp = fields.Char(string=u'主数量')

    price_tmp = fields.Char(string=u'单价')

    def _compute_money(self):
        self.money = self.price * self.main_unit_number

    @api.onchange('second_unit_number_tmp')
    def _onchange_for_second_unit_number_from_tmp(self):
        self.second_unit_number = float(self.second_unit_number_tmp)
        if not self.goods_id.need_change():
            return
        self.main_unit_number = self.goods_id.second_rate * self.second_unit_number
        self.main_unit_number_tmp = None if self.main_unit_number == 0 else str(self.main_unit_number)
        self._compute_money()

    @api.onchange('main_unit_number_tmp')
    def _onchange_for_main_unit_number_from_tmp(self):
        self.main_unit_number = float(self.main_unit_number_tmp)
        self._compute_money()
        if not self.goods_id.need_change():
            return
        if self.goods_id.second_rate != 0:
            self.second_unit_number = self.main_unit_number / self.goods_id.second_rate
            self.second_unit_number_tmp = None if self.second_unit_number == 0 else str(self.second_unit_number)

    @api.onchange('price_tmp')
    def _onchange_for_price_from_tmp(self):
        self.price = float(self.price_tmp)
        self._compute_money()

    @api.onchange('goods_id')
    def _onchange_goods2(self):
        self.second_unit_number_tmp = None
        self.main_unit_number_tmp = None
        self.price_tmp = None

    @api.model
    def create(self, values):
        DetailMobileBase._set_tmp_for_number(values)
        return super(DetailMobileBase, self).create(values)

    @staticmethod
    def _set_tmp_for_number(values):
        if 'second_unit_number' in values:
            values['second_unit_number_tmp'] = None if values['second_unit_number'] == 0 else str(
                values['second_unit_number'])
        if 'main_unit_number' in values:
            values['main_unit_number_tmp'] = None if values['main_unit_number'] == 0 else str(
                values['main_unit_number'])
        if 'price' in values:
            values['price_tmp'] = None if values['price'] == 0 else str(values['price'])

    @api.multi
    def write(self, values):
        DetailMobileBase._set_tmp_for_number(values)
        return super(DetailMobileBase, self).write(values)


class GoodsDetailMobile(DetailMobileBase):
    _auto = True  # automatically create database backend
    _register = False  # not visible in ORM registry, meant to be python-inherited only
    _abstract = False  # not abstract
    _transient = False  # transient


class TransientGoodsDetailMobile(DetailMobileBase):
    _auto = True  # automatically create database backend
    _register = False  # not visible in ORM registry, meant to be python-inherited only
    _abstract = False  # not abstract
    _transient = True  # transient
