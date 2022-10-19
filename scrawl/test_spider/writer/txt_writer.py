# -*- coding: utf-8 -*-
# @Time    : 2022/4/3 22:00
# @Author  : ChrisPeng
# @File    : txt_writer.py
# @Software: PyCharm

import logging
import sys

from .writer import Writer

logger = logging.getLogger('spider.txt_writer')

class TXTWriter(Writer):
    def __init__(self, file_path, filter):
        self.file_path = file_path
        self.original_post_header = u'原创微博内容'
        self.repost_header = u'转发微博内容'


    def writer_weibo(self, weibo):
        '''将爬取到的微博存入到txt文件'''

        original_weibo_header = ''
        repost_weibo_header = ''
        '''舍弃了判断是否为原创微博的内容'''
        if self.original_post_header:
            original_weibo_header = self.original_post_header + ': \n'
            self.original_post_header = ''
        if self.repost_header:
            repost_weibo_header = self.repost_header + ': \n'

        try:
            temp_result = []
            temp_result.append(weibo.original_post)
            temp_result.append(weibo.repost)

            with open(self.file_path, 'ab') as f:
                f.write((original_weibo_header + temp_result[0]).encode(sys.stdout.encoding))
                f.write((repost_weibo_header + temp_result[1]).encode(sys.stdout.encoding))

            logger.info(u'%d条微博写入txt文件完毕，保存路径：%s', len(weibo), self.file_path)

        except Exception as e:
            logger.exception(e)