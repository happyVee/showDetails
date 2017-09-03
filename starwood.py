#Coding = 'utf-8'
#filename:Starwood

import requests
import urllib
from urllib import parse as urlparse
from lxml import html
from bs4 import BeautifulSoup


class Starwood():
	def __init__(self,params):
		self.basic_url = 'http://www.starwoodhotels.com/preferredguest/search/index.html'
		self._url = "http://www.starwoodhotels.com/preferredguest/search/results/detail.html"
		self._headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Connection':'keep-alive',
		'Host':'www.starwoodhotels.com',
		'Referer':'http://www.starwoodhotels.com',
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
			year = int(params['day_cin'][2:4])
			month = int(params['day_cin'][4:6])
			day = int(params['day_cin'][6:8])
		else:
			day_cin = "09/15/2017"#should get today num

		monthnum = [31,28 if year%4 else 29,31,30,31,30,31,31,30,31,30,31]

		for i in range(0,self.day_num):
			self.dayin_list.append(str(year) +'年'+('0' if month < 10 else '')+str(month) + '月' + ('0' if day < 10 else '')+str(day) + '日')
			#self.dayin_list.append( ('0' if month < 10 else '') + str(month)+ '/' + ('0' if day < 10 else '') + str(day) + '/' + str(year))
			if day < monthnum[month-1]:
				day = day + 1
			else:
				year = year + 1 if month == 12 else year
				month = ( month + 1 ) if month < 12 else 1
				day = 1
			self.dayout_list.append(str(year) +'年'+('0' if month < 10 else '')+str(month) + '月' + ('0' if day < 10 else '')+str(day) + '日')
			#self.dayout_list.append( ('0' if month < 10 else '') + str(month)+ '/' + ('0' if day < 10 else '') + str(day) + '/' + str(year))
	
	def formatParams(self,params):
		if 'day_num' not in params.keys():
			self.day_num = 30
		else:
			self.day_num = params['day_num']

		self.getDayList(params)
		self._params['arrivalDate']   = self.dayin_list[0]
		self._params['departureDate'] = self.dayout_list[0]

		self._params['country'] = 'CN'
		self._params['city'] = params['place'] if 'place' in params.keys() else "Shanghai"

	def getSource(self):		
		self.url = self._url + '?' + urllib.parse.urlencode(self._params)
		print("正在打开网页：" + self.url)
		self.req = requests.get (self.url, headers = self._headers,  cookies = self._cookies)
		self.body = html.fromstring(self.req.text)
		self.soup = BeautifulSoup(self.req.text, 'lxml')

	def parseHotels(self):
		table = self.soup.find(id = 'primary2' )
		items = table.select('.propertyOuter')

		for item in items:
			if(item.div['data-have-rates']!="false"):
				hotel = {}
				#hotel_name = item.find('h3')
				hotel['unique_id'] = item.div['data-property-id']
				hotel['hotel_name_cn'] = item.h2.a.text.strip().replace('\t','').replace('\n','')
				hotel['hotel_name_en'] = item.h2.a.find_next_siblings()[0].text.strip().replace('\t','').replace('\n','')
				#hotel['address'] = item.find(class_= "m-hotel-address").text.strip().replace('\t','').replace('\n','')
				hotel['price'] = int(item.find(class_ = "currency").text.replace(',','').split(' ')[1])
				self.hotelRateDetial[hotel['unique_id']] = {
					'name_en': hotel['hotel_name_cn'],
					'name_cn': hotel['hotel_name_en'],
					'price':{
					self.changeDayFormat(self._params['arrivalDate']):int(item.find(class_ = "currency").text.replace(',','').split(' ')[1])
					},
				}
				hotel['detail'] = self.hotelRateDetial[hotel['unique_id']]
				self.hotels.append(hotel)

		print('Total SPG:'+str(len(self.hotels))+'!!')

	def parseMonthDetail(self):
		table = self.soup.find(id = 'primary2' )
		items = table.select('.propertyOuter')
		for item in items:
			if(item.div['data-have-rates']!="false"):
				unique_id = item.div['data-property-id']
				self.hotelRateDetial[unique_id]['price'][self.changeDayFormat(self._params['arrivalDate'])] = int(item.find(class_ = "currency").text.replace(',','').split(' ')[1])

	def getHotels(self):
		self.getSource()
		self.parseHotels()
		return self.hotels

	def getMonth(self):
		if(self.hotels == []):
			self.getHotels()
		for i in range(1,self.day_num):
				self._params['arrivalDate'] = self.dayin_list[i]
				self._params['departureDate']   = self.dayout_list[i]
				self.getSource()
				self.parseMonthDetail()
		self.save()

	def changeDayFormat(self,paramDay):
		return paramDay[0:2]+paramDay[3:5]+paramDay[6:8]

	def save(self):
		return


'''
#_url = 'http://www.starwoodhotels.com/preferredguest/search/index.html'

_headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Host':'www.starwoodhotels.com',
'Referer':'http://www.starwoodhotels.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}

#url = 'http://www.starwoodhotels.com/preferredguest/search/results/detail.html?country=CN&stateProvince=SHA&city=Shanghai&arrivalDate=17%E5%B9%B408%E6%9C%8823%E6%97%A5&departureDate=17%E5%B9%B408%E6%9C%8824%E6%97%A5'
url = 'http://www.starwoodhotels.com/preferredguest/search/results/detail.html?country=CN&stateProvince=SHA&city=Shanghai&arrivalDate=17年08月23日&departureDate=17年08月24日'

#url = "http://www.marriott.com.cn/search/submitSearch.mi?destinationAddress.destination=China&fromDate=2017-07-29&toDate=2017-07-30&lengthOfStay=1&recordsPerPage=40&clusterCode=oxd"

url = 'http://www.starwoodhotels.com/preferredguest/search/results/detail.html?country=CN&stateProvince=SHA&city=Shanghai&arrivalDate=17%E5%B9%B408%E6%9C%8823%E6%97%A5&departureDate=17%E5%B9%B408%E6%9C%8824%E6%97%A5'

'''