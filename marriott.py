#Coding = 'utf-8'
#filename:Marriott

import requests
import urllib
from urllib import parse as urlparse
from lxml import html
from bs4 import BeautifulSoup

class Marriott():
	def __init__(self,params):
		self.basic_url = 'http://www.marriott.com.cn/search/findHotels.mi'
		self._url = "http://www.marriott.com.cn/search/submitSearch.mi"
		self._headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Connection':'keep-alive',
		'Host':'www.marriott.com.cn',
		'Referer':'http://www.marriott.com.cn/default.mi',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
		}
		self._cookies = requests.get(self.basic_url, headers= self._headers).cookies
		self._params = {}
		self.dayin_list = []
		self.dayout_list = []
		self.hotels = []
		self.hotelRateDetial = {}
		self.formatParams(params)
		

	def getDayList(self,params):
		self.day_num = params['day_num']
		if 'day_cin' in params.keys():
			year = int(params['day_cin'][0:4])
			month = int(params['day_cin'][4:6])
			day = int(params['day_cin'][6:8])
		else:
			day_cin = "2017-08-27"#should get today num

		monthnum = [31,28 if year%4 else 29,31,30,31,30,31,31,30,31,30,31]

		for i in range(0,self.day_num):
			self.dayin_list.append(str(year) + "-" + ('0' if month < 10 else '')+str(month) + '-' + ('0' if day < 10 else '') + str(day))
			if day < monthnum[month-1]:
				day = day + 1
			else:
				year = year + 1 if month == 12 else year
				month = ( month + 1 ) if month < 12 else 1
				day = 1
			self.dayout_list.append(str(year) + "-" + ('0' if month < 10 else '')+str(month) + '-' + ('0' if day < 10 else '') + str(day))

	def formatParams(self,params):
		if 'day_num' not in params.keys():
			params['day_num'] = 30

		self.getDayList(params)
		self._params['fromDate'] = self.dayin_list[0]
		self._params['toDate']   = self.dayout_list[0]

		self._params['destinationAddress.destination'] = params['place'] if 'place' in params.keys() else"Shanghai"

		self._params['lengthOfStay'] = 1
		self._params['recordsPerPage'] = params['per_page'] if 'per_page' in params.keys() else 40
		self._params['clusterCode'] = params['code'] if 'code' in params.keys() else ""

	def getSource(self):
		self.url = self._url + '?' + urllib.parse.urlencode(self._params)
		print("正在打开网页：" + self.url)
		self.req = requests.get (self.url, headers = self._headers,  cookies = self._cookies)
		self.body = html.fromstring(self.req.text)
		self.soup = BeautifulSoup(self.req.text, 'lxml')

	def parseHotels(self):
		table = self.soup.find(id = 'comparison-form')
		items = table.find_all(_class = "merch-property-records")
		items = table.select(".merch-property-records")
		for item in items:
			hotel = {}
			#hotel_name = item.find('h3')
			hotel['unique_id'] = item['id'].split('-')[2]
			hotel['hotel_name_cn'] = item.h3.a['title']
			hotel['hotel_name_en'] = item.h3.span.text
			#hotel['address'] = item.find(class_= "m-hotel-address").text.strip().replace('\t','').replace('\n','')
			hotel['price'] = int(item.find(class_ = "t-price").text.strip().replace(',',''))
			self.hotelRateDetial[hotel['unique_id']] = {
				'name_en': item.h3.span.text,
				'name_cn': item.h3.a['title'],
				'price':{
				self._params['fromDate'].replace('-','')[2:8]:int(item.find(class_ = "t-price").text.strip().replace(',',''))
				},
			}
			hotel['detail'] = self.hotelRateDetial[hotel['unique_id']]
			self.hotels.append(hotel)

		print('Total MT:'+str(len(self.hotels))+'!!')

	def parseMonthDetail(self):
		table = self.soup.find(id = 'comparison-form')
		items = table.find_all(_class = "merch-property-records")
		items = table.select(".merch-property-records")
		for item in items:
			unique_id = item['id'].split('-')[2]
			self.hotelRateDetial[unique_id]['price'][self._params['fromDate'].replace('-','')[2:8]] = int(item.find(class_ = "t-price").text.strip().replace(',',''))

	def getHotels(self):
		self.getSource()
		self.parseHotels()
		return self.hotels

	def getMonth(self):
		if(self.hotels == []):
			self.getHotels()
		for i in range(1,self.day_num):
				self._params['fromDate'] = self.dayin_list[i]
				self._params['toDate']   = self.dayout_list[i]
				self.getSource()
				self.parseMonthDetail()
		self.save()

	def save(self):
		return

'''
	def getMonthRate(self):
		self.url = 'http://www.marriott.com.cn/reservation/availabilitySearch.mi?propertyCode=SHACA&isSearch=true&isRateCalendar=true&flexibleDateSearchRateDisplay=false&fromDate=17-09-01&toDate=17-09-02&incentiveType=false&numberOfRooms=1&numberOfGuests=2'
		self.session = requests.Session()
		self.session.get(self.basic_url,headers = self._headers)
		self.newbody = self.session.get(self.url)
		f = open('new1.html','w')
		f.write(self.newbody.text)
		f.close

		self.url = "http://www.marriott.com.cn/reservation/availabilitySearch.mi?istl_enable=true&istl_data"
		self.newbody = self.session.get(self.url)
		f = open('new2.html','w')
		f.write(self.newbody.text)
		f.close
'''

#http://www.starwoodhotels.com/preferredguest/search/results/detail.html?arrivalDate=9%2F27%2F2017&departureDate=9%2F28%2F2017&country=CN&city=Shanghai