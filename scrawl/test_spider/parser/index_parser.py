# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 10:38
# @Author  : ChrisPeng
# @File    : index_parser.py
# @Software: PyCharm

import logging

from .info_parser import InfoParser
from .parser import Parser
from .util import handle_html, string_to_int

logger = logging.getLogger('spider.index_parser')

class IndexParser(Parser):
    def __init__(self, cookie, user_uri):
        self.cookie = cookie#cookie
        self.user_uri = user_uri
        self.url = 'https://weibo.cn/%s' % (user_uri)#网址
        self.selector = handle_html(self.cookie, self.url)

    def _get_user_id(self):
        """获取用户id，使用者输入的user_id不一定是正确的，可能是个性域名等，需要获取真正的user_id"""
        user_id = self.user_uri
        url_list = self.selector.xpath("//div[@class='u']//a")
        for url in url_list:
            if (url.xpath('string(.)')) == u'资料':
                if url.xpath('@href') and url.xpath('@href')[0].endswith(
                        '/info'):
                    link = url.xpath('@href')[0]
                    user_id = link[1:-5]
                    break
        return user_id

    def get_page_num(self):
        """获取微博总页数"""
        try:
            if self.selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(self.selector.xpath("//input[@name='mp']")
                                 [0].attrib['value'])
            return page_num
        except Exception as e:
            logger.exception(e)

