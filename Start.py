from flask import Flask
from flask import Blueprint, render_template, request, jsonify
import re
import time
from scrawl.run import Scrawl
import base64
import jieba
import jieba.analyse

app = Flask(__name__,
            static_folder='./dist',  # 设置静态文件夹目录
            template_folder="./dist",
            static_url_path="")  # 设置vue编译输出目录dist文件夹，为Flask模板文件目录

import MySQLdb
import time

# webdriver配置
HIDE_WEB_DRIVER = False
WEB_DRIVER_PATH = "D:\\chromeDriver2\\chromedriver"

# mysql配置
MYSQL_HOST = "localhost"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "123"
MYSQL_DATABASE = "data11"


@app.route('/')
def index():
    return render_template('index.html', name='index')  # 使用模板插件，引入index.html


@app.route('/get_1s', methods=['GET'])
def catchId():
    pass
    # db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')
    # cursor = db.cursor()
    # cursor.execute("SELECT `爬取进度`.id,`爬取进度`.`爬取进度`FROM`爬取进度`")
    # data = list(cursor.fetchall())
    # cursor.close()
    # db.close()
    # return jsonify(data)


@app.route('/catchById', methods=['GET'])
def catchById():
    strId = request.args.get('strId')
    print(strId)
    url = 'https://music.163.com/#/song?id=4153632'
    scrawl = Scrawl(url=url)
    scrawl.write()
    print('结束')
    return ''


@app.route('/searchId', methods=['GET'])
def getId():
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    resList = []
    cursor = db.cursor()
    if currentApp == '网易云' or '微博':
        sqlStr = "SELECT `{0}id` FROM `网易云微博id` WHERE `{0}id` like '{1}%' LIMIT 50".format(currentApp, strId)
        print(sqlStr)
        cursor.execute(sqlStr)
        for i in cursor.fetchall():
            resList.append(i[0])
    cursor.close()
    db.close()
    return jsonify(resList)


@app.route('/getRateChart', methods=['GET'])
def getRateChart():
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    cursor = db.cursor()
    print("这是评分的表。。。")
    print(strId)
    if currentApp == '网易云' or '微博':
        sqlStr = 'select `credit` from `网易云微博id` where `{0}id` = {1}'.format(currentApp, strId)
        print(sqlStr)
        cursor.execute(sqlStr)
        res = str(cursor.fetchone()[0])
        cursor.close()
        db.close()
        return res


