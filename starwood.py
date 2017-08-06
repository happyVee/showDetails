import requests
import urllib
from urllib import parse as urlparse
from lxml import html
from bs4 import BeautifulSoup

_url = 'http://www.starwoodhotels.com/preferredguest/search/index.html'

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

resp = requests.get(_url, headers= _headers)
cookies = resp.cookies    


#url = 'http://www.starwoodhotels.com/preferredguest/search/results/detail.html?country=CN&stateProvince=SHA&city=Shanghai&arrivalDate=17%E5%B9%B408%E6%9C%8823%E6%97%A5&departureDate=17%E5%B9%B408%E6%9C%8824%E6%97%A5'
url = 'http://www.starwoodhotels.com/preferredguest/search/results/detail.html?country=CN&stateProvince=SHA&city=Shanghai&arrivalDate=17年08月23日&departureDate=17年08月24日'

#url = "http://www.marriott.com.cn/search/submitSearch.mi?destinationAddress.destination=China&fromDate=2017-07-29&toDate=2017-07-30&lengthOfStay=1&recordsPerPage=40&clusterCode=oxd"
#basic_url = "http://www.marriott.com.cn/search/submitSearch.mi"
r = requests.get (url, headers = _headers,  cookies = cookies)

body = html.fromstring(r.text)
soup = BeautifulSoup(r.text, 'lxml')
#print(soup)


table = soup.find(id = 'primary2' )
items = table.select('.propertyOuter')
hotels = []

for item in items:
	if(item.div['data-have-rates']!="false"):
		hotel = {}
		#hotel_name = item.find('h3')
		hotel['hotel_name_cn'] = item.h2.a.text.strip().replace('\t','').replace('\n','')
		hotel['hotel_name_en'] = item.h2.a.find_next_siblings()[0].text.strip().replace('\t','').replace('\n','')
		#hotel['address'] = item.find(class_= "m-hotel-address").text.strip().replace('\t','').replace('\n','')
		hotel['price'] = item.find(class_ = "currency").text.replace(',','').split(' ')[1]
		hotels.append(hotel)
print('一共有:'+str(len(hotels))+'家')
#print(hotels)

for i in hotels:
    for k,v in i.items():
        print('{k}:{v}'.format(k=k,v=v))
    print()

#print(soup.prettify())
'''
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


url = 'http://www.starwoodhotels.com/preferredguest/search/results/detail.html?country=CN&stateProvince=SHA&city=Shanghai&arrivalDate=17%E5%B9%B408%E6%9C%8823%E6%97%A5&departureDate=17%E5%B9%B408%E6%9C%8824%E6%97%A5'

'''