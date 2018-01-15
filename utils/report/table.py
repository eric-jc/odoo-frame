# coding: utf-8
from . import row, column


class ReportTable(object):
    def __init__(self):
        self._all_data = []

    def add_row(self, row_data, data_info=None):
        self._all_data.append((row_data, data_info))

    def get(self):
        fm = ''' '
<table class="table wq-table" style="margin-bottom:0px">
<tbody>
    {}
</tbody>
</table>
    ' '''
        last_pos = len(self._all_data) - 1
        s = ''
        for i, row_pair in enumerate(self._all_data):
            r = row.ReportRow()
            if i < last_pos:
                ReportTable._add_row(i, row_pair, r)
            else:
                ReportTable._add_row(i, row_pair, r, is_last_row=True)
            s += r.get()

        return fm.format(s)

    @staticmethod
    def _add_row(row_index, row_pair, report_row, is_last_row=False):
        last_pos = len(row_pair[1]) - 1
        for i, d in enumerate(row_pair[0]):
            column_info = row_pair[1][i] if i <= last_pos else None
            ReportTable._add_column(d, report_row, row_index, is_last_row, column_info)

    @staticmethod
    def _add_column(d, report_row, row_index, is_last_row=False, column_info=None):
        c = column.ReportColumn()
        report_row.add_column(c)
        c.add_value(d)
        c.add_column_info(column_info)


class ColumnInfo(object):  # bg_color:True 或 颜色代码
    def __init__(self, is_line_below=False, is_line_before=False, bg_color=None, other_style=None,  # style
                 row_span=None, col_span=None, other_info=None):  # other
        self.is_line_below = is_line_below
        self.is_line_before = is_line_before
        self.bg_color = bg_color
        self.other_style = other_style
        self.row_span = row_span
        self.col_span = col_span
        self.other_info = other_info

    def __str__(self):
        style = ''
        if not self.is_line_before:
            style += 'border-top:none;'
        if self.is_line_below:
            style += 'border-bottom: 1px solid gray;'
        if self.bg_color:
            style += 'background-color:{};'.format(self.bg_color) if ColumnInfo._is_string(
                self.bg_color) else 'background-color:#C0C0C0;'
        if self.other_style:
            style += self.other_style
        result = ' style="{}"'.format(style) if style else ''
        if self.col_span:
            result += ' colspan="{}"'.format(self.col_span)
        if self.row_span:
            result += ' rowspan="{}"'.format(self.row_span)
        if self.other_info:
            result += ' ' + self.other_info
        return result

    @staticmethod
    def _is_string(s):
        return isinstance(s, basestring)

    __repr__ = __str__


    # 例子：
    # line_below = report.table.column.ColumnInfo(is_line_below=True)
    # none_info = report.table.column.ColumnInfo()
    # color_info = report.table.column.ColumnInfo(bg_color=True)
    # color_info2 = report.table.column.ColumnInfo(bg_color='blue')
    # t = report.table.ReportTable()
    # t.add_row(['张安军', 3000, 200.23, 9999], [line_below, line_below, line_below, line_below])
    # t.add_row(['a', 'b', 'c'], [none_info, none_info, none_info])
    # t.add_row(['a2', 'b2', 'c2'], [line_below, line_below, line_below])
    # t.add_row(['a3', 'b3', 'c3'], [color_info, color_info, color_info])
    # t.add_row(['a4', 'b4', 'c4'], [none_info, none_info, none_info])
    # t.add_row(['a5', 'b5', 'c5'], [color_info2, color_info2, color_info2])
    # return t.get()

    # 例子2：
    # line_below = report.table.column.ColumnInfo(is_line_below=True)
    # none_info = report.table.column.ColumnInfo()
    # col_span_2 = report.table.column.ColumnInfo(col_span=2)
    # color_info = report.table.column.ColumnInfo(bg_color=True)
    # color_info2 = report.table.column.ColumnInfo(bg_color='blue')
    # t = report.table.ReportTable()
    # t.add_row(['张安军', 3000, 200.23, 9999], [line_below, line_below, line_below, line_below])
    # t.add_row(['a', 'b', 'c'], [col_span_2, none_info, none_info])
    # t.add_row(['', 'a2', 'b2', 'c2'], [line_below, line_below, line_below, line_below])
    # t.add_row(['a3', 'b3', 'c3'], [col_span_2, color_info, color_info])
    # t.add_row(['', 'a4', 'b4', 'c4'], [none_info, none_info, none_info, none_info])
    # t.add_row(['', 'a5', 'b5', 'c5'], [color_info2, color_info2, color_info2, color_info2])
    # return t.get()
