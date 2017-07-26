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

resp = requests.get(_url, headers= _headers)
cookies = resp.cookies    

url ="http://www.marriott.com.cn/search/submitSearch.mi?searchType=InCity&groupCode=&searchRadius=&poiName=&poiCity=%E5%8C%97%E4%BA%AC&recordsPerPage=20&for-hotels-nearme=%E9%9D%A0%E8%BF%91&destinationAddress.destination=%E5%8C%97%E4%BA%AC%2C+China&singleSearch=true&singleSearchAutoSuggest=false&autoSuggestItemType=Unmatched&clickToSearch=false&destinationAddress.latitude=39.906011&destinationAddress.longitude=116.387911&destinationAddress.cityPopulation=0.0&destinationAddress.cityPopulationDensity=0.0&destinationAddress.city=%E5%8C%97%E4%BA%AC&destinationAddress.stateProvince=&destinationAddress.country=CN&airportCode=&fromToDate=7+%E6%9C%88+28%E6%97%A5%2C+%E5%91%A8%E5%9B%9B&fromToDate_submit=2017-07-24&fromDate=2017-07-29&toDate=2017-07-30&lengthOfStay=1&roomCountBox=1&roomCount=1&guestCountBox=1&guestCount=1&clusterCode=none&corporateCode="
basic_url = "http://www.marriott.com.cn/search/submitSearch.mi"
r = requests.get (url, headers = _headers,  cookies = cookies)
#print(r.text)
#body = html.fromstring(r.text)

#sub = body.xpath('//span[@class="t-price"]')
#print(sub[0].text)
'''
soup = BeautifulSoup(r.text, 'lxml')

#print(soup.prettify())

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

#print(hotels)
'''
parsed_url = urllib.parse.urlparse(url)
params = urllib.parse.parse_qs(parsed_url.query,True)

#print(params)

params['poiCity'][0] = '上海'
#params['formData'][0] = '2017-7-29'
params['destinationAddress.city'][0] = '上海'
params['destinationAddress.destination'][0] = '上海,China'
params['destinationAddress.latitude'][0] = ''
params['destinationAddress.longitude'][0] = ''

print(params)


r_sh = requests.get (basic_url, data = params,  headers = _headers,  cookies = cookies)


soup = BeautifulSoup(r_sh.text, 'lxml')

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
'''
url_params = urllib.parse.urlencode(params)
new_url = basic_url + "?" + url_params
print(new_url)
print(hotels)