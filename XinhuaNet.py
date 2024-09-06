from bs4 import BeautifulSoup
from SaveResult import PostInfo
from utils import logger, KEY, trace_debug, url_get


def get_hrefs(hrefs, url):
    resp = url_get(url)
    html = resp.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    if 'ah' in url:
        target = soup.find("ul", {'class': 'showMoreN'})
    else:
        target = soup.find("div", {'id': 'focus'})
    for a in target.find_all("a"):
        hrefs.append(a.attrs['href'])


@trace_debug
def xh_check_one_day(date=''):
    logger.info("check xinhua news!")
    post_info = PostInfo('xh', date)
    hrefs = []
    get_hrefs(hrefs, "http://www.news.cn/")
    get_hrefs(hrefs, "http://ah.news.cn/news/yaowen.htm")
    get_hrefs(hrefs, "http://ah.news.cn/news/anhui.htm")

    for href in hrefs:
        if href.startswith("../"):
            href = "http://ah.news.cn" + href[2:]
        resp = url_get(href)
        html = resp.content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        if "sikepro" in href:
            target = soup.find("div", {'id': 'detail'})
        else:
            target = soup.find("span", {'id': 'detailContent'})

        # 可能是视频类新闻
        if target is None:
            logger.warning(href + ' miss!')
            continue

        if KEY in target.text:
            post_info.title.append(soup.find('title').text.strip())
            post_info.url.append(href)
            post_info.section.append("新华网首页-焦点")
            logger.info("find it!" + href)

    post_info.save()

if __name__ == '__main__':
    xh_check_one_day()