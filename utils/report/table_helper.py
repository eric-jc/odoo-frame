# coding: utf-8
from . import table
from odoo.exceptions import ValidationError


# from itertools import groupby


class TableHelper(object):
    def __init__(self):
        self.table = table.ReportTable()
        self.header = None
        self.header_bg_color = None
        self.details = []
        self.line_below = table.ColumnInfo(is_line_below=True)
        self.none_info = table.ColumnInfo()
        return

    def add_header(self, values, header_bg_color=None):  # 不支持header的列数多余明细的列数的情况
        if not values:
            return
        self.header = values
        self.header_bg_color = header_bg_color
        return

    def add_details(self, details, deep=1):
        if not details or len(details) == 0:
            raise ValidationError(u'details参数不合法')
        if deep < 0 or deep > len(details[0]):
            raise ValidationError(u'deep参数不合法')
        if deep:
            if len(self.details) > 0:
                raise ValidationError(u'明细必须一次性添加')
            # lines = groupby(details, key=lambda x: x[0])
            # for key, group in lines:
            #     if len(group) == 1:
            #         info = [self.line_below for i in range(len(group[0]))]
            #         self.table.add_row(group[0], info)
            #         continue
            #     last_pos = len(group) - 1
            #     for i, d in enumerate(group):
            #         if i == 0:
            #             info = [self.none_info for i in range(len(group[0]))]
            #             self.table.add_row(group[0], info)
            for i in range(deep):
                details = sorted(details, key=lambda x: x[deep - i - 1])
            self._set_empty(details, deep)
        self.details = details
        return

    def _set_empty(self, details, deep):
        last = None
        fm = None
        for data in details:
            if not last:  # 第一次循环
                last = data
                fm = data[0:deep]
                continue
            same_deep = self._get_same_deep(data, fm, deep)
            fm = data[0:deep]
            last = data
            self._set_data(data, same_deep)
        return

    def _get_same_deep(self, data, fm, deep):
        for i in range(deep):
            if data[i] == fm[i]:
                continue
            return i
        return deep

    def _set_data(self, data, same_deep):
        if same_deep == 0:
            return
        for i in range(same_deep):
            data[i] = u''

    def get(self):
        self._add_head()
        self._add_details()
        return self.table.get()

    def _get_first_column_info(self, col_span):
        if self.header_bg_color:
            return table.ColumnInfo(col_span=col_span, bg_color=self.header_bg_color)
        return table.ColumnInfo(is_line_below=True, col_span=col_span)

    def _get_column_info_except_first(self):
        if self.header_bg_color:
            return table.ColumnInfo(bg_color=self.header_bg_color)
        return table.ColumnInfo(is_line_below=True)

    def _add_head(self):
        if not self.header:
            return
        header_info = self._get_column_info_except_first()
        detail_column_count = len(self.details[0]) if self.details and len(self.details) > 0 else -1
        if detail_column_count < 0:  # 没有明细
            info = [self.none_info for i in range(len(self.header))]
        elif len(self.header) >= detail_column_count:
            info = [header_info for i in range(len(self.header))]
        else:
            diff = detail_column_count - len(self.header)
            first_column_info = self._get_first_column_info(diff + 1)
            info = [first_column_info]
            info.extend([header_info for i in range(len(self.header)) if i > 0])
        self.table.add_row(self.header, info)

    def _add_details(self):
        if not self.details or len(self.details) == 0:
            return
        count = len(self.details[0])
        last = None
        line = [self.line_below for i in range(count)]
        none = [self.none_info for i in range(count)]
        for data in self.details:
            if not last:
                last = data
                continue
            if data[0]:
                info = line
            else:
                info = none
            self.table.add_row(last, info)
            last = data
        self.table.add_row(last, none)
        return

# 例子
# from odoo.utils.report import table_helper

# helper = table_helper.TableHelper()
# helper.add_header(['张安军', 3000, 99, 12.34, 5, 6])
# helper.add_details([
#     ['a', 'b', 'c', 1],
#     ['a', 'b', 'c', 2],
#     ['b', 'c', 'd', 3],
#     ['b', 'c', 'e', 4],
#     ['b', 'b', 'c', 5],
#     ['c', 'b', 'c', 6]
# ], 3)
# result2 = helper.get()
