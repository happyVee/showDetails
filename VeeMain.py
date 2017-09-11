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
from pylab import *

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
		json.dump(self.hotels,open('hotels.json','w'))
		self.details = dict(vee.marriott.hotelRateDetial, **vee.starwood.hotelRateDetial)
		json.dump(self.details,open('details.json','w'))

	def showByImage(self,key,num,num_all):
		#figure = plt.figure()
		plt.subplot(num_all,1,num)
		ih = self.details[key]
		#plt.subplot(1,1,1)
		price = ih['price']
		xda = list(price.keys())
		yda = list(price.values())
		x = range(0,len(xda))
		#plt.xlabel('day')
		plt.ylabel('price')
		plt.title(ih['name_en'])
		plt.plot(x,yda,'y')
		plt.xticks(x,xda,rotation=30)
		for a,b in zip(x,yda):
			plt.text(a, b+1, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)
		plt.ylim(0, (int(max(yda)/100)+1)*100)
		#plt.grid()
		#plot.show()

	def showAllImage(self):
		num_all = len(self.details)
		num = 1
		for key in vee.details:
			if num < 3:
				self.showByImage(key,num,num_all)
				num = num+1
		plt.grid()
		plot.show()
'''
	def showLowestPrice(self):
		self.lowest = {}
		for key in self.details:
			item = self.details[key]
			price = item['price']
			self.lowest[key] = {'price':min(zip(price.values(),price.keys()),'name' = item['name_cn'])}

	def getDetails():
		with open('details.txt','r') as f:
			details = json.load(f)
			return details
'''
if __name__ == '__main__':
	#mpl.rcParams['font.san-serif'] = ['SimHei']
	place = 'Shanghai'
	day_in = '20170913'
	print("正在查询  "+place + "  "+day_in[0:4]+"年"+day_in[4:6]+"月"+day_in[6:8]+"日的酒店")
	#day_out = '20170827'
	day_num = 30
	vee = MainQuery(place,day_in,day_num)
	vee.getResult()
	vee.showResult()
	vee.getMonth()
	vee.saveToTxt()



