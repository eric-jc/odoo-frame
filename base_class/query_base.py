# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.utils import util

KAN_BAN = 'kanban'
TREE = 'tree'
PIVOT = 'pivot'


class QueryBase(models.Model):
    _auto = False
    _abstract = True
    _transient = False
    _register = False

    # sql相关：查询、查询结果
    _query_table = None  # 要查询的表
    _query_fields_sum = []  # 合计字段
    _query_fields_expression_dic = {}  # 其他计算字段（非合计、非分组字段）。key：字段；value：表达式
    _query_where_equal_fields = []  # 相等条件的字段
    _query_where_like_fields = []  # ilike条件的字段
    _query_where_fields_and_condition_dic = {}  # 非相等、非ilike条件字段。key：字段；value：条件表达式（例如date<value，其中，value会被替换为条件的值）
    _insert_model = None
    _insert_fields_compute = {}  # 非查询字段。key:字段；value：func（参数为查询出来的数据行row，返回结果为要插入到数据库中的值）

    # 查询结果相关
    _show_xmlid_action = None
    _show_xmlid_kanban = ''
    _show_xmlid_tree = ''
    _show_xmlid_pivot = ''
    _show_order = [TREE, KAN_BAN, PIVOT]  # 所有的显示顺序，添加到这里。使用时，在子类中，选择需要的，并排序

    _ignore_fields = ['id', 'create_date', 'write_date', 'create_uid', 'write_uid', 'display_name', 'current_user_id']

    # 数据授权表达式。例如：[self.env['archives.organization'].get_customer_organization_condition_staff('staff_id')]
    def get_organizations(self):
        raise ValidationError(u'开发错误：请重写方法：get_organizations')

    def _get_default_date_from(self):
        date = fields.Date.from_string(fields.Date.context_today(self))
        year = date.strftime('%Y')
        month = date.strftime('%m')
        return '{}-{}-01'.format(year, month)

    current_user_id = fields.Many2one('res.users')

    @api.onchange('current_user_id')
    def _onchange_for_money(self):
        self._reload()

    def _reload(self):
        if not self.current_user_id:
            return
        dmo = self.search([('create_uid', '=', self._uid)], limit=1, order='id desc')
        if not dmo:
            return
        for f in self._fields:
            if f in self._ignore_fields:
                continue
            # self.date_start = dmo.date_start
            v = getattr(dmo, f)
            setattr(self, f, v)

    def _copy_show_fields_to(self, wizard):
        # wizard.s_month = self.s_month
        for f in self._fields:
            if f in self._ignore_fields:
                continue
            if not f.startswith('s_'):
                continue
            v = getattr(self, f)
            setattr(wizard, f, v)

    def clear_condition(self):
        wizard = self.create({})
        self._copy_show_fields_to(wizard)
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wizard.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    @api.multi
    def query(self):
        if not self._query_table:
            raise ValidationError(u'开发错误：请给_query_table赋值')
        if not self._insert_model:
            raise ValidationError(u'开发错误：请给_insert_table赋值')
        if not self._show_xmlid_action:
            raise ValidationError(u'开发错误：请给_show_xmlid_action赋值')
        show_fields = self._get_show_fields()
        data = self._query_data(show_fields)
        self.clear_data()
        self.insert_data(data, show_fields)
        return self.open_result(show_fields)

    def _get_show_fields(self):  # 所有显示字段
        show_fields = []
        # if self.s_month:
        #     show_fields.append('month')
        for f in self._fields:
            if f in self._ignore_fields:
                continue
            if not f.startswith('s_'):
                continue
            v = getattr(self, f)
            if v:
                show_fields.append(f[2:])

        if not show_fields:
            raise ValidationError('请选择显示字段')
        return show_fields

    def _query_data(self, show_fields):
        sql = self.get_sql(show_fields)
        self.env.cr.execute(sql)
        return self.env.cr.fetchall()

    def get_sql(self, show_fields):
        select_and_group = self._get_select_and_group(show_fields)
        condition = self.get_condition()
        sql = u'SELECT {} ' \
              u'FROM {} ' \
              u'{} '. \
            format(select_and_group[0], self._query_table.replace('.', '_'), condition)
        if select_and_group[1]:
            sql += u' group by ' + select_and_group[1]
        return sql

    def _get_select_and_group(self, show_fields):
        arr = []
        group_arr = []
        for f in show_fields:
            if f in self._query_fields_sum:
                arr.append('sum({})'.format(f))
            elif f in self._query_fields_expression_dic:
                arr.append(self._query_fields_expression_dic[f])
            else:
                arr.append(f)
                group_arr.append(f)
        return ','.join(arr), ','.join(group_arr)

    def get_condition(self):
        a = self._get_condition_from_select()
        _query_where_fields_organization = [o for o in self.get_organizations() if o]
        if not _query_where_fields_organization:
            return a
        if not a:
            a = u'where '
        if len(_query_where_fields_organization) == 1:
            return a + u' and ' + _query_where_fields_organization[0]
        return a + u' and '.join(_query_where_fields_organization)
        # cs = '' if self.customer_id else self.env[
        #     'archives.organization'].get_customer_organization_condition_staff('staff_id')
        # co = '' if self.customer_id else self.env[
        #     'archives.organization'].get_customer_organization_condition_organization('customer_organization_id')
        # gt = '' if self.goods_id else self.env[
        #     'archives.organization'].get_goods_organization_condition_goods_type('goods_type_id')
        # go = '' if self.goods_id else self.env[
        #     'archives.organization'].get_goods_organization_condition_organization('goods_organization_id')

    def _get_condition_from_select(self):
        # 'boolean'
        # 'char'
        # 'selection'
        # 'many2one'
        # 'date'
        condition_list = []
        for f in self._fields:
            if f in self._ignore_fields:
                continue
            if f.startswith('s_'):
                continue
            v = getattr(self, f)
            if not v:
                continue
            if not util.is_string(v):
                v = str(v.id) if self._fields[f].type == 'many2one' else str(v)
            if f in self._query_where_equal_fields:
                condition_list.append(f + ' = ' + v)
            elif f in self._query_where_like_fields:
                condition_list.append(f + u" ilike '%" + v + u"%'")
            elif f in self._query_where_fields_and_condition_dic:
                c = self._query_where_fields_and_condition_dic[f].replace('value', v)
                condition_list.append(c)
        if condition_list:
            return u'where ' + u' and '.join(condition_list)
        return ''

        # if self.zone_id:
        #     condition += self.get_and(condition)
        #     condition += 'zone_id = ' + str(self.zone_id.id)
        # if self.date_start:
        #     condition += self.get_and(condition)
        #     condition += "date >= '" + str(self.date_start) + "'"
        # if self.date_end:
        #     condition += self.get_and(condition)
        #     condition += "date <= '" + str(self.date_end) + "'"
        # if self.remark:
        #     condition += self.get_and(condition)
        #     condition += u"remark ilike '%" + self.remark + u"%'"

    #
    # def get_and(self, v):
    #     if len(v) > 6:
    #         return ' and '
    #     return ''

    def clear_data(self):
        sql = 'DELETE FROM {} WHERE create_uid = {}'.format(self._insert_model.replace('.', '_'), self._uid)
        self.env.cr.execute(sql)

    def insert_data(self, data, show_fields):
        for row in data:
            dic = self._get_values_dic(row, show_fields)
            dic['create_uid'] = str(self._uid)
            self.env[self._insert_model].create(dic)
        return

    def _get_values_dic(self, row, show_fields):
        dic = {}
        index = 0
        for f in show_fields:
            dic[f] = row[index]
            index += 1
        if self._insert_fields_compute:
            for key, func in self._insert_fields_compute:
                v = func(row)
                dic[f] = v
        return dic

    def open_result(self, show_fields):
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object(self._show_xmlid_action)
        list_view_id = imd.xmlid_to_res_id(self._show_xmlid_tree) if self._show_xmlid_tree else ''
        kan_ban_view_id = imd.xmlid_to_res_id(self._show_xmlid_kanban) if self._show_xmlid_kanban else ''
        pivot_view_id = imd.xmlid_to_res_id(self._show_xmlid_pivot) if self._show_xmlid_pivot else ''
        views = []
        for t in self._show_order:
            if t == TREE and list_view_id:
                views.append([list_view_id, TREE])
            elif t == KAN_BAN and kan_ban_view_id:
                views.append([kan_ban_view_id, KAN_BAN])
            elif t == PIVOT and pivot_view_id:
                views.append([pivot_view_id, PIVOT])

        context = QueryBase._get_context(show_fields)
        domain = [('create_uid', '=', self._uid)]

        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            # 'views': [[list_view_id, 'tree'], [form_view_id, 'form']],
            'views': views,
            'target': action.target,
            # 'context': action.context,
            # 'context': {
            #     'create_uid': self.env.uid,
            # },
            'context': context,
            'res_model': action.res_model,
            'domain': domain,
        }

    @staticmethod
    def _get_context(show_fields):
        context = {}
        for f in show_fields:
            context[f] = 1
        return context


class TransientQuery(QueryBase):
    _auto = True  # automatically create database backend
    _register = False  # not visible in ORM registry, meant to be python-inherited only
    _abstract = False  # not abstract
    _transient = True  # transient
