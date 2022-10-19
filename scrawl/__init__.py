# -*- coding: utf-8 -*-
# @Time : 2022/4/5 4:13
# @Author : ChrisPeng
# @FileName: __init__.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/

from WeiboScrawl import WeiboScrawl
from WangyiyunScrawl import WangyiyunScrawl
from test_spider import spider
__all__ = [WeiboScrawl, WangyiyunScrawl,spider]