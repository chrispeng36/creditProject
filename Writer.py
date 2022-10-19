# -*- coding: utf-8 -*-
# @Time : 2022/6/13 16:20
# @Author : ChrisPeng
# @FileName: Writer.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/

import MySQLdb
import logging

from scrawl.WeiboScrawl import WeiboScrawl

class Writer(object):
    def __init__(self):
        self.MYSQL_HOST = "localhost"
        self.MYSQL_USERNAME = "root"
        self.MYSQL_PASSWORD = "123"
        self.MYSQL_DATABASE = "data11"
        self.db = MySQLdb.connect(self.MYSQL_HOST, self.MYSQL_USERNAME, self.MYSQL_PASSWORD, self.MYSQL_DATABASE, charset='utf8')
        self.cursor = self.db.cursor()  # 数据库的游标

    def write_wangyi_following(self, WY_followers):
        '''
        将WY的关注者写入数据库中
        :param WY_followers: {用户：[粉丝列表]}，或者{用户：[关注列表]}
        :return:
        '''
        followers = list(WY_followers.values())[0]
        user_id = 1269643340
        index = 0

        for user in followers:
            follow_name = list(user.keys())[0]
            follow_id = list(user.values())[0]
            temp_sql = "insert into 网易云关注列表新增 (`序号`,`关注用户`,`关注ID`,`用户ID`) VALUES ({},{},{},{});".format(
                index,"'{}'".format(follow_name),int(follow_id),user_id)
            self.cursor.execute(temp_sql)

        # sqlStr = "insert into test (id,`name`) VALUES ('2','chshiufs');"
        # cursor.execute(sqlStr)
        self.db.commit()
        logging.info("网易云关注者写入数据库完毕！！！")

    def write_wangyi_fans(self, WY_fans):
        '''

        :param WY_fans:
        :return: {用户：[粉丝列表]}，或者{用户：[关注列表]}
        '''
        fans = list(WY_fans.values())[0]
        user_id = 1269643340
        index = 0
        for user in fans:
            fan_name = list(user.keys())[0]
            fan_id = list(user.values())[0]
            temp_sql = "insert into 网易云粉丝列表新增 (`index`,`name`,`粉丝ID`,`用户ID`) VALUES ({},{},{},{});".format(
                index,"'{}'".format(fan_name),int(fan_id),user_id)
            self.cursor.execute(temp_sql)

        self.db.commit()
        logging.info("网易云粉丝写入数据库完毕！！！")

    def write_wangyi_attributes(self, WY_user_attributes):
        '''

        :param WY_user_attributes: user_name：用户名
                user_rank: 用户等级
                user_sex: 用户性别
                user_event: 用户动态数
                user_follow: 用户关注人数
                user_fans: 用户粉丝数
                user_intro: 用户个人介绍
                user_loc: 用户所在地
                user_age: 用户年龄
                weibo_link: 微博链接
        :return:
        '''
        index = 0 #待修改
        user_name = WY_user_attributes['user_name']
        user_rank = WY_user_attributes['user_rank']
        user_sex = WY_user_attributes['user_sex']
        user_event = WY_user_attributes['user_event']
        user_follow = WY_user_attributes['user_follow']
        user_fans = WY_user_attributes['user_fans']
        user_intro = WY_user_attributes['user_intro']
        user_loc = WY_user_attributes['user_loc']
        user_age = WY_user_attributes['user_age']
        weibo_id = WY_user_attributes['weibo_id']
        sqlStr = "insert into 网易云用户属性信息新增 " \
                 "(`序号`,`网易云用户名`,`网易云等级`,`网易云动态数`,`网易云关注人数`," \
                 "`网易云粉丝数`,`网易云个人简介`,`所在地区`,`用户性别`,`用户年龄`,`微博链接`) values (" \
                 "{},{},{},{},{},{},{},{},{},{},{});".format(
            index,"'{}'".format(user_name),int(user_rank),int(user_event),int(user_follow),
            int(user_fans),"'{}'".format(user_intro),"'{}'".format(user_loc),"'{}'".format(user_sex),"'{}'".format(user_age),int(weibo_id)
        )

        self.cursor.execute(sqlStr)
        self.db.commit()
        logging.info("网易云属性信息写入数据库完毕！！！")

    def write_wangyi_posts(self, WY_posts):
        '''

        :param WY_posts: str的发帖记录，一整个句子
        :return:
        '''
        index = 0
        name = 'hgfuiw' #后面放在init方法里面
        sqlStr = "insert into 网易云用户发帖新增 (`序号`,`网易云用户名`,`网易云发帖`) values (" \
                 "{},{},{});".format(index, "'{}'".format(name), "'{}'".format(WY_posts))
        self.cursor.execute(sqlStr)
        self.db.commit()
        logging.info("网易云发帖写入数据完毕！！！")

    def write_weibo_following(self,WB_follow):
        '''

        :param WB_fans: {用户：[粉丝列表]}，或者{用户：[关注列表]}
        :return:
        '''
        index = 0
        user_id = int(list(WB_follow.keys())[0])
        follows = list(WB_follow.values())[0]
        for user in follows:
            follow_name = user['name']
            follow_id = int(user['id'])
            temp_sql = "insert into 微博关注列表新增 (`序号`,`name`,`用户ID`,`关注ID`) values (" \
                       "{},{},{},{});".format(index, "'{}'".format(follow_name),user_id, follow_id)
            self.cursor.execute(temp_sql)
        self.db.commit()
        logging.info("微博关注用户写入完毕！！！")

    def write_weibo_fans(self,WB_fans):
        '''

        :param WB_fans: {用户：[粉丝列表]}，或者{用户：[关注列表]}
        :return:
        '''
        index = 0
        user_id = int(list(WB_fans.keys())[0])
        fans = list(WB_fans.values())[0]
        for user in fans:
            fan_name = user['name']
            fan_id = int(user['id'])
            temp_sql = "insert into 微博粉丝列表新增 (`序号`,`name`,`用户ID`,`粉丝ID`) values (" \
                       "{},{},{},{});".format(index, "'{}'".format(fan_name),user_id, fan_id)
            self.cursor.execute(temp_sql)
        self.db.commit()
        logging.info("微博关注用户写入完毕！！！")

    def write_weibo_posts(self,WB_id):
        '''
        这里由于不好改程序，所以直接按照爬虫代码中进行存储
        :param WB_id:
        :return:
        '''
        weiboScrawl = WeiboScrawl()
        weiboScrawl.get_user_posts(WB_id)

    def write_weibo_attributes(self, WB_attributes):
        '''

        :param WB_attributes:
        :return:
        '''
        index = 0
        attributes = list(WB_attributes.values())[0]
        user_id = int(list(WB_attributes.keys())[0])
        user_name = attributes[0]['user_name']
        user_sex = attributes[1]['user_sex']
        user_rank = attributes[2]['user_rank']
        user_fans_count = attributes[3]['user_fans_count']
        user_following_count = attributes[4]['user_following_count']
        user_authority = attributes[5]['user_authority']
        user_intro = attributes[6]['user_intro']
        user_credit = attributes[7]['user_credit']
        user_loc = attributes[8]['user_loc']
        user_edu = attributes[9]['user_edu']
        join_time = attributes[10]['join_time']
        birth_day = attributes[11]['birth_day']

        sqlStr = "insert into 微博用户信息新增 (`序号`,`用户ID`,`用户名`,`粉丝数`,`关注人数`,`性别`,`用户等级`,`用户简介`,`用户认证`,`加入日期`,`生日`,`信用等级`,`教育信息`,`用户所在地`) " \
                 "values ({},{},{},{},{},{},{},{},{},{},{},{},{},{});".format(
            index, int(user_id), "'{}'".format(user_name), "'{}'".format(user_fans_count), "'{}'".format(user_following_count),
            "'{}'".format(user_sex),"'{}'".format(user_rank),"'{}'".format(user_intro),"'{}'".format(user_authority),
            "'{}'".format(join_time),"'{}'".format(birth_day),"'{}'".format(user_credit),"'{}'".format(user_edu),"'{}'".format(user_loc)
        )

        self.cursor.execute(sqlStr)
        self.db.commit()
        logging.info("微博属性信息写入完毕！！！")

    def shutdown(self):
        self.db.close()

