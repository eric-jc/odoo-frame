# -*- coding: utf-8 -*-

import re


# 判断是否合法车牌号
def is_car_no(car_no):
    if not car_no:
        return False

    # 匹配民用车牌和使馆车牌
    # 判断标准
    # 1，第一位为汉字省份缩写
    # 2，第二位为大写字母城市编码
    # 3，后面是5位仅含字母和数字的组合
    regular = u'^[京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云渝藏陕甘青宁新使]{1}[A-Za-z]{1}[0-9a-zA-Z]{5}$'
    pattern = re.compile(regular)
    if pattern.match(car_no):
        return True

    # 匹配特种车牌(挂,警,学,领,港,澳)
    # 参考 https://wenku.baidu.com/view/4573909a964bcf84b9d57bc5.html
    regular = u'^[京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云渝藏陕甘青宁新]{1}[A-Za-z]{1}[0-9a-zA-Z]{4}[挂警学领港澳]{1}$'
    pattern = re.compile(regular)
    if pattern.match(car_no):
        return True

    # 匹配武警车牌
    # 参考 https://wenku.baidu.com/view/7fe0b333aaea998fcc220e48.html
    regular = u'^WJ[京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云渝藏陕甘青宁新]?[0-9a-zA-Z]{5}$'
    pattern = re.compile(regular)
    if pattern.match(car_no):
        return True

    # 匹配军牌
    # 参考 http://auto.sina.com.cn/service/2013-05-03/18111149551.shtml
    regular = u'^[A-Za-z]{2}[0-9]{5}$'
    pattern = re.compile(regular)
    if pattern.match(car_no):
        return True

    return False
