# -*- coding: utf-8 -*-
# @Time    : 2022/4/3 20:41
# @Author  : ChrisPeng
# @File    : downloader.py
# @Software: PyCharm
import logging
import os
import sys
from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm

logger = logging.getLogger('spider.downloader')
'''省略了源文件中的图片以及视频的下载'''
class Downloader(ABC):
    def __init__(self, file_dir, file_download_timeout):
        self.file_dir = file_dir
        self.describe = ''
        self.key = ''
        self.file_download_timeout = [5, 5, 10]
        if (isinstance(file_download_timeout, list)) and (len(file_download_timeout) == 3):
            for i in range(3):
                v = file_download_timeout[i]
                if isinstance(v, (int, float)) and v > 0:
                    self.file_download_timeout[i] = v


