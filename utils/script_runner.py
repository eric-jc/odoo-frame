# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from change_key_helper import ChangeKeyHelper


# 假如设置setting = '''
# a=b*c
# d=b+c
#        '''#其中a、d顶头
# =======则使用方法：========
#        runner = ScriptRunner(self)
#        runner.add_func('b', lambda bill: 40)
#        runner.add_value('c', 30)
#        runner.execute(setting)
#        runner.result['a']
#        runner.result['d']

class ScriptRunner(object):
    def __init__(self, bill):
        self.bill = bill
        self.func_dic = {}
        self.value_dic = {}
        self.keys = []
        self.key_helper = ChangeKeyHelper()
        self.key_helper.add_invalid_keys(['bill', 'func_dic', 'value_dic', 'keys', 'result'])
        self.result = {}
        return

    def _add_param(self, p):
        if p in ['bill', 'func_dic', 'value_dic', 'keys', 'result']:
            raise ValidationError(u'设置错误：参数不允许为' + p)
        param_name = self.key_helper.get_new_key(p)
        setattr(self, param_name, None)
        self.result[p] = None
        return

    def add_func(self, key, func):
        if key in self.keys:
            raise ValidationError(u'开发错误：add_func的key“{}”已存在'.format(key))
        self.keys.append(key)
        self.func_dic[key] = func
        return

    def add_value(self, key, value):
        if key in self.keys:
            raise ValidationError(u'开发错误：add_value的key“{}”已存在'.format(key))
        self.keys.append(key)
        self.value_dic[key] = value
        return

    def execute(self, script):
        params = ScriptRunner._get_params(script)
        for p in params:
            self._add_param(p)
        new_script = self._init_script(script).strip()
        script_list = ScriptRunner._split_scripts(new_script)
        for line in script_list:
            exec 'self.' + line
        self._set_values()
        return

    @staticmethod
    def _get_params(script):
        result = []
        script_list = ScriptRunner._split_scripts(script)
        for s in script_list:
            new_s = s.strip()
            if not new_s:
                continue
            p = new_s.split('=')[0].strip()
            if not p:
                raise ValidationError(u'配置错误：' + s)
            result.append(p)
        return result

    def _init_script(self, script):
        result = script
        self.keys.sort(key=lambda x: len(x), reverse=True)
        for key in self.keys:
            if key not in script:
                continue
            if key in self.value_dic:
                result = result.replace(key, str(self.value_dic[key]))
                continue
            if key in self.func_dic:
                result = result.replace(key, str(self.func_dic[key](self.bill)))
                continue
            raise ValidationError(u'未处理的配置。key：' + key)
        for key in self.result:
            param_name = self.key_helper.safe_get_key(key)
            result = result.replace(key, param_name)
        return result

    @staticmethod
    def _split_scripts(script):
        s = script.strip()
        rows = s.split('\n')
        return [line.strip() for line in rows]

    def _set_values(self):
        for key in self.result:
            param_name = self.key_helper.safe_get_key(key)
            self.result[key] = getattr(self, param_name)
        return
