# -*- coding: utf-8 -*-
# @Time : 2022/6/14 14:23
# @Author : ChrisPeng
# @FileName: test.py
# @Software: PyCharm
# @Blog ：https://chrispeng36.github.io/


from flask import Flask
from flask import Blueprint, render_template, request, jsonify
import re
import time
# from GetData import GetData
import base64
import MySQLdb
import random

MYSQL_HOST="localhost"
MYSQL_USERNAME="root"
MYSQL_PASSWORD="123"
MYSQL_DATABASE="data11"
db = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE, charset='utf8')

cursor = db.cursor()
sqlStr = 'SELECT `网易云发帖` FROM `网易云用户发帖` WHERE `网易云id` = 268530254;'

cursor.execute(sqlStr)
res = cursor.fetchone()

print(res)

