import os
from datetime import datetime

from utils import logger, result_path


class PostInfo:
    end_mark = '-end-'

    def __init__(self, paper, date):
        self.title = list()
        self.url = list()
        self.section = list()
        self.date = datetime.strptime(date, '%Y%m%d') if len(date) > 0 else datetime.now()
        self.path = ''
        self.paper = paper

    def is_recorded(self):
        year = self.date.year
        month = self.date.month
        day = self.date.day

        self.path = result_path + '/{}-{:0>2d}-{:0>2d}'.format(year, month, day) + '_' + self.paper + '.txt'
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                texts = f.read()
                if self.end_mark in texts:
                    return True
        except FileNotFoundError:
            # windows下无法使用该方法
            # os.mknod(self.path)
            logger.info('first time to check, create file!')

        return False

    def write_head(self, file_handle):
        head_info = '{}-{:0>2d}-{:0>2d}'.format(self.date.year, self.date.month, self.date.day)
        file_handle.write('=' * 10 + head_info + '=' * 10 + '\n')

    def write_single(self, file_handle, i):
        # 此处不太可能超过100条，02d够用
        file_handle.write('**************{:0>2d}**************\n'.format(i + 1))
        # section
        file_handle.write('版面：{}\n'.format(self.section[i]))
        # title
        file_handle.write('标题：{}\n'.format(self.title[i]))
        # url
        file_handle.write('地址：{}\n'.format(self.url[i]))

    def write_tail(self, file_handle):
        file_handle.write('=' * 10 + self.end_mark + '=' * 10)

    def save(self):
        if self.is_recorded():
            return

        if len(self.title) != len(self.url):
            logger.error('title len not equal to url!, date{}'.format(datetime.strftime(self.date, '%Y%m%d')))
            return

        file_handle = open(self.path, 'w', encoding='utf-8')

        self.write_head(file_handle)

        for i in range(len(self.title)):
            self.write_single(file_handle, i)

        self.write_tail(file_handle)
        file_handle.close()


if __name__ == '__main__':
    result = PostInfo('ad')
    result.title.append('csh')
    result.url.append('123')
    result.section = '01 要闻'

    result.save()
