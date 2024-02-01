import requests
from datetime import datetime
from bs4 import BeautifulSoup
from SaveResult import PostInfo
from utils import logger, KEY, trace_debug


def ad_get_url(date, section):
    if len(date) == 0:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y%m%d')
    date_str = datetime.strftime(date, '%Y%m/%d')
    return "https://szb.ahnews.com.cn/ahrb/layout/{}/node_{:0>2d}.html".format(date_str, section)


def ad_get_article_url(href):
    href = href[href.find('/content'):]
    return 'https://szb.ahnews.com.cn/ahrb' + href


@trace_debug
def ad_check_one_day(date=''):
    post_info = PostInfo('ad', date)
    if post_info.is_recorded():
        print(f"Anhui daily already checked for {date if len(date) > 0 else 'today'}!")
        return

    section = 1
    while True:
        url = ad_get_url(date, section)
        resp = requests.get(url)
        if resp.status_code == 404:
            # 防跨版导致中断
            section += 1
            url = ad_get_url(date, section)
            resp = requests.get(url)
            if resp.status_code == 404:
                break

        html = resp.content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        news_list = [news['href'] for news in soup.find('div', {'class': 'newslist'}).find_all('a')]

        for href in news_list:
            article_url = ad_get_article_url(href)
            article = requests.get(article_url)
            html = article.content.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            article = soup.find_all('body')

            if KEY in article[-1].text:
                post_info.title.append(soup.find('title').contents[0])
                post_info.url.append(url + '#' + href[href.rfind('/') + 1: href.rfind('.')])
                post_info.section.append("第{:0>2d}版".format(section))
                logger.info("find it!" + article_url)

        section += 1

    post_info.save()
