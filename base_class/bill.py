# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.utils import constant

ignore_fields_when_cannot_save = ['bill_state', 'check_uid', 'process_state']


class BillBase(models.BaseModel):
    _auto = False
    _abstract = True
    _transient = False
    _register = False

    bill_state = fields.Selection(constant.bill_state, string=u'单据状态', required=True, default=1, readonly=True)

    name = fields.Char(string=u'单据编号', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: '新建')
    date = fields.Date(string=u'日期', required=True, default=fields.Date.context_today)
    remark = fields.Char(string=u'摘要')

    create_uid = fields.Many2one('res.users', string='创建人', readonly=True)
    check_uid = fields.Many2one('res.users', string='审核人', readonly=True)

    can_check = fields.Boolean('是否拥有审核权限', compute='_compute_check')
    can_uncheck = fields.Boolean('是否拥有撤销权限', compute='_compute_uncheck')
    can_finish = fields.Boolean('是否拥有完毕权限', compute='_compute_finish')
    can_unfinish = fields.Boolean('是否拥有撤销完毕权限', compute='_compute_unfinish')

    @api.model
    def get_code(self):
        raise ValidationError('开发错误：请重写 get_code 方法')

    def _get_error_info(self):
        if self.bill_state == 10:
            return self._description + self.name + u' 已审核,不能删除.'
        if self.bill_state == 20:
            return self._description + self.name + u' 已完毕,不能删除.'
        return u'单据状态的逻辑存在缺陷，请联系开发者'

    def before_create(self, values):
        if values.get('name', '新建') == '新建':
            n = self.get_code()
            values['name'] = self.env['ir.sequence'].next_by_code(n) or '新建'

    def before_save(self, values):
        return

    def after_save(self, values):
        return

    @api.multi
    def unlink(self):
        if self.bill_state > 1:
            msg = self._get_error_info()
            raise ValidationError(msg)
        return super(BillBase, self).unlink()

    @api.model
    def create(self, values):
        self.before_create(values)
        self.before_save(values)
        result = super(BillBase, self).create(values)
        self.after_save(values)
        return result

    @api.multi
    def write(self, values):
        if self.bill_state != 1 and not self._is_bill_state_change(values):
            raise ValidationError('只有未审核单据才能编辑.')
        self.before_save(values)
        result = super(BillBase, self).write(values)
        self.after_save(values)
        return result

    def get_ignore_fields_when_cannot_save(self):
        return ignore_fields_when_cannot_save

    def _is_bill_state_change(self, values):
        ignore_fields = self.get_ignore_fields_when_cannot_save()
        if len(values) > len(ignore_fields):
            return False
        for f in values:
            if f not in ignore_fields:
                return False
        return True

    def check(self):
        self.check_access_rights('check')
        self.before_check()
        self.do_check()
        self.after_check()

    def before_check(self):
        if self.bill_state != 1:
            raise ValidationError(u'单据状态已发生改变，请重新打开')
        return

    def after_check(self):
        self.check_uid = self._uid
        self.bill_state = 10
        return

    @api.multi
    def do_check(self):
        return

    def finish(self):
        self.check_access_rights('finish')
        self.before_finish()
        self.do_finish()
        self.after_finish()
        return

    def before_finish(self):
        if self.bill_state != 10:
            raise ValidationError(u'单据状态已发生改变，请重新打开')
        return

    def after_finish(self):
        self.bill_state = 20
        return

    @api.multi
    def do_finish(self):
        return

    def un_finish(self):
        self.check_access_rights('unfinish')
        self.before_un_finish()
        self.do_un_finish()
        self.after_un_finish()
        return

    def before_un_finish(self):
        if self.bill_state != 20:
            raise ValidationError(u'单据状态已发生改变，请重新打开')
        return

    def after_un_finish(self):
        self.bill_state = 10
        return

    @api.multi
    def do_un_finish(self):
        return

    def un_check(self):
        self.check_access_rights('uncheck')
        self.before_un_check()
        self.do_un_check()
        self.after_un_check()
        return

    def before_un_check(self):
        if self.bill_state != 10:
            raise ValidationError(u'单据状态已发生改变，请重新打开')
        return

    def after_un_check(self):
        self.check_uid = False
        self.bill_state = 1
        return

    @api.multi
    def do_un_check(self):
        return

    def _compute_check(self):
        self.can_check = self.check_access_rights('check', False)

    def _compute_uncheck(self):
        self.can_uncheck = self.check_access_rights('uncheck', False)

    def _compute_finish(self):
        self.can_finish = self.check_access_rights('finish', False)

    def _compute_unfinish(self):
        self.can_unfinish = self.check_access_rights('unfinish', False)


class Bill(BillBase):
    _auto = True  # automatically create database backend
    _register = False  # not visible in ORM registry, meant to be python-inherited only
    _abstract = False  # not abstract
    _transient = False  # transient
