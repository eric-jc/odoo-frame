# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DetailBase(models.BaseModel):  # 存货明细，含数量单价金额
    _auto = False
    _abstract = True
    _transient = False
    _register = False

    goods_id = fields.Many2one('archives.goods', string=u'产品', required=True,
                               domain=lambda self: self.env['archives.organization'].get_goods_organization())
    # need_second_change = fields.Selection([
    #     ('1', '是'),
    #     ('0', '否')
    # ], related='goods_id.need_second_change', string=u'辅单位是否换算', default='1')
    second_unit_id = fields.Many2one('archives.unit', string=u'辅单位', compute='_set_second', store=True)
    second_unit_number = fields.Float(digits=(6, 2), string=u'辅数量')
    main_unit_id = fields.Many2one('archives.unit', string=u'主单位', compute='_set_main', store=True)
    main_unit_number = fields.Float(digits=(6, 2), string=u'主数量')

    price = fields.Float(digits=(6, 2), help="单价", string=u'单价')
    money = fields.Float(digits=(6, 2), help="金额", string=u'金额', compute='_set_money', store=True)

    @api.depends('price', 'main_unit_number')
    def _set_money(self):
        for record in self:
            record.money = record.price * record.main_unit_number

    def _compute_money(self):
        self.money = self.price * self.main_unit_number

    @api.depends('goods_id')
    def _set_main(self):
        for record in self:
            record.main_unit_id = record.goods_id.main_unit_id

    @api.depends('goods_id')
    def _set_second(self):
        for record in self:
            if record.goods_id.need_change():
                record.second_unit_id = record.goods_id.second_unit_id
            else:
                record.second_unit_id = None

    @api.onchange('price', 'main_unit_number')
    def _onchange_for_money(self):
        self._compute_money()

    @api.onchange('second_unit_number')
    def _onchange_second(self):
        if not self.goods_id.need_change():
            return
        if self.goods_id.second_rate != 0:
            self.main_unit_number = self.goods_id.second_rate * self.second_unit_number

    @api.onchange('main_unit_number')
    def _onchange_main(self):
        if not self.goods_id.need_change():
            return
        if self.goods_id.second_rate != 0:
            self.second_unit_number = self.main_unit_number / self.goods_id.second_rate

    @api.onchange('goods_id')
    def _onchange_goods(self):
        if self.goods_id.need_change():
            self.second_unit_id = self.goods_id.second_unit_id
        else:
            self.second_unit_id = None
        self.main_unit_id = self.goods_id.main_unit_id
        self.second_unit_number = None
        self.main_unit_number = None
        self.price = None
        self.money = None


class GoodsDetail(DetailBase):
    _auto = True  # automatically create database backend
    _register = False  # not visible in ORM registry, meant to be python-inherited only
    _abstract = False  # not abstract
    _transient = False  # transient


class TransientGoodsDetail(DetailBase):
    _auto = True  # automatically create database backend
    _register = False  # not visible in ORM registry, meant to be python-inherited only
    _abstract = False  # not abstract
    _transient = True  # transient
