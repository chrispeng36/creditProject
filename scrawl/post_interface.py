# -*- coding: utf-8 -*-
# @Time : 2022/6/14 14:57
# @Author : ChrisPeng
# @FileName: post_interface.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/

from WeiboScrawl import WeiboScrawl

def get_user_post(id):
    weibo = WeiboScrawl()
    weibo_post = weibo.get_user_posts(id)
    print(weibo_post)

get_user_post(6292624763)