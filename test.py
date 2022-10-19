# -*- coding: utf-8 -*-
# @Time : 2022/6/14 14:23
# @Author : ChrisPeng
# @FileName: test.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/


from scrawl.WeiboScrawl import WeiboScrawl
weibo = WeiboScrawl()
weibo = weibo.get_user_posts(6307242122)

print(weibo)