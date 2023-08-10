# coding=utf-8
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import speed_limit

warnings.filterwarnings("ignore")


class Driver:
	chrome_options = webdriver.ChromeOptions()
	prefs = {'profile.managed_default_content_settings.images': 2, 'permissions.default.stylesheet': 2}
	chrome_options.add_experimental_option('prefs', prefs)
	
	def __init__(self):
		self.driver = webdriver.Chrome(options=self.chrome_options)
		self.driver.implicitly_wait(5)
	
	def get(self, url):
		self.driver.get(url)
	
	def find_elements(self, xpath):
		return self.driver.find_elements(By.XPATH, xpath)
	
	def find_element(self, xpath):
		return self.driver.find_element(By.XPATH, xpath)
	
	def find_elements_by_name(self, name):
		return self.driver.find_elements(By.CLASS_NAME, name)
	
	def find_element_by_css(self, name):
		return self.driver.find_element(By.CSS_SELECTOR, name)
	
	def find_elements_by_name(self, name):
		return self.driver.find_elements(By.CLASS_NAME, name)
	
	@speed_limit
	def click(self, xpath):
		self.driver.find_element(By.XPATH, xpath).click()


if __name__ == '__main__':
	driver = webdriver.Chrome()
	driver.get('https://szb.ahnews.com.cn/ahrb/layout/202212/02/node_01.html#c947867')
	
	pass
