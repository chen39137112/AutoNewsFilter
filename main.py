# coding=utf-8
import os
from os import path
from datetime import datetime, timedelta
from time import sleep


from PeopleDaily import pd_check_one_day
from AnhuiDaily import ad_check_one_day
from GuangmingDaily import gm_check_one_day


def print_interface():
	file_name = 'config/interface_pic.txt'
	file_path = path.join(path.dirname(__file__), file_name)
	with open(file_path, 'r') as f:
		stdout = f.readline()
		while stdout:
			print(stdout, end='')
			stdout = f.readline()


if __name__ == '__main__':
	if os.name == 'nt':
		print_interface()
		target = input("要检查的报纸(1-人民日报，2-安徽日报，3-光明日报，else-全部):")
		check_date = input("请输入要检查的日期(e.g. 20200907):")

		if target == '1':
			print('开始检查人民日报：')
			pd_check_one_day(check_date)
			print('检查完毕！')
		elif target == '2':
			print('开始检查安徽日报：')
			ad_check_one_day(check_date)
			print('检查完毕！')
		elif target == '3':
			print('开始检查光明日报：')
			gm_check_one_day(check_date)
			print('检查完毕！')
		else:
			print('开始检查人民日报：')
			pd_check_one_day(check_date)
			print('检查完毕！')

			print('开始检查安徽日报：')
			ad_check_one_day(check_date)
			print('检查完毕！')

			print('开始检查安徽日报：')
			ad_check_one_day(check_date)
			print('检查完毕！')

	elif os.name == 'posix':
		while True:
			today = datetime.today() + timedelta(hours=12)

			if today.hour == 7:
				pd_check_one_day(datetime.strftime(today, '%Y%m%d'))
				ad_check_one_day(datetime.strftime(today, '%Y%m%d'))
				gm_check_one_day(datetime.strftime(today, '%Y%m%d'))
				sleep(23 * 60 * 60)
			sleep(5 * 60)
	else:
		print('unknown system name!')
