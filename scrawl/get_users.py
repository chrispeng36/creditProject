# -*- coding: utf-8 -*-
# @Time : 2022/10/20 8:05
# @Author : ChrisPeng
# @FileName: get_users.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import json
from WeiboScrawl import WeiboScrawl
from WangyiyunScrawl import WangyiyunScrawl

class GetUser(object):

    def __init__(self, url):
        self.url = url  # 开始爬虫的页面，可以设置
        hide = True
        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        if hide == True:
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome("D:\\chromeDriver\\chromedriver", chrome_options=option)
        self.driver_weibo = webdriver.Chrome("D:\\chromeDriver1\\chromedriver", chrome_options=option)
        self.wangyi_HOME_PAGE = 'https://music.163.com/#'
        self.weibo_scralwer = WeiboScrawl()
        self.wangyi_scrawler = WangyiyunScrawl()



    def get_content(self,url):
        '''

        :param url: 待登录的网页
        :param driver: 驱动器
        :return: 爬取的待处理的信息
        '''
        driver = self.driver
        driver.maximize_window()
        driver.get(url)
        while True:
            try:
                with open('cookies.txt', 'r') as cookief:
                    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
                    cookieslist = json.load(cookief)

                    #  将expiry类型变为int
                    for cookie in cookieslist:
                        # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
                        if isinstance(cookie.get('expiry'), float):
                            cookie['expiry'] = int(cookie['expiry'])
                        driver.add_cookie(cookie)
                sleep(2)
                # 获取到页面后再次刷新页面，这时候可以看是否还有登录选项了
                driver.get(url)

                break
            except:
                print('需要登录')
                self.log_in(driver)
                print("登陆完毕")

        try:
            # 有登录选项的话就需要走登录的流程
            driver.find_element_by_css_selector("[data-action=login]")
            print('需要登录')
            self.log_in(driver)
            print("登陆完毕")
        except:
            print('不用登录')
        sleep(1.5)
        return driver

    def get_content_webio(self,url):
        '''

        :param url: 待登录的网页
        :param driver: 驱动器
        :return: 爬取的待处理的信息
        '''
        driver = self.driver_weibo
        driver.maximize_window()
        driver.get(url)
        while True:
            try:
                with open('cookies.txt', 'r') as cookief:
                    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
                    cookieslist = json.load(cookief)

                    #  将expiry类型变为int
                    for cookie in cookieslist:
                        # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
                        if isinstance(cookie.get('expiry'), float):
                            cookie['expiry'] = int(cookie['expiry'])
                        driver.add_cookie(cookie)
                sleep(2)
                # 获取到页面后再次刷新页面，这时候可以看是否还有登录选项了
                driver.get(url)

                break
            except:
                print('需要登录')
                self.log_in(driver)
                print("登陆完毕")

        try:
            # 有登录选项的话就需要走登录的流程
            driver.find_element_by_css_selector("[data-action=login]")
            print('需要登录')
            self.log_in(driver)
            print("登陆完毕")
        except:
            print('不用登录')
        sleep(1.5)
        return driver

    def log_in(self):
        '''
        模拟登陆操作
        :param driver: 驱动器
        :return: null
        '''
        driver = self.driver
        driver.get('http://music.163.com/#/login')
        # 程序打开网页后60秒内手动登陆账户
        sleep(60)

        with open('cookies.txt', 'w') as cookief:
            # 将cookies保存为json格式
            cookief.write(json.dumps(driver.get_cookies()))
        driver.close()

    def get_user(self):
        '''
        根据歌曲主页的信息尝试爬取同一个用户
        '''
        driver = self.get_content(url=self.url)
        driver.switch_to.frame(driver.find_element_by_class_name("g-iframe"))

        accounts_link_dict = {} #wangyi_id -> weibo_id
        FLAG = True
        cur_page = 0
        '''只翻页50'''
        while(FLAG and cur_page < 1):
            sleep(1)
            try:
                info = driver.find_element_by_id("comment-box")
                comments_list = info.find_element_by_class_name("cmmts")
                user_list = comments_list.find_elements_by_class_name("itm")
                print(driver.title)
                for user in user_list:
                    user_home_page = user.find_element_by_class_name("head").find_element_by_tag_name('a').get_attribute("href")

                    user_wangyi_id = int(user_home_page.split("=")[1])

                    # wangyi_attribute = self.wangyi_scrawler.get_user_attributes(user_wangyi_id)
                    # print(wangyi_attribute)
                    '''上面获取了当前页面的所有的网易云id'''
                    '''可能有些人注销了账号。。。'''
                    driver_for_weibo = self.get_content_webio(url=user_home_page)
                    driver_for_weibo.switch_to.frame(driver_for_weibo.find_element_by_id("g_iframe"))
                    user_info = driver_for_weibo.find_element_by_id("head-box")
                    try:
                        weibo_id = user_info.find_element_by_class_name("u-logo-s").find_element_by_tag_name(
                            'a').get_attribute('href')
                        weibo_id = weibo_id.split('http://weibo.com/u/')[1]
                    except:
                        weibo_id = None
                        print("该用户没有微博链接！！！")
                    if weibo_id is not None:
                        print(user_wangyi_id)
                        accounts_link_dict[user_wangyi_id] = weibo_id

            except:
                print("未能抓取到数据！！！")
            print(driver.title)
            next_page_button = driver.find_element_by_class_name("u-page")
            if next_page_button.find_element_by_class_name("js-disabled") is not None:
                text = next_page_button.find_element_by_class_name("js-disabled").text
                if text == '下一页':
                    '''说明已经没有翻页了'''
                    FLAG = False
                else:
                    '''说明是第一页，可以继续翻页'''
                    button = driver.find_element_by_class_name("zbtn")
                    button.click()# 点击下一页
                cur_page += 1
            else:
                '''既不是第一页，也不是最后一页，直接点击'''
                button = driver.find_element_by_class_name("zbtn")
                button.click()  # 点击下一页
        return accounts_link_dict

    def close(self):
        self.driver.close()
        self.driver_weibo.close()





if __name__ == '__main__':
    get_user = GetUser(url='https://music.163.com/#/song?id=4153632')
    accounts = get_user.get_user()
    print(accounts)
