import time
import sys,io
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import datetime
import sys 
from pypinyin import lazy_pinyin
from lxml import etree
import pandas as pd
import random
# reload(sys) 
# sys.setdefaultencoding( "utf-8" )
import sys,io
def setup_io():
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)
setup_io()


class meituan_m_web():
	"""docstring for meituan_m_web"""
	def __init__(self,city):
		# self.city = city
		self.url = url

	def init_brower(self):
		#driver_path='/home/reocar/Crawling/driver/chromedriver_linux'
		driver_path='/Users/reocar/Documents/chromedriver/chromedriver'
		option = webdriver.ChromeOptions()
		# option.add_argument("headless")
		#option.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
		option.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
		option.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
		option.add_argument('disable-infobars')
		mobile_emulation = {"deviceName":"iPhone X"}
		# option.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 8.0; MI 6 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044204 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060736)')
		# ua = 'Mozilla/5.0 (Linux; Android 8.0; MI 6 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044204 Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060736)'
		option.add_experimental_option("mobileEmulation", mobile_emulation)
		browser=webdriver.Chrome(driver_path,options=option)
		browser.implicitly_wait(6)
		# city_info=self.get_city_info(start_date,end_date)
		print('begin!')
		return browser

	def __wait_rangdom_time(self,end):
		return random.randint(2,end)

	def __show_wait(self,located_type,element,browser,time):
		try:
			element = WebDriverWait(browser,time).until(
				EC.presence_of_element_located((located_type, element))
			)
			return  element
		except:
			print('can not find element: '+element )
			return  False

	def __is_element_exist(self,located_type,element,browser):
		s = browser.find_elements(located_type,element)
		if(len(s) == 0):
			print("元素未找到:%s"%element) 
			return False
		elif(len(s) == 1):
			return True
		else:
			print("找到%s个元素：%s"%(len(s),element)) 
			return False

	def parse_store_info(self,browser):
		html=etree.HTML(browser.page_source)
		name_xpath = '//*[@class="cont"]/dl/dd[1]/div/h1/text()'
		score_xpath = '//*[@class="cont"]//*[@class="star-text"]/text()'
		location_xpath = '//*[@class="cont"]//*[@class="poi-address"]/text()'
		tel_xpath = '//*[@class="cont"]//*[@class="react poi-info-phone"]/@data-tele'
		try:
			name = html.xpath(name_xpath)[0]
		except:
			name = 'None'
		try:
			score = html.xpath(score_xpath)[0]
		except:
			score = 'None'
		try:
			location = html.xpath(location_xpath)[0]
		except:
			location = 'None'
		try:
			tel = html.xpath(tel_xpath)[0]
		except:
			tel = 'None'
		print(name,score,location,tel)
		data = {}
		data['name']=[name]
		data['score']=[score]
		data['location']=[location]
		data['tel']=[tel]
		data_df=pd.DataFrame(data)

		return data_df

	def save_date(self,name,score,location,tel):
		data = pd.DataFrame()
		data['name']=name
		data['score']=score
		data['location']=location
		data['tel']=tel
		data=data[['name','score','location','tel']]
		return data

	def action(self):
		browser = self.init_brower()
		print(url)
		browser.get(url)
		time.sleep(2)
		el = browser.find_element_by_class_name('i-link').click()

		# 选择默认排序
		sort_xpath = '//*[@class="dropdown-toggle caret sort"]/span'
		self.__show_wait(By.XPATH,sort_xpath,browser,60).click()
		# 选择离我最近
		distinct_xpath = '//*[@data-sort-id="distance"]/span'
		self.__show_wait(By.XPATH,distinct_xpath,browser,60).click()
		# time.sleep()

		until_xpath = '//*[@id="deals"]/dl/dd[1]/dl[20]'
		self.__show_wait(By.XPATH,until_xpath,browser,60)


		time.sleep(20)
		try:
			cancel_xpath = '//*[@id="msg"]/button'
			self.__show_wait(By.XPATH,cancel_xpath,browser,10).click()
		except:
			pass


		page = 1

		finish=pd.DataFrame()
		while True:
			store_list_xpath = '//*[@id="deals"]/dl/dd[1]/dl'

			el2 = browser.find_elements_by_xpath(store_list_xpath)
			print("第%d页" % page)
			time.sleep(30)
			for i in range(1,len(el2)+1):
				store_xpath = '//*[@id="deals"]/dl/dd[1]/dl[%s]/dd[1]' % i
				self.__show_wait(By.XPATH,store_xpath,browser,60).click()
				time.sleep(self.__wait_rangdom_time(4))

				# 解析网页
				data = self.parse_store_info(browser)
				finish = finish.append(data,ignore_index=0)
				return_xpath = '//*[@id="deal-list"]/header/div[1]/a'
				self.__show_wait(By.XPATH,return_xpath,browser,60).click()
				time.sleep(2+self.__wait_rangdom_time(3))
			file_name = 'meituan.csv'
			finish.to_csv(file_name,index=0)

			node_next_page_xpath='//*[@id="deals"]/dl/dd[2]/div/a[2]'
			try:
				if_next_page=browser.find_elements_by_xpath(node_next_page_xpath)[0].get_attribute("herf")
			except:
				break;
			# 点击下一页
			browser.find_elements_by_xpath(node_next_page_xpath)[0].click()
			page = page + 1
		

		print("结束")
		browser.close()


if __name__ == '__main__':
	city = '广州'
	series =tuple(lazy_pinyin(city))
	city_py=('%s'*len(series))% series
	url = 'https://i.meituan.com/s/'+str(city_py)+'-租车'
	meituan = meituan_m_web(url)
	meituan.action()



