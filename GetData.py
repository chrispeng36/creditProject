from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import json
import MySQLdb
HIDE_WEB_DRIVER = False
WEB_DRIVER_PATH = "D:/bishe/chromedriver"

from scrawl.WangyiyunScrawl import WangyiyunScrawl
from scrawl.WeiboScrawl import WeiboScrawl
from Writer import Writer

'''
爬虫获取信息
'''

class GetData():
    def __init__(self, WY_id, WB_id):
        self.WY_id = WY_id
        self.WB_id = WB_id
        self.WangyiyunScrawl = WangyiyunScrawl()
        self.weiboScrawl = WeiboScrawl()
    '''获取网易云的信息'''
    def get_WY_followers(self):
        return self.WangyiyunScrawl.get_fans_followers(id=self.WY_id,fans_or_follows='follows')
    def get_WY_fans(self):
        return self.WangyiyunScrawl.get_fans_followers(id=self.WY_id, fans_or_follows='fans')
    def get_WY_user_attributes(self):
        return self.WangyiyunScrawl.get_user_attributes(id=self.WY_id)
    def get_WY_get_user_post(self):
        return self.WangyiyunScrawl.get_user_post(id=self.WY_id)

    '''获取微博的信息'''
    def get_WB_attributes(self):
        return self.weiboScrawl.get_user_attributes(id=self.WB_id)
    def get_WB_following(self):
        return self.weiboScrawl.get_user_following(id=self.WB_id)
    def get_WB_fans(self):
        return self.weiboScrawl.get_user_fans(id=self.WB_id)
    # def get_WB_posts(self):
    #     return self.weiboScrawl.get_user_posts(id=self.WB_id)



if __name__=="__main__":
    # 调整hide决定其是否在后台运行
    '''
    存在的问题：
    爬虫过程中需要将赋值改成try语句，不然可能有些elements找不到
    '''
    print("这是什么情况")
    get_data = GetData(WY_id=1763051697,WB_id=3176010690)
    '''获取需要的各种信息，现在缺用户的网易云以及微博的id'''
    # WY_followers = get_data.get_WY_followers()
    MYSQL_HOST = "localhost"
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = "123"
    MYSQL_DATABASE = "data11"
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')

    # WB_post = get_data.get_WB_posts()
    Writer = Writer()
    # Writer.write_weibo_posts(WB_post)
    # print("============================")
    # print(WB_post)
    WB_attributes = get_data.get_WB_attributes()
    # Writer.write_weibo_posts(WB_attributes)
    Writer.write_weibo_attributes(WB_attributes)
    Writer.shutdown()
    # followers = list(WY_followers.values())[0]
    # Writer = Writer()
    # Writer.write_wangyi_following(WY_followers)
    # WY_fans = get_data.get_WY_fans()
    # Writer = Writer()
    # Writer.write_wangyi_fans(WY_fans)
    # print(WY_fans)
    # Writer.shutdown()

    # Writer = Writer()
    # # WB_follows = get_data.get_WB_following()
    # # Writer.write_weibo_following(WB_follows)
    # # print(WB_follows)
    # WB_fans = get_data.get_WB_fans()
    # Writer.write_weibo_fans(WB_fans)
    # print(WB_fans)
    # WY_posts = get_data.get_WY_get_user_post()
    # print(WY_posts)
    # Writer.write_wangyi_posts(WY_posts)
    # Writer.shutdown()
    # WY_user_attributes = get_data.get_WY_user_attributes()
    # Writer.write_wangyi_attributes(WY_user_attributes)
    # Writer.shutdown()

    # user_id = 1269643340
    # index = 0
    # cursor = db.cursor()  # 数据库的游标
    # for user in followers:
    #     follow_name = list(user.keys())[0]
    #     follow_id = list(user.values())[0]
    #     temp_sql = "insert into 网易云关注列表新增 (`序号`,`name`,`用户ID`,`id`) VALUES ({},{},{},{});".format(index, "'{}'".format(follow_name),int(follow_id), user_id)
    #     cursor.execute(temp_sql)
    #
    #
    #
    # # sqlStr = "insert into test (id,`name`) VALUES ('2','chshiufs');"
    # # cursor.execute(sqlStr)
    # db.commit()
    # db.close()
    # print("over")
    # print(WY_followers)

    # WY_fans = get_data.get_WY_fans()
    # WY_user_attributes = get_data.get_WB_get_user_attributes()
    # WY_get_user_post = get_data.get_WY_get_user_post()
    #
    # WB_get_user_attributes = get_data.get_WB_get_user_attributes()
    # WB_get_user_following = get_data.get_WB_get_user_following()
    # WB_get_user_fans = get_data.get_WB_get_user_fans()
    # WB_user_posts = get_data.get_WB_user_posts()
    # WY_user_attributes = get_data.get_WY_user_attributes()
    # print(WY_user_attributes)