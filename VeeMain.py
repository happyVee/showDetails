#Coding = 'utf-8'

import requests
import urllib
from urllib import parse as urlparse
from lxml import html
from bs4 import BeautifulSoup
from marriott import Marriott
from starwood import Starwood
import json
import matplotlib.pyplot as plt  

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
		self.hotels = sorted(self.hotels,key = lambda hotel:hotel['price'])

	def showResult(self):
		print("")
		print("Sum of Hotel:" + str(len(self.hotels)))
		for i in self.hotels:
		    for k,v in i.items():
		        print('{k}:{v}'.format(k=k,v=v))
		    print()#

	def getMonth(self):
		vee.starwood.getMonth()
		vee.marriott.getMonth()

	def saveToTxt(self):
		json.dump(self.hotels,open('hotels.txt','w'))
		self.details = dict(vee.marriott.hotelRateDetial, **vee.starwood.hotelRateDetial)
		json.dump(self.details,open('details.txt','w'))

	def showByImage(self):
		ih = self.details['SHARN']
		price = ih['price']
		xda = list(price.keys())
		yda = list(price.values())
		x = range(0,len(xda))
		plt.xlabel('day')
		plt.ylabel('price')
		plt.title(ih['name_en'])
		plt.plot(x,yda,'y')
		plt.xticks(x,xda,rotation=90)
		plt.grid() 
		plt.show()

if __name__ == '__main__':
	place = 'Shanghai'
	day_in = '20170905'
	print("正在查询  "+place + "  "+day_in[0:4]+"年"+day_in[4:6]+"月"+day_in[6:8]+"日的酒店")
	#day_out = '20170827'
	day_num = 35 
	vee = MainQuery(place,day_in,day_num)
	vee.getResult()
	vee.showResult()
	vee.getMonth()
	vee.saveToTxt()



