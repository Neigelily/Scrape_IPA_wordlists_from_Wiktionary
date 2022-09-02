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
	currentLink = baseLink+"/wiki/Category:"+language+"_terms_with_IPA_pronunciation"
	driver = webdriver.Chrome(<path of the file "chromedriver" on your computer>, options = options)
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
			for h2 in h2liste:
				if h2.find_all("span", id=language) != []:
					for par in h2.find_next_siblings():
						listOfSpansIPA = par.find_all("span", class_="IPA")
						if listOfSpansIPA != []:
							for spanIPA in listOfSpansIPA:
								parent = spanIPA.parent
								iSpanDialect = spanIPA.find_previous_sibling("i")
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
							break
								 #("span", class_="IPA").text)
			print("Page "+str(counterPage)+" : "+str(counter+1)+"/"+str(len(listOfLinksCurrentPage)))
		nextPageLinks = soup.find_all(lambda tag: tag.name == "a" and "next page" in tag.text)
		if nextPageLinks != []:
			currentLink = baseLink+nextPageLinks[0]["href"]
			driver.get(currentLink)
			html_source = driver.page_source
		else:	
			html_source = ""
	
	
	fields=['Word', 'Dialect']
	with open(language+'.csv', 'w', encoding='utf-8') as f:
	      
	    # using csv.writer method from CSV package
	    write = csv.writer(f)
	      
	    write.writerow(fields)
	    write.writerows(listOfIPAWords)
	
	#<span class="IPA">/attiβiˈtat/</span>
	
	#<h2><span class="mw-headline" id="Occitan">Occitan</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=a&amp;action=edit&amp;section=683" title="Edit section: Occitan">edit</a><span class="mw-editsection-bracket">]</span></span></h2>
	
	#<span class="IPA" lang="">/a/</span>
		#find_next_sibling()

