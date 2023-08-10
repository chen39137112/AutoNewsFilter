from datetime import datetime
from tqdm import tqdm
from utils import logger, KEY
from SaveResult import PostInfo

BASE_URL = 'http://paper.people.com.cn/rmrb/html/{}-{:0>2d}/{:0>2d}/nbs.D110000renmrb_01.htm'
SWIPER_XPATH = '/html/body/div[2]/div[2]/div[2]/div/*'
NEWS_XPATH = '/html/body/div[2]/div[2]/div[3]/ul/*'


def pd_get_url(date=''):
    if len(date) == 0:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y%m%d')
    return BASE_URL.format(date.year, date.month, date.day)


def pd_back_to_content(driver):
    driver.click('/html/body/div[2]/div[2]/div[3]/div[1]/span/a')


def pd_check_news(driver, post_info, section_name):
    news_list = driver.find_elements(NEWS_XPATH)
    for j, news in enumerate(news_list):
        driver.click(f'/html/body/div[2]/div[2]/div[3]/ul/li[{j + 1}]/a')
        paragraphs = driver.find_elements('//*[@id="ozoom"]/*')
        for para in paragraphs:
            if KEY in para.text:
                post_info.title.append(driver.driver.title)
                post_info.url.append(driver.driver.current_url)
                post_info.section.append(section_name)
                logger.info("find it!" + driver.driver.current_url)
                print("find it!" + driver.driver.current_url)
                break
        pd_back_to_content(driver)


# 查询一页，ex：01 要闻
def pd_check_swiper(driver, post_info):
    section = driver.find_element('/html/body/div[2]/div[1]/div[2]/p[1]')

    pd_check_news(driver, post_info, section.text)


def pd_check_one_day(driver, date=''):
    post_info = PostInfo('pd', date)
    if post_info.is_recorded():
        print(f"People daily already checked for {date if len(date) > 0 else 'today'}!")
        return

    base_url = pd_get_url(date)
    driver.get(base_url)
    section_num = len(driver.find_elements(SWIPER_XPATH))

    for i in tqdm(range(1, section_num)):
        pd_check_swiper(driver, post_info)
        # 去到下一页
        driver.click('/html/body/div[2]/div[2]/div[2]/div/div[{}]/a'.format(i + 1))
    else:
        pd_check_swiper(driver, post_info)
    post_info.save()


if __name__ == '__main__':
    pass
