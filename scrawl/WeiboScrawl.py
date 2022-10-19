# -*- coding: utf-8 -*-
# @Time : 2022/4/1 15:43
# @Author : ChrisPeng
# @FileName: WeiboScrawl.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/

from absl import app, flags
import logging

logger = logging.getLogger('WeiboScrawl')
from test_spider.spider import _get_config
from test_spider.config_util import validate_config
from test_spider import spider
from lxml import html
import json
import time
import pandas as pd
import numpy as np
from fake_useragent import UserAgent
import random
etree = html.etree
import requests  # 导入requests包
from selenium import webdriver

class WeiboScrawl():

    def __init__(self):
        '''
        记得更换cookie
        '''
        ua = UserAgent()
        self.headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Cookie': 'PC_TOKEN=e46c84a85b; XSRF-TOKEN=CJeFrTnI1PcMwY3q8rst6GFy; SUB=_2A25Po47MDeRhGeBI6lET8CrFyTyIHXVs2OcErDV8PUNbmtAKLRjVkW9NRrEU1UYwNLZsvOXDl4rPnFWBx78xABbM; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhmvAghRvVWRIXwUOCfdA_s5JpX5KzhUgL.FoqceKeEehB4eo52dJLoIp8hIGiDMNWLdJMp1K.4ehe7Sntt; ALF=1686712860; SSOLoginState=1655176860; WBPSESS=39AlmNMpKtW8ntUWMdo1GuC5wsBwdSMqqID5fRsXNLLcY_H9W2LGWPuRU_zcXVcNgIq1lqVnJOOLmxlY17pbXfWE9qeafm5WvBUy0JBXld1O9n--C02VhZkjeEbsv7Wt3MBuMi_HnKXbcGKfV-dbMg=='
    }
        hide = True#隐藏浏览器
        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        if hide == True:
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome("D:\\chromeDriver\\chromedriver", chrome_options=option)

    def get_user_attributes(self, id):
        '''

        :param id: 用户的id
        :return: 用户的特征(dict形式存储)
        user_name: 用户名
        user_fans_count: 粉丝数
        user_following_coount: 关注人数
        user_sex: 性别
        user_rank: 用户等级
        user_intro: 用户简介
        user_authority: 用户认证
        join_time: 加入日期
        birth_day: 生日
        user_loc: 用户位置
        user_credit: 用户信用等级
        '''
        self.driver.maximize_window()
        url = 'https://weibo.com/u/' + str(id)
        self.driver.get(url)
        time.sleep(8)
        try:
            inform_show_button = self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div/div/div[2]/i')
            inform_show_button.click()
            time.sleep(5)  # 智能等待元素加载完成
        except:
            print('没有下拉条点击的情况')

        # inform_list=driver.find_elements_by_xpath('/html/body/div/div[1]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[2]')
        # for inform in inform_list:
        #     print(inform.text)
        user_attribute_dict = {}
        user_attribute_list = []
        user_name = self.driver.find_element_by_class_name("ProfileHeader_h3_2nhjc").text
        user_attribute_list.append({"user_name": user_name})
        try:
            self.driver.find_element_by_class_name('woo-icon--male')
        except:
            user_sex = '女'
        else:
            user_sex = '男'
        user_attribute_list.append({"user_sex": user_sex})
        user_rank = self.driver.find_element_by_class_name("IconVip_icon_2tjdp").get_attribute("aria-label")
        user_attribute_list.append({"user_rank": user_rank})
        # print(user_rank)
        fans_or_folllow_driver = self.driver.find_element_by_class_name("ProfileHeader_h4_gcwJi"). \
            find_elements_by_class_name("ProfileHeader_alink_tjHJR")
        user_fans_count = fans_or_folllow_driver[0].text.split("粉丝")[1]
        user_attribute_list.append({"user_fans_count": user_fans_count})
        user_following_count = fans_or_folllow_driver[1].text.split('关注')[1]
        user_attribute_list.append({"user_following_count": user_following_count})
        try:
            self.driver.find_element_by_class_name("ProfileHeader_con3_Bg19p")
        except:
            user_authority = ''
            print("该用户没有认证")
        else:
            user_authority = self.driver.find_element_by_class_name("ProfileHeader_con3_Bg19p").text
        user_attribute_list.append({"user_authority": user_authority})
        '''获取接下来的几类信息'''
        user_intro = ''
        birth_day = ''
        user_loc = ''
        user_edu = ''
        user_credit = ''
        join_time = ''
        info_list = self.driver.find_element_by_class_name("ProfileHeader_box3_2R7tq"). \
            find_elements_by_class_name("woo-box-item-inlineBlock")
        for info in info_list:
            # print(info.text)
            class_name = info.find_element_by_tag_name("i").get_attribute("class")
            if "woo-font--proBintro" in class_name:
                user_intro = info.text
            elif "woo-font--proIntro" in class_name:
                birth_day = info.text
            elif "woo-font--proPlace" in class_name:
                user_loc = info.text
            elif "woo-font--proTime" in class_name:
                join_time = info.text
            elif "woo-font--proCredit" in class_name:
                user_credit = info.text
            elif "woo-font--proEdu" in class_name:
                user_edu = info.text
        '''在循环外更新属性值'''
        user_attribute_list.append({"user_intro": user_intro})
        user_attribute_list.append({"user_credit": user_credit})
        user_attribute_list.append({"user_loc": user_loc})
        user_attribute_list.append({"user_edu": user_edu})
        user_attribute_list.append({"join_time": join_time})
        user_attribute_list.append({"birth_day": birth_day})
        # # print("用户简介：",user_intro)
        # # print("用户信用等级：",user_credit)
        # # print("用户所在地址：",user_loc)
        # # print("用户学历：",user_edu)
        # # print("用户加入时间：",join_time)
        # # print("用户出生日期：",birth_day)
        user_attribute_dict.update({id: user_attribute_list})
        # print(user_attribute_dict)
        self.driver.close()
        print('爬取结束')
        return user_attribute_dict

    def get_user_following(self, id):
        '''

        :param id: 爬取用户的id
        :return: {用户：[关注列表]}
        '''
        following_dict = {}
        following_list = []
        page = 1
        while (page < 31):
            url = 'https://weibo.com/ajax/friendships/friends?page={0}&uid={1}'.format(page, id)
            html_str = requests.get(url, headers=self.headers)  # Get方式获取网页数据
            html_str.encoding = 'utf-8'
            # print(html_str)
            if html_str.status_code == 400:#不可访问的界面
                return following_dict
            result_dict = json.loads(html_str.text.encode('utf-8'))
            # 一个result_dict表示一个页面的内容
            # new_dict = {}
            for i in range(len(result_dict['users'])):
                dict_per_following = result_dict['users'][i]
                following_id = dict_per_following['id']
                following_name = dict_per_following['name']
                new_dict_update = {'id': following_id, 'name': following_name}

                following_list.append(new_dict_update)
            # users里面没有信息则跳出循环
            if not result_dict['users']:
                break
            page += 1
        # time.sleep(np.random.randint(10, 20))#防止反爬,如果多次爬取可以开启
        following_dict.update({id:following_list})
        return following_dict

    def get_user_fans(self, id):
        '''

        :param id: 爬取用户的id
        :return: {用户：[粉丝列表]}
        '''
        fans_dict = {}
        fans_list = []
        page = 1
        while (page < 31):
            url = 'https://weibo.com/ajax/friendships/friends?relate=fans&page={0}&uid={1}'.format(page, id)
            html_str = requests.get(url, headers=self.headers)  # Get方式获取网页数据
            html_str.encoding = 'utf-8'
            # print(html_str)
            if html_str.status_code == 400:  # 不可访问的界面
                return fans_dict
            result_dict = json.loads(html_str.text.encode('utf-8'))
            # 一个result_dict表示一个页面的内容
            # new_dict = {}
            for i in range(len(result_dict['users'])):
                dict_per_fan = result_dict['users'][i]
                fan_id = dict_per_fan['id']
                fan_name = dict_per_fan['name']
                new_dict_update = {'id': fan_id, 'name': fan_name}

                fans_list.append(new_dict_update)
            # users里面没有信息则跳出循环
            if not result_dict['users']:
                break
            page += 1
        # time.sleep(np.random.randint(10, 20))#防止反爬,如果多次爬取可以开启
        fans_dict.update({id: fans_list})
        return fans_dict

    def get_user_posts(self, id):
        '''
        本代码是调用GitHub项目地址https://github.com/dataabc/weiboSpider中的爬虫代码来爬取微博用户的。
        本地是weiboSpider文件夹
        :param id: 用户的id
        :return: 字符串格式
                self_post：用户原创的微博
                retweet_weibo：用户转发的微博
                这个地方的接口位于test_spider.spider文件中
        '''
        user_id_list = [str(id)]

        try:
            with open(r'D:\CreditProject\web_platform\scrawl\test_spider\config.json') as f:
                config = json.loads(f.read())
                # print("修改前：",config["user_id_list"])
                config["user_id_list"] = user_id_list
                # print("修改后：",config["user_id_list"])
            f.close()
            # print(config)
            with open('config.json', 'w') as r:
                json.dump(config, r)
            r.close()
        except Exception as e:
            logger.exception(e)
        app.run(spider.main)
        # print(type(weibo))




if __name__ == '__main__':
    weiboScrawl = WeiboScrawl()
    print("what")
    follow = weiboScrawl.get_user_posts(6613204920)
    print("try again")
    print(follow)
    # print(following_dict)