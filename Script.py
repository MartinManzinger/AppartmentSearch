"""This is a data scraper for the crawling and searching of child care facilities in the canton of Zürich, Switzerland, from the website http://www.lotse.zh.ch. Code: Jan Rothenberger, CC 2.0 BY NC"""

import os
import sys
import urllib.request
from bs4 import BeautifulSoup


clear = lambda: os.system('cls')
wait  = lambda: input('press enter to proceed')


class AppartmentSearch:
	if True: # Webaddresses
		WebSite_SavedSearch = 'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Polygonsuche/mbidHgoydAgfB%7Bi@mmEgsDszAknXkdKihNo%60Gije@%60cMaiGvwGp_Nz%7BKdwBdyLfoQtwBlgUuDtpY%7B%7BFv_CwvDzi@acCpr@/2,00-/-/EURO--810,00?enteredFrom=saved_search'

	def __init__(self):
		clear()
		print('Appartment Search - Immobilienscout24')
		Choice = input('expose id or just enter\n')
		if len(Choice)<3:
			print('apply stored search...')
			ExposeIds = self.extract_search_results()
			print('extract appartment datas...')
			AppartmentDatas = []
			for ExposeId in ExposeIds:
				AppartmentDatas.append(self.extract_appartment_data(ExposeId))
			print('save in csv...')
			self.write_csv(AppartmentDatas)
		else:
			AppartmentData = self.extract_appartment_data(Choice)
			for key in AppartmentData:
				tab = '                                  '
				tab = tab[:(20-len(key))]
				print(key + tab + str(AppartmentData[key]))
			
	def extract_search_results(self):
		response = urllib.request.urlopen(self.WebSite_SavedSearch)
		HtmlString = BeautifulSoup(response, features="html.parser")
		results = HtmlString.find_all("a", class_="result-list-entry__brand-title-container")
		ExposeIds = []
		for result in results:
			ExposeIds.append(self.get_string_attribute(result, "data-go-to-expose-id"))
		return ExposeIds
	def extract_appartment_data(self, ExposeId):
		# attributes
		Kaltmiete = None
		Warmmiete = None
		Addresse = None
		MapsUrl = None
		Url = None
		Zimmer = None
		Fläche = None
		Etage = None
		BezugsFrei = None
		Grundriss = None
		Beschreibung = None
		Bilder = None
		Vermieter = None
		# calculate url
		Url = 'https://www.immobilienscout24.de/expose/' + str(ExposeId)
		# open site with beautifulsoup
		response = urllib.request.urlopen(Url)
		HtmlString = BeautifulSoup(response, features="html.parser")
		# dd container
		if True:
			containers = HtmlString.find_all("dd")
			# search attributes in containers
			temp = self.get_class_content(containers, 'addresse')
			if temp!=-1:
				Addresse = temp
			temp = self.get_class_content(containers, 'kaltmiete')
			if temp!=-1:
				Kaltmiete = temp
			temp = self.get_class_content(containers, 'gesamtmiete')
			if temp!=-1:
				Warmmiete = temp
			temp = self.get_class_content(containers, 'zimmer')
			if temp!=-1:
				Zimmer = temp
			temp = self.get_class_content(containers, 'wohnflaeche')
			if temp!=-1:
				Fläche = temp
			temp = self.get_class_content(containers, 'etage')
			if temp!=-1:
				Etage = temp
			temp = self.get_class_content(containers, 'bezugsfrei')
			if temp!=-1:
				BezugsFrei = temp
				{"house" : "Haus", "cat":"Katze", "black":"schwarz"}
		# pre container
		if True:
			containers = HtmlString.find_all("pre")
			# search attributes in containers
			Beschreibung = ''
			temp = self.get_class_content(containers, 'objektbeschreibung')
			if temp!=-1:
				Beschreibung += 'Objektbeschreibung\n' + temp + '\n'
			temp = self.get_class_content(containers, 'ausstattung')
			if temp!=-1:
				Beschreibung += 'Ausstattung\n' + temp + '\n'
			temp = self.get_class_content(containers, 'lage')
			if temp!=-1:
				Beschreibung += 'Lage\n' + temp + '\n'
			temp = self.get_class_content(containers, 'sonstiges')
			if temp!=-1:
				Beschreibung += 'Sonstiges\n' + temp + '\n'
		# search attributes in containers
		# search Addresse and MapsUrl
		# search Grundriss
		# search Beschreibung
		# search Bilder
		# search Vermieter
		return {'ExposeId' : ExposeId,
				'Url' : Url,
				'Addresse' : Addresse,
				'MapsUrl' : MapsUrl,
				'Kaltmiete' : Kaltmiete,
				'Warmmiete' : Warmmiete,
				'Zimmer' : Zimmer,
				'Fläche' : Fläche,
				'Etage' : Etage,
				'Grundriss' : Grundriss,
				'BezugsFrei' : BezugsFrei,
				'Beschreibung' : Beschreibung,
				'Bilder' : Bilder,
				'Vermieter' : Vermieter}
	# helper functions
	def get_string_attribute(self, InputString, AttributeName):
		InputString = str(InputString)
		CharStart = InputString.find(AttributeName)
		while True:
			CharStart += 1
			if InputString[CharStart]=='"':
				CharStart += 1
				break
		CharEnd = CharStart
		while True:
			CharEnd += 1
			if InputString[CharEnd]=='"':
				break
		return InputString[CharStart:CharEnd]
	def get_class_content(self, InputStrings, AttributePart):
		FoundItem = False
		for InputString in InputStrings:
			InputString = str(InputString)
			# extract class tag
			temp = InputString.split('>')[0]
			# find attribute
			CharStart = temp.find(AttributePart)
			if CharStart != -1:
				FoundItem = True
				break
		if FoundItem==False:
			return -1
		while True:
			CharStart += 1
			if InputString[CharStart]=='>':
				CharStart += 1
				break
		CharEnd = CharStart
		while True:
			CharEnd += 1
			if InputString[CharEnd]=='<':
				break
		return InputString[CharStart:CharEnd]
	def write_csv(self, AppartmentDatas):
		with open('AppartmentData.csv', mode='w') as file:
			SplitChar = ';'
			for key in AppartmentDatas[0]:
				Str = key + SplitChar
				for i in range(len(AppartmentDatas)):
					Data = str(AppartmentDatas[i][key])
					Data = Data.replace(';', ',')
					if '\n' in Data:
						Data = '"' + Data + '"'
					Str += Data + SplitChar
				Str = Str[:-1] + '\n'
				file.write(Str)
	
		
Instance = AppartmentSearch()
		
		

		
		
		
		
		
		
		
		
		
		
		
		