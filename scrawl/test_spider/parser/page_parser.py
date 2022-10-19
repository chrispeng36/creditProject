# -*- coding: utf-8 -*-
# @Time    : 2022/4/3 21:05
# @Author  : ChrisPeng
# @File    : page_parser.py
# @Software: PyCharm

import logging
import re
import sys
from datetime import datetime, timedelta

from .. import datetime_util
from ..Weibo import Weibo
from .comment_parser import CommentParser
# from .mblog_picAll_parser import MblogPicAllParser
from .parser import Parser
from .util import handle_garbled, handle_html, to_video_download_url

logger = logging.getLogger('spider.page_parser')

class PageParser(Parser):
    empty_count = 0

    def __init__(self, cookie, user_config, page, filter):
        self.cookie = cookie
        if hasattr(PageParser, 'user_uri') and self.user_uri != user_config['user_uri']:
            PageParser.empty_count = 0

        self.user_uri = user_config['user_uri']#用户名
        self.since_date = user_config['since_date']#开始爬虫日期
        self.end_date = user_config['end_date']#结束爬虫日期
        self.page = page#页数
        self.url = 'https://weibo.cn/%s?page=%d' % (self.user_uri, page)
        if self.end_date != 'now':
            since_date = self.since_date.split(' ')[0].split('-')
            end_date = self.end_date.split(' ')[0].split('-')
            for date in [since_date, end_date]:
                for i in [1, 2]:
                    if len(date[i]) == 1:
                        date[i] = '0' + date[i]
            starttime = ''.join(since_date)
            endtime = ''.join(end_date)
            self.url = 'https://weibo.cn/%s/profile?starttime=%s&endtime=%s&advancedfilter=1&page=%d' % (
                self.user_uri, starttime, endtime, page)
        self.selector = ''
        self.to_continue = True
        is_exist = ''
        for i in range(3):
            self.selector = handle_html(self.cookie, self.url)
            info = self.selector.xpath("//div[@class='c']")
            is_exist = info[0].xpath("div/span[@class='ctt']")
            if is_exist:
                PageParser.empty_count = 0
                break
        if not is_exist:
            PageParser.empty_count += 1
        if PageParser.empty_count > 2:
            self.to_continue = False
            PageParser.empty_count = 0
        self.filter = filter

    def get_one_page(self, weibo_id_list):
        """获取第page页的全部微博
        这里get_one_weibo返回的是个结构体了，所以可以根据需要获取
        """
        try:
            info = self.selector.xpath("//div[@class='c']")
            # print(info)
            is_exist = info[0].xpath("div/span[@class='ctt']")
            weibos = {}#此处改为dict存储，
            original_post = ''
            re_post = ''
            '''
               原创微博：
               转发微博：
            '''
            if is_exist:
                since_date = datetime_util.str_to_time(self.since_date)#将日期转换为数字
                for i in range(0, len(info) - 1):#微博的页数
                    weibo = self.get_one_weibo(info[i])#对每一页获取每一条微博
                    original_post += weibo.original_post
                    re_post += weibo.repost
                    if weibo:
                        if weibo.id in weibo_id_list:
                            continue
                        publish_time = datetime_util.str_to_time(
                            weibo.publish_time)

                        if publish_time < since_date:
                            if self.is_pinned_weibo(info[i]):#置顶微博的话还是要爬取
                                continue
                            else:#超过了时间就返回
                                return weibos, weibo_id_list, False
                        # logger.info(weibo)#日志打印微博信息
                        logger.info('-' * 100)
                        weibo_id_list.append(weibo.id)#将爬取的微博id加入list
                weibos.update({"原创微博":original_post})
                weibos.update({"转发微博":re_post})
                # print(weibos)
            return weibos, weibo_id_list, self.to_continue
        except Exception as e:
            logger.exception(e)

    def is_original(self, info):
        '''判断是否为原创微博'''
        is_original = info.xpath("div/span[@class='cmt']")
        if len(is_original) > 3:
            return False
        else:
            return True

    def get_original_weibo(self, info, weibo_id):
        """获取原创微博"""
        try:
            weibo_content = handle_garbled(info)
            weibo_content = weibo_content[:weibo_content.rfind(u'赞')]
            a_text = info.xpath('div//a/text()')
            if u'全文' in a_text:
                wb_content = CommentParser(self.cookie,
                                           weibo_id).get_long_weibo()
                if wb_content:
                    weibo_content = wb_content
            return weibo_content
        except Exception as e:
            logger.exception(e)

    def get_retweet(self, info, weibo_id):
        """获取转发微博"""
        try:
            weibo_content = handle_garbled(info)
            weibo_content = weibo_content[weibo_content.find(':') +
                                          1:weibo_content.rfind(u'赞')]
            weibo_content = weibo_content[:weibo_content.rfind(u'赞')]
            a_text = info.xpath('div//a/text()')
            if u'全文' in a_text:
                wb_content = CommentParser(self.cookie,
                                           weibo_id).get_long_retweet()
                if wb_content:
                    weibo_content = wb_content
            retweet_reason = handle_garbled(info.xpath('div')[-1])
            retweet_reason = retweet_reason[:retweet_reason.rindex(u'赞')]
            # original_user = info.xpath("div/span[@class='cmt']/a/text()")
            # if original_user:#是原始用户的话
            #     original_user = original_user[0]#获取原始用户
            #     weibo_content = (retweet_reason + '\n' + u'原始用户: ' +
            #                      original_user + '\n' + u'转发内容: ' +
            #                      weibo_content)
            # else:
            #     weibo_content = (retweet_reason + '\n' + u'转发内容: ' +
            #                      weibo_content)
            '''不需要那么麻烦的区分转发内容和转发原因，直接全部打包'''
            weibo_content = retweet_reason + weibo_content
            return weibo_content
        except Exception as e:
            logger.exception(e)

    # def get_weibo_content(self, info, is_original):
    #     """获取微博内容"""
    #     try:
    #         weibo_id = info.xpath('@id')[0][2:]
    #         if is_original:
    #             weibo_content = self.get_original_weibo(info, weibo_id)
    #         else:
    #             weibo_content = self.get_retweet(info, weibo_id)
    #         return weibo_content
    #     except Exception as e:
    #         logger.exception(e)

    def get_one_weibo(self, info):
        '''获取一条微博的全部信息

        '''
        try:
            weibo = Weibo()#微博结构体
            is_original = self.is_original(info)
            weibo.original = is_original#是否为原创微博
            '''分别存储原创微博和转发微博'''
            weibo.repost = ''  # 此时是原创微博
            weibo.original_post = ''
            if (not self.filter) and is_original:
                try:
                    weibo.id = info.xpath('@id')[0][2:]#获取微博的id
                    weibo.original_post += self.get_original_weibo(info, weibo.id)#原创的微博
                    weibo.publish_time = self.get_publish_time(info)

                except Exception as e:
                    logger.exception(e)
            elif (not self.filter) and (not is_original):#转发微博
                try:
                    weibo.id = info.xpath('@id')[0][2]
                    weibo.repost += self.get_retweet(info, weibo.id)
                    weibo.publish_time = self.get_publish_time(info)

                except Exception as e:
                    logger.exception(e)
            else:
                weibo = None
                logger.info(u"这条微博未提取")
            return weibo
        except Exception as e:
            logger.exception(e)

    def get_publish_time(self, info):
        """获取微博发布时间"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = handle_garbled(str_time[0])
            publish_time = str_time.split(u'来自')[0]
            if u'刚刚' in publish_time:
                publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            elif u'分钟' in publish_time:
                minute = publish_time[:publish_time.find(u'分钟')]
                minute = timedelta(minutes=int(minute))
                publish_time = (datetime.now() -
                                minute).strftime('%Y-%m-%d %H:%M')
            elif u'今天' in publish_time:
                today = datetime.now().strftime('%Y-%m-%d')
                time = publish_time[3:]
                publish_time = today + ' ' + time
                if len(publish_time) > 16:
                    publish_time = publish_time[:16]
            elif u'月' in publish_time:
                year = datetime.now().strftime('%Y')
                month = publish_time[0:2]
                day = publish_time[3:5]
                time = publish_time[7:12]
                publish_time = year + '-' + month + '-' + day + ' ' + time
            else:
                publish_time = publish_time[:16]
            return publish_time
        except Exception as e:
            logger.exception(e)

    def is_pinned_weibo(self, info):
        '''判断是否为置顶微博'''
        kt = info.xpath(".//span[@class='kt']/text()")
        if kt and kt[0] == u'置顶':
            return True
        else:
            return False
