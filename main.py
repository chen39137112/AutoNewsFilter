# coding=utf-8
from os import path

# from Browser import Driver
from PeopleDaily import pd_check_one_day
from AnhuiDaily import ad_check_one_day


def print_interface():
	file_name = 'config/interface_pic.txt'
	file_path = path.join(path.dirname(__file__), file_name)
	with open(file_path, 'r') as f:
		stdout = f.readline()
		while stdout:
			print(stdout, end='')
			stdout = f.readline()


if __name__ == '__main__':
	print_interface()
	target = input("要检查的报纸(1-人民日报，2-安徽日报，else-全部):")
	check_date = input("请输入要检查的日期(e.g. 20200907):")
	# driver = Driver()
	if target != '2':
		print('开始检查人民日报：')
		pd_check_one_day(check_date)
		print('检查完毕！')
	if target != '1':
		print('开始检查安徽日报：')
		ad_check_one_day(check_date)
		print('检查完毕！')
