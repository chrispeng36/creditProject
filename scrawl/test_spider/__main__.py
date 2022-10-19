# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 10:52
# @Author  : ChrisPeng
# @File    : __main__.py
# @Software: PyCharm

import os
import sys

from absl import app
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from test_spider.spider import main

app.run(main)