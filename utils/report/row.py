# coding: utf-8

from enum import Enum, unique


class ReportRow(object):
    # fm = '''<tr>
    #     <td style="border-bottom: 1px solid gray;border-top:none;">a</td>
    #     <td style="border-bottom: 1px solid gray;border-top:none;">b</td>
    # </tr>'''

    def __init__(self):
        self._report_columns = []

    def add_column(self, report_column):
        self._report_columns.extend([report_column])

    def add_columns(self, report_columns):
        self._report_columns.extend(report_columns)

    def get(self):
        fm = '''<tr>
        {}</tr>'''
        cs = ''
        for c in self._report_columns:
            cs += c.get() + '''
            '''
        return fm.format(cs)
