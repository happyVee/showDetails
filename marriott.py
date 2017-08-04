import requests
import urllib
from urllib import parse as urlparse
from lxml import html
from bs4 import BeautifulSoup

_url = 'http://www.marriott.com.cn/search/findHotels.mi'

_headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Host':'www.marriott.com.cn',
'Referer':'http://www.marriott.com.cn/default.mi',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}



#r = requests.get (url, headers = _headers,  cookies = cookies)

#body = html.fromstring(r.text)
#soup = BeautifulSoup(r.text, 'lxml')

#print(soup.prettify())
def parsesoup(soup):
	table = soup.find(id = 'comparison-form')
	items = table.find_all(_class = "merch-property-records")
	items = table.select(".merch-property-records")
	hotels = []
	for item in items:
		hotel = {}
		#hotel_name = item.find('h3')
		hotel['hotel_name_cn'] = item.h3.a['title']
		hotel['hotel_name_en'] = item.h3.span.text
		#hotel['address'] = item.find(class_= "m-hotel-address").text.strip().replace('\t','').replace('\n','')
		hotel['price'] = int(item.find(class_ = "t-price").text.strip().replace(',',''))
		hotels.append(hotel)
	print('一共有:'+str(len(hotels))+'家')
	print(hotels)
	return hotels

def querydata(url,_headers,cookies):
	r = requests.get (url, headers = _headers,  cookies = cookies)
	body = html.fromstring(r.text)
	soup = BeautifulSoup(r.text, 'lxml')
	return soup

def getparams():
	queryinfo={
	'destinationAddress.destination':'Beijing',
	'fromDate': '2017-08-26',
	'toDate':'2017-08-27',
	'lengthOfStay':1,
	'recordsPerPage':20,
	'clusterCode':''
	}  

if __name__ == '__main__':
	cookies = requests.get(_url, headers= _headers).cookies

	basic_url = "http://www.marriott.com.cn/search/submitSearch.mi"
	url = basic_url + '?' + urllib.parse.urlencode(queryinfo)
	print(url)
	soup = querydata(url,_headers,cookies)
	parsesoup(soup)