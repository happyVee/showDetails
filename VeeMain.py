#Coding = 'utf-8'

import requests
import urllib
from urllib import parse as urlparse
from lxml import html
from bs4 import BeautifulSoup
from Marriott import Marriott
from Starwood import Starwood

class MainQuery():
	def __init__(self,place,day_cin,day_num):
		self._params = {}
		self._params['place'] = place
		self._params['day_cin'] = day_cin
		#self._params['day_out'] = day_out
		self._params['day_num'] = day_num
		self.starwood = Starwood(self._params)
		self.marriott = Marriott(self._params)
		self.hotels = []

	def getResult(self):
		self.hotels = self.starwood.getHotels()
		self.hotels = self.hotels + self.marriott.getHotels()

	def showResult(self):
		print("")
		print("Sum of Hotel:" + str(len(self.hotels)))
		for i in self.hotels:
		    for k,v in i.items():
		        print('{k}:{v}'.format(k=k,v=v))
		    print()


if __name__ == '__main__':
	place = 'Shanghai'
	day_in = '20170901'
	print("正在查询  "+place + "  "+day_in[0:4]+"年"+day_in[4:6]+"月"+day_in[7:8]+"日的酒店")
	#day_out = '20170827'
	day_num = 1 
	vee = MainQuery(place,day_in,day_num)
	vee.getResult()
	vee.showResult()
	



