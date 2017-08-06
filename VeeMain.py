import requests
import urllib
from urllib import parse as urlparse
from lxml import html
from bs4 import BeautifulSoup

class Main_Query():
	def __init__(self,place,day_cin,day_num):
		self._place = place
		self._day_cin = day_cin
		self._day_num = day_num
		self.starwood = Starwood()
		self.marriott = Marriott()
		self.hotels = []

	def showResult(self):
		for i in self.hotels:
		    for k,v in i.items():
		        print('{k}:{v}'.format(k=k,v=v))
		    print()

	def getResult(self):
		self.hotels = self.starwood.getHotels()
		self.hotels = self.hotels.append(self.marriott.getHotels())

	



