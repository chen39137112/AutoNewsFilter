import requests
from datetime import datetime
from bs4 import BeautifulSoup
from SaveResult import PostInfo
from utils import logger, KEY, trace_debug


def gm_get_url(date, section, i):
    if len(date) == 0:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y%m%d')
    date_str1 = datetime.strftime(date, '%Y-%m/%d')
    date_str2 = datetime.strftime(date, '%Y%m%d')
    return 'https://epaper.gmw.cn/gmrb/html/{}/nw.D110000gmrb_{}_{}-{:02d}.htm'.format(date_str1, date_str2, i, section)


@trace_debug
def gm_check_one_day(date=''):
    post_info = PostInfo('gm', date)
    if post_info.is_recorded():
        print(f"Guangming daily already checked for {date if len(date) > 0 else 'today'}!")
        return

    section = 1
    while True:
        i = 0
        while True:
            i += 1
            url = gm_get_url(date, section, i)
            resp = requests.get(url)
            if resp.status_code == 404:
                break
            html = resp.content.decode('utf-8')

            soup = BeautifulSoup(html, 'html.parser')
            article = soup.find_all('div', {'id': 'articleContent'})
            if len(article) == 0:
                break
            if KEY in article[0].text:
                post_info.title.append(soup.find('title').contents[0])
                post_info.url.append(url)
                post_info.section.append('第' + soup.find('div', {'class': 'ban_t'}).text.strip().split('\r')[0])
                logger.info("find it!" + url)

        if i == 1:
            # 防跨版导致中断
            url = gm_get_url(date, section + 1, i)
            resp = requests.get(url)
            if resp.status_code == 404:
                break
        section += 1

    post_info.save()


if __name__ == '__main__':
    gm_check_one_day('20240305')
    pass
