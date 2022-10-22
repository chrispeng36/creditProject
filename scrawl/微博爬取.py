from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re

def get_weibo():
    driver.maximize_window()
    url=r'https://weibo.com/u/6613204920'
    driver.get(url)

    driver.implicitly_wait(30)  # 智能等待元素加载完成
    try:
        inform_show_button=driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div/div/div[2]/i')
        inform_show_button.click()
        driver.implicitly_wait(30)  # 智能等待元素加载完成
    except:
        print('没有下拉条点击的情况')

    # inform_list=driver.find_elements_by_xpath('/html/body/div/div[1]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[2]')
    # for inform in inform_list:
    #     print(inform.text)
    user_attribute_dict = {}
    user_attribute_list = []
    '''

            :param id: 用户的id
            :return: 用户的特征
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
            user_edu: 用户教育水平
            '''
    user_name = driver.find_element_by_class_name("ProfileHeader_h3_2nhjc").text
    user_attribute_list.append({"user_name":user_name})
    try:
        driver.find_element_by_class_name('woo-icon--male')
    except:
        user_sex = '女'
    else:
        user_sex = '男'
    user_attribute_list.append({"user_sex":user_sex})
    user_rank = driver.find_element_by_class_name("IconVip_icon_2tjdp").get_attribute("aria-label")
    user_attribute_list.append({"user_rank":user_rank})
    # print(user_rank)
    fans_or_folllow_driver = driver.find_element_by_class_name("ProfileHeader_h4_gcwJi").\
        find_elements_by_class_name("ProfileHeader_alink_tjHJR")
    user_fans_count = fans_or_folllow_driver[0].text.split("粉丝")[1]
    user_attribute_list.append({"user_fans_count":user_fans_count})
    user_following_count = fans_or_folllow_driver[1].text.split('关注')[1]
    user_attribute_list.append({"user_following_count":user_following_count})
    try:
        driver.find_element_by_class_name("ProfileHeader_con3_Bg19p")
    except:
        user_authority = ''
        print("该用户没有认证")
    else:
        user_authority = driver.find_element_by_class_name("ProfileHeader_con3_Bg19p").text
    user_attribute_list.append({"user_authority":user_authority})
    '''获取接下来的几类信息'''
    user_intro = ''
    birth_day = ''
    user_loc = ''
    user_edu = ''
    user_credit = ''
    join_time = ''
    info_list = driver.find_element_by_class_name("ProfileHeader_box3_2R7tq").\
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
    user_attribute_list.append({"user_intro":user_intro})
    user_attribute_list.append({"user_credit":user_credit})
    user_attribute_list.append({"user_loc":user_loc})
    user_attribute_list.append({"user_edu":user_edu})
    user_attribute_list.append({"join_time":join_time})
    user_attribute_list.append({"birth_day":birth_day})
    # print("用户简介：",user_intro)
    # print("用户信用等级：",user_credit)
    # print("用户所在地址：",user_loc)
    # print("用户学历：",user_edu)
    # print("用户加入时间：",join_time)
    # print("用户出生日期：",birth_day)
    user_attribute_dict.update({"1":user_attribute_list})
    print(user_attribute_dict)
    driver.close()
    print('爬取结束')

if __name__=="__main__":
    # 调整hide决定其是否在后台运行
    hide=False
    option = webdriver.ChromeOptions()
    option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    if hide == True:
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
    driver = webdriver.Chrome("D:\\chromeDriver\\chromedriver", chrome_options=option)
    get_weibo()