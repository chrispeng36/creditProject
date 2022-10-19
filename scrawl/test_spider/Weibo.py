# -*- coding: utf-8 -*-
# @Time    : 2022/4/3 20:28
# @Author  : ChrisPeng
# @File    : Weibo.py
# @Software: PyCharm

'''微博数据结构'''
class Weibo:
    def __init__(self):
        self.id = ''  # 用户id
        self.original_post = ''  # 用户发帖
        self.repost = ''  # 用户转发
        self.original = None
        self.publish_time = ''

    def __str__(self):
        '''打印一条微博'''
        result = u"原创微博：%s\n" % self.original_post
        result += u"转发微博：%s\n" % self.repost
        # result += u'发布时间：%s\n' % self.publish_time
        return result




