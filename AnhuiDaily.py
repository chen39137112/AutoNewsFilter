# coding=utf-8
from datetime import datetime
from selenium.common import NoSuchElementException, ElementNotInteractableException
import requests
import re
from tqdm import tqdm

from utils import logger, KEY
from SaveResult import PostInfo

BASE_URL = 'https://szb.ahnews.com.cn/ahrb/layout/{}{:0>2d}/{:0>2d}/node_01.html'
NEWS_XPATH = '/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/ul'
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}


def ad_get_url(date=''):
	if len(date) == 0:
		date = datetime.now()
	else:
		date = datetime.strptime(date, '%Y%m%d')
	return BASE_URL.format(date.year, date.month, date.day)


def ad_back_to_content(driver):
	driver.click('/html/body/div[2]/div[1]/div[2]/div[2]/a')


def ad_get_news_url(current_url):
	"""
	https://szb.ahnews.com.cn/ahrb/layout/202212/02/node_01.html#c947867
	->
	https://szb.ahnews.com.cn/ahrb/content/202212/02/c947867.html
	"""
	url_parts = current_url.split('layout')
	pattern = r'node_\d\d.html#'
	result = re.split(pattern, url_parts[1])
	news_url = url_parts[0] + 'content' + result[0] + result[1] + '.html'
	
	return news_url


def ad_check_one_title(driver, post_info, section_name, i):
	driver.click(f'/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/ul/li[{i}]/h3/a')
	# XML无法定位，采用直接发送http请求的方式获取文章内容
	news_url = ad_get_news_url(driver.driver.current_url)
	try:
		resp = requests.get(url=news_url, headers=HEADERS)
	except Exception as e:
		logger.error(f"{e} error occured!")
		logger.error(f"get info from {news_url} out of time, try again!")
		resp = requests.get(url=news_url, headers=HEADERS)
	
	text = resp.content.decode('utf-8')
	if KEY in text:
		post_info.title.append(driver.driver.title)
		post_info.url.append(driver.driver.current_url)
		post_info.section.append(section_name)
		logger.info("find it!" + driver.driver.current_url)
		print("find it!" + driver.driver.current_url)


def ad_check_news(driver, post_info, section_name):
	i = 1
	try:
		while True:
			ad_check_one_title(driver, post_info, section_name, i)
			ad_back_to_content(driver)
			i += 1
	except NoSuchElementException as e:
		logger.info(f"check news finish, section({section_name})count({i - 1})error({e})")
	except ElementNotInteractableException as e:
		logger.info(f"check news finish, section({section_name})count({i - 1})error({e})")


# 查询一页，ex：01 要闻
def ad_check_swiper(driver, post_info):
	section = driver.find_element('/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/em')
	ad_check_news(driver, post_info, section.text)


def ad_check_one_day(driver, date=''):
	post_info = PostInfo('ad', date)
	if post_info.is_recorded():
		print(f"Anhui daily already checked for {date if len(date) > 0 else 'today'}!")
		return
	
	base_url = ad_get_url(date)
	driver.get(base_url)
	pbar = tqdm(total=len(driver.find_elements_by_name('layoutNum')))

	while True:
		ad_check_swiper(driver, post_info)
		pbar.update(1)
		# 去到下一页
		if pbar.last_print_n != pbar.total:
			driver.click('/html/body/div[2]/div[1]/div[2]/div[4]/a')
			continue
		break
	post_info.save()


if __name__ == '__main__':
	current_url = 'https://szb.ahnews.com.cn/ahrb/layout/202212/02/node_01.html#c947867'
	news_url = ad_get_news_url(current_url)
	print(news_url)
