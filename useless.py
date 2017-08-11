
'''
#sub = body.xpath('//span[@class="t-price"]')
#print(sub[0].text)

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
'''

'''
#url ="http://www.marriott.com.cn/search/submitSearch.mi?searchType=InCity&groupCode=&searchRadius=&poiName=
&poiCity=%E5%8C%97%E4%BA%AC&recordsPerPage=20&for-hotels-nearme=%E9%9D%A0%E8%BF%91
&destinationAddress.destination=%E5%8C%97%E4%BA%AC%2C+China&singleSearch=true&singleSearchAutoSuggest=false
&autoSuggestItemType=Unmatched&clickToSearch=false&destinationAddress.latitude=39.906011
&destinationAddress.longitude=116.387911&destinationAddress.cityPopulation=0.0&destinationAddress.cityPopulationDensity=0.0
&destinationAddress.city=%E5%8C%97%E4%BA%AC&destinationAddress.stateProvince=&destinationAddress.country=CN&airportCode=
&fromToDate=7+%E6%9C%88+28%E6%97%A5%2C+%E5%91%A8%E5%9B%9B&fromToDate_submit=2017-07-24&fromDate=2017-07-29
&toDate=2017-07-30&lengthOfStay=1&roomCountBox=1&roomCount=1&guestCountBox=1&guestCount=1&clusterCode=none&corporateCode="

#url = "http://www.marriott.com.cn/search/submitSearch.mi?destinationAddress.destination=%E5%8C%97%E4%BA%AC%2C+China
&fromDate=2017-07-29&toDate=2017-07-30&lengthOfStay=1&recordsPerPage=40"

#&singleSearch=true&singleSearchAutoSuggest=false&autoSuggestItemType=Unmatched&clickToSearch=false
&destinationAddress.latitude=39.906011&destinationAddress.longitude=116.387911
&destinationAddress.cityPopulation=0.0&destinationAddress.cityPopulationDensity=0.0&destinationAddress.city=北京
&destinationAddress.country=CN
'''

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