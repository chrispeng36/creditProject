# -*- coding: utf-8 -*-
# @Time : 2022/10/20 13:42
# @Author : ChrisPeng
# @FileName: run.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/
from WangyiyunScrawl import WangyiyunScrawl
from WeiboScrawl import WeiboScrawl
from get_users import GetUser
from Writer import Writer
import MySQLdb

class Scrawl():
    def __init__(self, url):
        # self.wangyi_scrawl = WangyiyunScrawl()
        self.anchor_users = None
        self.get_users = GetUser(url=url)
        self.writer = Writer()

    def get_anchor_users(self):
        anchors_dict = self.get_users.get_user()
        print(anchors_dict)
        self.get_users.close()
        return anchors_dict

    def get_weibo_info(self, id):
        weibo_scrawl = WeiboScrawl()
        weibo_attributes = weibo_scrawl.get_user_attributes(id=id)
        # print(weibo_attributes)
        weibo_scrawl = WeiboScrawl()
        weibo_fans = weibo_scrawl.get_user_fans(id=id)
        # print(weibo_fans)
        weibo_scrawl = WeiboScrawl()
        weibo_follows = weibo_scrawl.get_user_following(id=id)
        # print(weibo_follows)
        # weibo_scrawl = WeiboScrawl()
        # weibo_posts = weibo_scrawl.get_user_posts(id=id)
        # print(weibo_posts)
        weibo_scrawl.close()
        return weibo_attributes, weibo_fans, weibo_follows

    def get_wangyi_info(self, id):
        wangyi_scrawl = WangyiyunScrawl()
        wangyi_attributes = wangyi_scrawl.get_user_attributes(id=id)
        print("属性爬取成功！")
        wangyi_scrawl = WangyiyunScrawl()
        wangyi_fans = wangyi_scrawl.get_fans_followers(id=id, fans_or_follows='fans')
        print("粉丝爬取成功！")
        wangyi_scrawl = WangyiyunScrawl()
        wangyi_follows = wangyi_scrawl.get_fans_followers(id=id, fans_or_follows='follows')
        print("关注爬取成功！")
        wangyi_scrawl = WangyiyunScrawl()
        wangyi_posts = wangyi_scrawl.get_user_post(id=id)
        print("发帖爬取成功！")
        wangyi_scrawl.close()

        return wangyi_attributes, wangyi_fans, wangyi_follows, wangyi_posts

    def write(self):

        anchor_users = self.get_anchor_users()

        for wangyi_id in anchor_users.keys():
            wangyi_attributes, wangyi_fans, wangyi_follows, wangyi_posts = self.get_wangyi_info(id=wangyi_id)
            self.writer.write_wangyi_attributes(WY_user_attributes=wangyi_attributes, WY_id=wangyi_id)
            self.writer.write_wangyi_fans(WY_fans=wangyi_fans, WY_id=wangyi_id)
            self.writer.write_wangyi_following(WY_followers=wangyi_follows, WY_id=wangyi_id)
            self.writer.write_wangyi_posts(WY_posts=wangyi_posts, WY_id=wangyi_id)
            print(wangyi_id,"已经写入成功")
            weibo_id = int(anchor_users.get(wangyi_id))
            weibo_attributes, weibo_fans, weibo_follows = self.get_weibo_info(id=weibo_id)
            self.writer.write_weibo_attributes(WB_attributes=weibo_attributes,WB_id=weibo_id)
            self.writer.write_weibo_fans(WB_fans=weibo_fans, WB_id=weibo_id)
            self.writer.write_weibo_following(WB_follow=weibo_follows, WB_id=weibo_id)
            self.writer.write_weibo_posts(WB_id=weibo_id)


if __name__ == '__main__':
    url = 'https://music.163.com/#/song?id=4153632'
    scrawl = Scrawl(url=url)
    scrawl.write()