@app.route('/getRelChart', methods=['GET'])
def getRelChart():
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT `{0}用户名` FROM `网易云微博id` WHERE `{0}id` = '{1}' LIMIT 1".format(currentApp, strId))
    strName = cursor.fetchall()[0][0]  # 这里有问题
    # strName = '111'
    if currentApp == '网易云' or '微博':
        # select * 而不是select name 是因为有奇怪BUG，所以采用查询全部的方式
        sqlStr = "SELECT * FROM `{0}粉丝列表` WHERE `用户ID` = {1} limit 25".format(currentApp, strId)
        cursor.execute(sqlStr)
        follower = cursor.fetchall()
        sqlStr = "SELECT * FROM `{0}关注列表` WHERE `用户ID` = {1} limit 25".format(currentApp, strId)
        cursor.execute(sqlStr)
        follow = cursor.fetchall()
        followerList = []
        for i in follower:
            followerList.append(i[1])
        followList = []
        for i in follow:
            followList.append(i[1])

        # 生成所有节点的列表（因为关注和被关注者的列表可能会有重复，所以需要去重）
        allList = list(set(followerList + followList))
        # 生成节点列表，第一个放入的就是中心节点
        dataList = [{
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
        linksList = []
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

    cursor.close()
    return jsonify([dataList, linksList])


@app.route('/getBarChart', methods=['GET'])
def getBarChart():
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    cursor = db.cursor()
    # cursor.execute("SELECT 网易云用户名 FROM 网易云微博id WHERE 网易云id = {0}".format(35908438))
    # res = cursor.fetchall()
    # print(res)
    if currentApp == '网易云':
        sqlStr1 = 'SELECT `{0}发帖` FROM `{1}用户发帖` WHERE `{2}id` = {3}'.format(currentApp, currentApp, currentApp, strId)
        print(sqlStr1)
        cursor.execute(sqlStr1)
        user_post = cursor.fetchone()[0]
        words = jieba.lcut(user_post)  # 生成装有词的列表
        count = {}
        for word in words:
            if len(word) < 2:
                continue
            else:  # 只统计大于2的
                count[word] = count.get(word, 0) + 1
        word_list = list(count.items())
        word_list.sort(key=lambda x: x[1], reverse=True)  # 词频排序
        keywords_top10 = [[], []]
        for idx in range(10):
            hot_word, num = word_list[idx]
            keywords_top10[0].append(hot_word)
            keywords_top10[1].append(num)
        cursor.close()
        db.close()
        return jsonify(keywords_top10)
    if currentApp == '微博':
        sqlStr = 'select `原创微博` from `微博用户发帖` where `微博id` = {0}'.format(strId)
        cursor.execute(sqlStr)
        user_post_origin = cursor.fetchone()[0]
        sqlStr2 = 'select `转发微博` from `微博用户发帖` where `微博id` = {0}'.format(strId)
        cursor.execute(sqlStr2)
        user_repost = cursor.fetchone()[0]
        user_post = user_post_origin + user_repost
        words = jieba.lcut(user_post)  # 生成装有词的列表
        count = {}
        for word in words:
            if len(word) < 2:
                continue
            else:  # 只统计大于2的
                count[word] = count.get(word, 0) + 1
        word_list = list(count.items())
        word_list.sort(key=lambda x: x[1], reverse=True)  # 词频排序
        keywords_top10 = [[], []]
        for idx in range(10):
            hot_word, num = word_list[idx]
            keywords_top10[0].append(hot_word)
            keywords_top10[1].append(num)
        cursor.close()
        db.close()
        return jsonify(keywords_top10)

@app.route('/wordCloud', methods=['GET'])
def draw_wordcloud():
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')
    currentApp = request.args.get('currentApp')
    strId = request.args.get('strId')
    cursor = db.cursor()
    # 词云中文显示乱码解决方法：https://blog.csdn.net/qq_34777600/article/details/77455674?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_antiscanv2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_antiscanv2&utm_relevant_index=2
    from wordcloud import WordCloud
    font_path = r'C:\font\SimHei.ttf'
    if currentApp == '网易云':
        sqlStr1 = 'SELECT `{0}发帖` FROM `{1}用户发帖` WHERE `{2}id` = {3}'.format(currentApp, currentApp, currentApp, strId)
        print(sqlStr1)
        cursor.execute(sqlStr1)
        user_post = cursor.fetchone()[0]
        wordcloud = WordCloud(background_color="white",
                              font_path=font_path,
                              width=400,
                              height=400,
                              margin=2).generate(user_post)
        wordcloud.to_file('wordCloud.jpg')
    if currentApp == '微博':
        sqlStr = 'select `原创微博` from `微博用户发帖` where `微博id` = {0}'.format(strId)
        cursor.execute(sqlStr)
        user_post_origin = cursor.fetchone()[0]
        sqlStr2 = 'select `转发微博` from `微博用户发帖` where `微博id` = {0}'.format(strId)
        cursor.execute(sqlStr2)
        user_repost = cursor.fetchone()[0]
        user_post = user_post_origin + user_repost
        wordcloud = WordCloud(background_color="white",
                              font_path=font_path,
                              width=400,
                              height=400,
                              margin=2).generate(user_post)
        wordcloud.to_file('wordCloud.jpg')
        # print(user_post)
    # f = open('wordcloud.txt', 'r', encoding='utf-8').read()
    # wordcloud = WordCloud(background_color="white",
    #                       width=400,
    #                       height=400,
    #                       margin=2).generate(f)

    # wordcloud.to_file('wordCloud.jpg')

    # width,height,margin可以设置图片属性
    # generate 可以对全部文本进行自动分词,但是对中文支持不好
    # 可以设置font_path参数来设置字体集   添加一个中文字体文件，一般是.ttf或.otf格式
    # background_color参数为设置背景颜色,默认颜色为黑色
    time.sleep(0.5)
    try:
        with open('wordCloud.jpg', 'rb') as f:
            jpg_as_text = base64.b64encode(f.read())
        jpg_original = base64.b64decode(jpg_as_text)
        cursor.close()
        db.close()
        return jpg_original
    except:
        return ''


# 解决跨域问题用的
@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


if __name__ == '__main__':
    app.run(debug=True)
