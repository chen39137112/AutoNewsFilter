from datetime import datetime
from bs4 import BeautifulSoup
from SaveResult import PostInfo
from utils import logger, KEY, trace_debug, url_get


def pd_get_url(date, section, i):
    if len(date) == 0:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y%m%d')
    date_str1 = datetime.strftime(date, '%Y-%m/%d')
    date_str2 = datetime.strftime(date, '%Y%m%d')
    return "http://paper.people.com.cn/rmrb/html/{}/nw.D110000renmrb_{}_{}-{:02d}.htm".format(date_str1, date_str2, i,
                                                                                              section)


@trace_debug
def pd_check_one_day(date=''):
    post_info = PostInfo('pd', date)
    if post_info.is_recorded():
        print(f"People daily already checked for {date if len(date) > 0 else 'today'}!")
        return

    section = 1
    while True:
        i = 0
        while True:
            i += 1
            url = pd_get_url(date, section, i)
            resp = url_get(url)
            if resp.status_code == 404:
                break
            html = resp.content.decode('utf-8')

            soup = BeautifulSoup(html, 'html.parser')
            article = soup.find_all('div', {'id': 'articleContent'})
            if len(article) == 0:
                logger.error("empty article : " + url)
                continue
            if KEY in article[0].text:
                post_info.title.append(soup.find('title').contents[0])
                post_info.url.append(url)
                post_info.section.append(soup.find('p', {'class': 'left ban'}).contents[0])
                logger.info("find it!" + url)

        if i == 1:
            # 防跨版导致中断
            url = pd_get_url(date, section + 1, i)
            resp = url_get(url)
            if resp.status_code == 404:
                break
        section += 1

    post_info.save()

if __name__ == '__main__':
    pd_check_one_day("20240401")