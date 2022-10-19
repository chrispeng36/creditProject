from flask import Flask
from flask import Blueprint, render_template, request, jsonify
import re
import time
from GetData import GetData
import base64

get_data = GetData(WY_id=1763051697,WB_id=6275391314)
app = Flask(__name__,
static_folder='./dist',  #设置静态文件夹目录
template_folder = "./dist",
static_url_path="")  #设置vue编译输出目录dist文件夹，为Flask模板文件目录

import MySQLdb
import random
from Writer import Writer
# webdriver配置
HIDE_WEB_DRIVER = False
WEB_DRIVER_PATH = "D:/chromedriver/chromedriver"

# mysql配置
MYSQL_HOST="localhost"
MYSQL_USERNAME="root"
MYSQL_PASSWORD="123"
MYSQL_DATABASE="data11"
db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')

cursor = db.cursor() # 数据库的游标

@app.route('/')
def index():
    return render_template('index.html',name='index') #使用模板插件，引入index.html

@app.route('/get_1s',methods=['GET'])
def catchId():
    cursor.execute("SELECT `爬取进度`.id,`爬取进度`.`爬取进度`FROM`爬取进度`")
    data=list(cursor.fetchall())
    return jsonify(data)

@app.route('/catchById',methods=['GET'])
def catchById():#网易云的爬取和微博的爬取
    strId = request.args.get('strId')
    print(strId)

    '''获取需要的各种信息，现在缺用户的网易云以及微博的id'''
    WY_followers = get_data.get_WY_followers()
    WY_fans = get_data.get_WY_fans()
    WY_user_attributes = get_data.get_WB_get_user_attributes()
    WY_get_user_post = get_data.get_WY_get_user_post()

    WB_get_user_attributes = get_data.get_WB_get_user_attributes()
    WB_get_user_following = get_data.get_WB_get_user_following()
    WB_get_user_fans = get_data.get_WB_get_user_fans()

    writer = Writer()
    writer.write_wangyi_attributes(WY_user_attributes=WY_user_attributes)
    writer.write_wangyi_fans(WY_fans=WY_fans)
    writer.write_wangyi_following(WY_followers=WY_followers)
    writer.write_wangyi_posts(WY_posts=WY_get_user_post)

    writer.write_weibo_attributes(WB_get_user_attributes)
    writer.write_weibo_fans(WB_fans=WB_get_user_fans)
    writer.write_weibo_following(WB_follow=WB_get_user_following)
    writer.write_weibo_posts(int(strId))
    '''提供了数据但是还没存储'''
    print('结束')
    return ''

@app.route('/searchId',methods=['GET'])
def getId():
    '''从数据库中获取id'''
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    resList=[]
    if currentApp=='网易云' or '微博':
        sqlStr="SELECT `{0}id` FROM `网易云微博id` WHERE `{0}id` like '{1}%' LIMIT 50".format(currentApp,strId)
        print(sqlStr)
        cursor.execute(sqlStr)
        for i in cursor.fetchall():
            resList.append(i[0])
        return jsonify(resList)

@app.route('/getRateChart',methods=['GET'])
def getRateChart():#信用分，待修改
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    res=str(random.randint(0,100))
    return res

@app.route('/getRelChart',methods=['GET'])
def getRelChart():
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')

    cursor.execute("SELECT `{0}用户名` FROM `网易云微博id` WHERE `{0}id` = '{1}' LIMIT 1".format(currentApp, strId))
    strName=cursor.fetchall()[0][0]
    print(strName, type(strName))

    if currentApp=='网易云' or '微博':
        # select * 而不是select name 是因为有奇怪BUG，所以采用查询全部的方式
        sqlStr="SELECT * FROM `{0}粉丝列表` WHERE `用户ID` = {1} limit 25".format(currentApp,strId)
        cursor.execute(sqlStr)
        follower =cursor.fetchall()
        sqlStr="SELECT * FROM `{0}关注列表` WHERE `用户ID` = {1} limit 25".format(currentApp,strId)
        cursor.execute(sqlStr)
        follow =cursor.fetchall()
        followerList=[]
        for i in follower:
            followerList.append(i[1])
        followList=[]
        for i in follow:
            followList.append(i[1])

        # 生成所有节点的列表（因为关注和被关注者的列表可能会有重复，所以需要去重）
        allList=list(set(followerList+followList))
        # 生成节点列表，第一个放入的就是中心节点
        dataList=[{
            "name": strName,
            "symbolSize": 70,
            "category": 0,
          }]
        # 其他节点信息push进去
        for i in allList:
            dataList.append({
            "name": i,
            "category": 1,
          })
        linksList=[]
        for i in followerList:
            linksList.append({
            "source": i,
            "target": strName,
            "name": '',
          })
        for i in followList:
            linksList.append({
            "source": strName,
            "target": i,
            "name": '',
          })


    print([dataList,linksList])
    return jsonify([dataList,linksList])

@app.route('/getBarChart',methods=['GET'])
def getBarChart():
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    resList=[['爱豆','喜欢','打榜','微博','搜索','位置','怎么','好奇','在看','关注'],[]]
    for i in range(10):
        resList[1].append(random.randint(1,200))
    resList[1].sort(reverse=True)
    random.shuffle(resList[0])
    return jsonify(resList)

@app.route('/wordCloud',methods=['GET'])
def draw_wordcloud():
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    # 词云中文显示乱码解决方法：https://blog.csdn.net/qq_34777600/article/details/77455674?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_antiscanv2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_antiscanv2&utm_relevant_index=2
    from wordcloud import WordCloud
    # f = open('wordcloud.txt', 'r', encoding='utf-8').read()
    # wordcloud = WordCloud(background_color="white",
    #                       width=400,
    #                       height=400,
    #                       margin=2).generate(f)
    #
    # wordcloud.to_file('wordCloud.jpg')

    # width,height,margin可以设置图片属性
    # generate 可以对全部文本进行自动分词,但是对中文支持不好
    # 可以设置font_path参数来设置字体集   添加一个中文字体文件，一般是.ttf或.otf格式
    # background_color参数为设置背景颜色,默认颜色为黑色
    try:
        with open('wordCloud.jpg','rb') as f:
            jpg_as_text = base64.b64encode(f.read())
        jpg_original = base64.b64decode(jpg_as_text)

        return jpg_original
    except:
        return ''


# 解决跨域问题用的
@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

if __name__ == '__main__':
    app.run(debug=True)
