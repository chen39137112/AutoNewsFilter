# coding=utf-8
import logging.config
import time
from os import path
import os
import configparser
from collections import OrderedDict
import traceback
from functools import wraps
import threading
from random import randint
import requests


class Config(object):
    def __init__(self, config_filename="config/config.conf"):
        file_path = path.join(path.dirname(__file__), config_filename)
        # RawConfigParser遇到特殊字符不会转义
        self.cf = configparser.RawConfigParser()
        self.cf.read(file_path, encoding='utf-8')

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section, option):
        value = self.cf.get(section, option)
        return int(value) if value.isdigit() else value

    def get_contents(self, section):
        result = OrderedDict()
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


config = Config()

_log_settings = config.get_contents('log')
_config_path = path.join(path.dirname(__file__), _log_settings['config_path'])
_log_path = path.join(path.dirname(__file__), _log_settings['log_path'])

if not path.exists(_log_path):
    os.mkdir(_log_path)
logging.config.fileConfig(_config_path, defaults={"log_path": _log_path, 'logger_name': _log_settings['logger_name']})
logger = logging.getLogger(_log_settings['logger_name'])

KEY = config.get_content('target', 'key_words')

result_path = config.get_content('result_path', 'path')
if not path.exists(result_path):
    os.mkdir(result_path)

email_conf = config.get_contents('email')


def trace_debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger.error(traceback.format_exc())

    return wrapper


# 互斥锁，用于下方限速装饰器
lock = threading.Lock()
INTERVAL = 0.5


# 限制http请求函数调用频率，1秒内只能调用一次
def speed_limit(func):
    cache = {}

    @wraps(func)
    def decorated_func(*args, **kwargs):
        # 函数的名称作为key
        key = func.__name__
        # 判断是否存在缓存
        if key in cache.keys():
            lock.acquire()
            update_time = cache[key]
            # 过期时间固定为1秒
            delta_time = time.time() - update_time
            if delta_time < INTERVAL:
                # print(f'函数被占用中，还需等待{1 - delta_time}')
                time.sleep(INTERVAL - delta_time + randint(0, 100) / 100)
            # 如果过期，或则没有缓存调用方法
            cache[key] = time.time()
            lock.release()
        else:
            cache[key] = time.time()
        result = func(*args, **kwargs)
        return result

    return decorated_func


def url_get(url):
    return requests.get(url=url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"})
