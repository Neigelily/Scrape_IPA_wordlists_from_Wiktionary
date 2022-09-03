#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 16:44:57 2022

@author: neigerochant
"""
import csv
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")


def scrapeFromWiktionaryIPAwords(language):
	baseLink = "https://en.wiktionary.org"
	language = language.replace(" ", "_")
	currentLink = baseLink+"/wiki/Category:"+language+"_terms_with_IPA_pronunciation"
	driver = webdriver.Chrome(<Path to driver>, options = options)
	driver.get(currentLink)
	
	html_source = driver.page_source
	listOfIPAWords = []
	counterPage = 0
	
	
	while html_source != "":
		counterPage += 1
		soup = BeautifulSoup(html_source, 'html.parser')
		
		myDiv = soup.find_all("div", class_="mw-category mw-category-columns")
		
		
		WordsCurrentPage = myDiv[0].find_all("a")
		
		listOfLinksCurrentPage = []
		for i in WordsCurrentPage:
			if baseLink in i["href"]:
				listOfLinksCurrentPage.append(i["href"])
			else:
				listOfLinksCurrentPage.append(baseLink+i["href"])
	
		for counter in range(0,len(listOfLinksCurrentPage)):
			driver.get(listOfLinksCurrentPage[counter])
			html_source_word = driver.page_source
			soupWord = BeautifulSoup(html_source_word, 'html.parser')
			h2liste = soupWord.find_all("h2")
			isFound = False
			for h2 in h2liste:
				if h2.find_all("span", id=language) != []:
					isAfterPronunciation = False
					for siblingH2 in h2.find_next_siblings():
						if isAfterPronunciation == True:
							listOfSpansIPA = siblingH2.find_all("span", class_="IPA")
							if listOfSpansIPA != []:
								for spanIPA in listOfSpansIPA:
									parent = spanIPA.parent
									if parent != None:
										text = parent.text.split(spanIPA.text)
										potentialDialects = re.findall('\(([^)]+)\)', text[0])
										dialectLabel = "unspecified"
										for potentialDialect in potentialDialects:
											if potentialDialect != "key":
												dialectLabel = potentialDialect
									else:
										dialectLabel = "unspecified"
									listOfIPAWords.append([spanIPA.text, dialectLabel])
								isFound = True
								break
						else:
							PronunciationTags = siblingH2.find_all(lambda tag: "Pronunciation" in tag.text)
							if PronunciationTags != []:
								isAfterPronunciation = True
			if isFound == True:		
				print("Page "+str(counterPage)+" : "+str(counter+1)+"/"+str(len(listOfLinksCurrentPage)))
			else: print("No IPA found at link n°"+str(counter+1)+" on page "+str(counterPage)+" ("+currentLink+")")
		nextPageLinks = soup.find_all(lambda tag: tag.name == "a" and "next page" in tag.text)
		if nextPageLinks != []:
			currentLink = baseLink+nextPageLinks[0]["href"]
			driver.get(currentLink)
			html_source = driver.page_source
		else:	
			html_source = ""
	
	
	fields=['Word', 'Dialect']
	with open(language+'.csv', 'w', encoding='utf-8') as f:
	      
	    write = csv.writer(f)
	      
	    write.writerow(fields)
	    write.writerows(listOfIPAWords)
	


