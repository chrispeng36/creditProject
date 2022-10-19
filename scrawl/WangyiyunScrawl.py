# -*- coding: utf-8 -*-
# @Time : 2022/3/30 9:56
# @Author : ChrisPeng
# @FileName: WangyiyunScrawl.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import json

'''
这里的输入都是对于单个用户的
'''
class WangyiyunScrawl():

    def __init__(self):
        hide = True
        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        if hide == True:
            option.add_argument('--headless')
            option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome("D:\\chromeDriver\\chromedriver", chrome_options=option)

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

    def get_fans_followers(self,id,fans_or_follows):
        '''

        :param id: 需要爬取用户的id
        :param fans_or_follows: 选取模式，'fans'表示爬取该用户对应的粉丝，'follows'爬取对应的关注者
        :param driver: 驱动器
        :return: {用户：[粉丝列表]}，或者{用户：[关注列表]}
        '''
        driver = self.driver
        fans_or_followsDict = {}
        fans_or_followsList = []
        # 需要进指定页面才能获取到cookie,否则会报错

        url = "https://music.163.com/#/user/" + fans_or_follows + "?id=" + str(id)
        driver = self.get_content(url=url)
        driver.switch_to.frame(driver.find_element_by_id("g_iframe"))
        flag = True

        while flag:
            sleep(1)
            try:
                # 这段就是把整个用户列表的信息打下来了
                user_data_ul = driver.find_element_by_id("main-box")

                user_list = user_data_ul.find_elements_by_tag_name('li')
                for i in user_list:
                    fans_or_follows_dictTemp = {}
                    i = i.find_element_by_tag_name('a')
                    single_user_id = i.get_attribute('href')
                    try:
                        single_user_id = re.search('(?<=\?id=).*', single_user_id).group(0)
                    except:
                        single_user_id = '没查找到id'
                    single_user_name = i.get_attribute('title')
                    fans_or_follows_dictTemp.update({single_user_name:single_user_id})
                    fans_or_followsList.append(fans_or_follows_dictTemp)
                    # print(single_user_name, single_user_id)

            except:
                print('未抓取到数据')
            if driver.find_element_by_xpath("//a[text()='下一页']") is not None:
                try:
                    driver.find_element_by_id("page").find_element_by_class_name("js-disabled")
                except:
                    # 翻到底页去滚动页面
                    js = "window.scrollTo(0, document.body.scrollHeight);"
                    driver.execute_script(js)
                    driver.find_element_by_xpath("//a[text()='下一页']").click()
                else:
                    if driver.find_element_by_id("page").find_element_by_class_name("js-disabled").text == '下一页':
                        flag = False
                    else:
                        # 翻到底页去滚动页面，也就是第一页的上一页会出现disabled，要避免这种情况不翻页
                        js = "window.scrollTo(0, document.body.scrollHeight);"
                        driver.execute_script(js)
                        driver.find_element_by_xpath("//a[text()='下一页']").click()
            else:
                # 说明没有分页了，可以直接结束
                flag = False
                print('当前页面只有一页')


        sleep(1)

        driver.close()
        fans_or_followsDict.update({id:fans_or_followsList})
        print('爬取结束')
        return fans_or_followsDict

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

    def get_user_attributes(self,id):
        '''

        :param id: 用户的id
        :param driver: 驱动器
        :return: user_name：用户名
                user_rank: 用户等级
                user_sex: 用户性别
                user_event: 用户动态数
                user_follow: 用户关注人数
                user_fans: 用户粉丝数
                user_intro: 用户个人介绍
                user_loc: 用户所在地
                user_age: 用户年龄
                weibo_link: 微博链接
        '''
        driver = self.driver
        # 需要进指定页面才能获取到cookie,否则会报错
        url = "https://music.163.com/#/user/" + "?id=" + str(id)
        driver = self.get_content(url=url)
        driver.switch_to.frame(driver.find_element_by_id("g_iframe"))
        user_info = driver.find_element_by_id("head-box")

        user_name = user_info.find_element_by_id("j-name-wrap").find_element_by_class_name('tit').text
        user_rank = user_info.find_element_by_id("j-name-wrap").find_element_by_class_name('lev').text
        user_sex = '男' if user_info.find_element_by_id("j-name-wrap").find_element_by_class_name('u-icn2-lev') is not None \
            else '女'

        user_event = user_info.find_element_by_id("event_count").text
        user_follow = user_info.find_element_by_id("follow_count").text
        user_fans = user_info.find_element_by_id("fan_count").text
        user_intro = user_info.find_element_by_class_name("f-brk").text
        user_loc = '' if user_info.find_element_by_class_name("inf") is None else \
            user_info.find_elements_by_class_name("inf")[1].find_elements_by_tag_name('span')[0].text
        user_loc = user_loc.split('所在地区：')[1]
        user_age = user_info.find_element_by_id("age").text
        weibo_id = user_info.find_element_by_class_name("u-logo-s").find_element_by_tag_name('a').get_attribute('href')
        weibo_id = weibo_id.split('http://weibo.com/u/')[1]

        res_dict = {}
        res_dict['user_name'] = user_name
        res_dict['user_rank'] = user_rank
        res_dict['user_age'] = user_age
        res_dict['user_event'] = user_event
        res_dict['user_loc'] = user_loc
        res_dict['user_fans'] = user_fans
        res_dict['user_follow'] = user_follow
        res_dict['user_event'] = user_event
        res_dict['user_intro'] = user_intro
        res_dict['user_sex'] = user_sex
        res_dict['weibo_id'] = weibo_id
        # res_dict.update({'user_name': user_name})
        # res_dict.update({'user_rank':user_rank})
        # res_dict.update({'user_age':user_age})
        # res_dict.update({'user_event':user_event})
        # res_dict.update({'user_loc':user_loc})
        # res_dict.update({'user_fans':user_fans})
        # res_dict.update({'user_follow':user_follow})
        # res_dict.update({'user_event':user_event})
        # res_dict.update({'user_intro':user_intro})
        # res_dict.update({'user_sex':user_sex})

        return res_dict

    def get_user_post(self, id):
        '''

        :param id: 用户的id
        :param driver: 驱动器
        :return: 发帖的文本字符串
        '''
        driver = self.driver
        url = 'https://music.163.com/#/user/event?id=' + str(id)
        self.get_content(url=url)
        js = "var q=document.body.scrollTop=10000"
        driver.execute_script(js)#滚动加载页面
        driver.switch_to_frame("contentFrame")#因为有多个frame，定位
        user_post = ''
        try:
            user_data_ul = driver.find_element_by_id("eventListBox")#找到有信息的位置
            user_post_list = user_data_ul.find_elements_by_tag_name('li')
            for post in user_post_list:
                singl_post = post.text.replace(' ','').replace('\n','')
                singl_post = re.sub('\d+年\d+月\d+日\d+:\d+', '', singl_post)
                singl_post = re.sub('\(\d*\)\|转发\|评论', '', singl_post)
                user_post += singl_post
        except:
            print("没有抓取到数据")
        return user_post



if __name__ == '__main__':

    wangyiyun_scrawler = WangyiyunScrawl()
    # 调整hide决定其是否在后台运行
    # dict1 = wangyiyun_scrawler.get_fans_followers(1763051697, 'follows')
    # print(dict1)
    # print(dict1.get(1763051697)[0])
    # print(type(dictTemp.get(1763051697)[0]))
    d = wangyiyun_scrawler.get_user_attributes(1763051697)
    print(d)