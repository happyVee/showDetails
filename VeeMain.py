import requests
import urllib
from urllib import parse as urlparse
from lxml import html
from bs4 import BeautifulSoup

class Main_Query():
	def __init__(self,place,day_cin,day_num):
		self._params['place'] = place
		self._params['day_cin'] = day_cin
		self._params['day_num'] = day_num
		self.starwood = Starwood(self._params)
		self.marriott = Marriott(self._params)
		self.hotels = []

	def showResult(self):
		for i in self.hotels:
		    for k,v in i.items():
		        print('{k}:{v}'.format(k=k,v=v))
		    print()

	def getResult(self):
		self.hotels = self.starwood.getHotels()
		self.hotels = self.hotels.append(self.marriott.getHotels())

if __name__ == '__main__':
	place = 'shanghai'
	day_in = '2017-08-29'
	day_num = 2 
	vee = Main_Query(place,day_in,day_num)
	vee.getResult()
	vee.showResult()
	



