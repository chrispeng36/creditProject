# -*- coding: utf-8 -*-
# @Time    : 2022/4/16 14:42
# @Author  : ChrisPeng
# @File    : help.py
# @Software: PyCharm
import pandas as pd
from WeiboScrawl import WeiboScrawl
from WangyiyunScrawl import WangyiyunScrawl
# scrawl = WeiboScrawl()
#
# f = open(r'D:\项目\Extract_long_text_features\MLP\data\test_missing.txt')
# # line = f.readline()
# df = pd.read_excel(r'D:\项目\Extract_long_text_features\MLP\data\test_add.xlsx')
# sex = ''
# count = 0
# while True:
#     line = f.readline()
#     count += 1
#     if line:
#         print(line.strip())
#         sex = scrawl.get_user_attributes(line.strip())
#         print(sex)
#         add_temp = pd.DataFrame({'id':line.strip(),'sex':sex},index=[1])
#         df = df.append(add_temp, ignore_index=True)
#         # break
#     else:
#         break
#     print('---------' + str(count) + '-------------')
# df.to_excel(r'D:\项目\Extract_long_text_features\MLP\data\test_add.xlsx',index=False)
# f.close()
# print(df)
# print('over!!!')


scrawl = WeiboScrawl()

test1 = scrawl.get_user_posts(6292624763)
print(test1)