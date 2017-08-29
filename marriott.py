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
		self.hotels = []
		self._params = {}
		self.formatParams(params)
		

	def formatParams(self,params):
		if 'day_num' not in params.keys():
			params['day_num'] = 1

		if 'day_cin' in params.keys():
			day_cin= params['day_cin'][0:4] + '-' + params['day_cin'][4:6] + "-" + params['day_cin'][6:8]
		else:
			day_cin = "2017-08-27"

		if 'day_out' in params.keys():
			day_out = params['day_out'][0:4] + '-' + params['day_out'][4:6] + "-" + params['day_out'][6:8]
		else:
			day_out= params['day_cin'][0:4] + "-" + params['day_cin'][4:6] + "-" + str(int(params['day_cin'][6:8]) + params['day_num'])

		self._params['fromDate'] = day_cin
		self._params['toDate']   = day_out

		self._params['destinationAddress.destination'] = params['place'] if 'place' in params.keys() else"Shanghai"

		self._params['lengthOfStay'] = params['day_num']
		self._params['recordsPerPage'] = params['per_page'] if 'per_page' in params.keys() else 40
		self._params['clusterCode'] = params['code'] if 'code' in params.keys() else ""


	def geneUrl(self):
		self.url = self._url + '?' + urllib.parse.urlencode(self._params)

	def getSource(self):
		#print("正在打开网页：" + self.url)
		self.req = requests.get (self.url, headers = self._headers,  cookies = self._cookies)
		self.body = html.fromstring(self.req.text)
		self.soup = BeautifulSoup(self.req.text, 'lxml')

	def parseSoup(self):
		table = self.soup.find(id = 'comparison-form')
		items = table.find_all(_class = "merch-property-records")
		items = table.select(".merch-property-records")
		hotels = []
		for item in items:
			hotel = {}
			#hotel_name = item.find('h3')
			hotel['unique_id'] = item['id'].split('-')[2]
			hotel['hotel_name_cn'] = item.h3.a['title']
			hotel['hotel_name_en'] = item.h3.span.text
			#hotel['address'] = item.find(class_= "m-hotel-address").text.strip().replace('\t','').replace('\n','')
			hotel['price'] = int(item.find(class_ = "t-price").text.strip().replace(',',''))
			hotels.append(hotel)

		print('Total MT:'+str(len(hotels))+'!!')
		self.hotels = hotels

	def getHotels(self):
		self.geneUrl()
		self.getSource()
		self.parseSoup()
		return self.hotels


	def getMonth(self):
		self.monthRate = {}
		

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

