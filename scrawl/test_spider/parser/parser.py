# -*- coding: utf-8 -*-
# @Time    : 2022/4/3 20:50
# @Author  : ChrisPeng
# @File    : parser.py
# @Software: PyCharm
class Parser:
    def __init__(self, cookie):
        self.cookie = cookie
        self.url = ''
        self.selector = None