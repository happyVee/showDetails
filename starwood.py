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
		self.hotels = []
		self._params = {}
		self.formatParams(params)
		
	def formatParams(self,params):
		if 'day_cin' in params.keys():
			day_cin = params['day_cin'][0:4] + '年' + params['day_cin'][4:6] + "月" + params['day_cin'][6:8] + "日"
		else:
			day_cin = "2017年08月26日"

		if 'day_out' in params.keys():
			day_out = params['day_out'][0:4] + '年' + params['day_out'][4:6] + "月" + params['day_out'][6:8] + "日"
		else:
			day_out= params['day_cin'][0:4] + '年' + params['day_cin'][4:6] + "月" + str(int(params['day_cin'][6:8]) + params['day_num']) + "日"

		self._params['arrivalDate']   = day_cin
		self._params['departureDate'] = day_out

		self._params['country'] = 'CN'
		self._params['city'] = params['place'] if 'place' in params.keys() else "Shanghai"

	def geneUrl(self):
		self.url = self._url + '?' + urllib.parse.urlencode(self._params)

	def getSource(self):
		#print("正在打开网页：" + self.url)
		self.req = requests.get (self.url, headers = self._headers,  cookies = self._cookies)
		self.body = html.fromstring(self.req.text)
		self.soup = BeautifulSoup(self.req.text, 'lxml')

	def parseSoup(self):
		table = self.soup.find(id = 'primary2' )
		items = table.select('.propertyOuter')
		hotels = []

		for item in items:
			if(item.div['data-have-rates']!="false"):
				hotel = {}
				#hotel_name = item.find('h3')
				hotel['hotel_name_cn'] = item.h2.a.text.strip().replace('\t','').replace('\n','')
				hotel['hotel_name_en'] = item.h2.a.find_next_siblings()[0].text.strip().replace('\t','').replace('\n','')
				#hotel['address'] = item.find(class_= "m-hotel-address").text.strip().replace('\t','').replace('\n','')
				hotel['price'] = int(item.find(class_ = "currency").text.replace(',','').split(' ')[1])
				hotels.append(hotel)

		print('Total SPG:'+str(len(hotels))+'!!')
		self.hotels = hotels


	def getHotels(self):
		self.geneUrl()
		self.getSource()
		self.parseSoup()
		return self.hotels


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