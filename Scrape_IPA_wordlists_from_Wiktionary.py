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

def isComplexWord(word):
	return " " in word.strip()
		 

def whichPartOfSpeechInText(text):
	WikiListOfPartsOfSpeech = ["adfix","adjective","adnoun", "adverb", "affix", "article", "auxiliary verb",
							"cardinal number", "circumfix", "collective numeral","conjunction","conjunctional phrase",
							"coverb","demonstrative determiner","demonstrative pronoun","determinative",
							"determiner","fractional number","gerund","indefinite pronoun","infinitive", "infix",
							"interjection","interjectional phrase","interrogative pronoun","intransitive verb",
							"multiplicative number","multiplicative numeral","noun","number","numeral","ordinal",
							"ordinal number","part of speech","participle","particle","personal pronoun",
							"phrasal preposition","possessional adjective","possessive adjective","possessive determiner",
							"possessive pronoun", "postfix", "postposition","predicative", "prefix", "preposition","preverb","privative adjective",
							"pronominal phrase","pronoun","quasi-adjective","reciprocal pronoun","reflexive pronoun",
							"relative adjective","relative pronoun","speech disfluency","substantive", "suffix", "transfix", "transitive",
							"transitive verb", "verb", "verbal noun"]
	for partOfSpeech in WikiListOfPartsOfSpeech:
		if partOfSpeech in text.lower():
			return partOfSpeech
	return None		

def scrapeFromWiktionaryIPAwords(language, removeComplexWords = False):
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
		
		myDiv = soup.find_all("div", class_="mw-category")
		
		if myDiv != []:	
			WordsCurrentPage = myDiv[0].find_all("a")
		else:
			print(currentLink)
			break
		listOfLinksCurrentPage = []
		for i in WordsCurrentPage:
			if not (removeComplexWords == True and isComplexWord(i.text) == True):	
				if baseLink in i["href"]:
					listOfLinksCurrentPage.append(i["href"])
				else:
					listOfLinksCurrentPage.append(baseLink+i["href"])		
		for counter in range(0, len(listOfLinksCurrentPage)):
			driver.get(listOfLinksCurrentPage[counter])
			html_source_word = driver.page_source
			soupWord = BeautifulSoup(html_source_word, 'html.parser')
			h2liste = soupWord.find_all("h2")
			isFound = False
			translationIsFound = False
			for h2 in h2liste:
				if h2.find_all("span", id=language) != []:
					isAfterPronunciation = False
					isAfterPartOfSpeech = False
					listOfTranslations = []
					listOfPartsOfSpeech = []
					temporaryIPAlist = []
					for siblingH2 in h2.find_next_siblings():
						if isAfterPartOfSpeech == True:
							#print("hello")
							if siblingH2.name == "ol" :
								listOfTranslationLi = siblingH2.find_all("li")
								translation = ""
								for transaltionLi in listOfTranslationLi:
									if translation != "":
										translation += "; "
									translation += transaltionLi.text
								listOfTranslations.append(translation)
								isAfterPartOfSpeech = False
								translationIsFound = True
						if siblingH2.name in ["h3", "h4"] and bool(whichPartOfSpeechInText(siblingH2.text)):
							partOfSpeech = whichPartOfSpeechInText(siblingH2.text)	
							isAfterPartOfSpeech = True
							listOfPartsOfSpeech.append(partOfSpeech)
						elif siblingH2.name == "h2":	
							break
						if isAfterPronunciation == True:
							listOfSpansIPA = siblingH2.find_all("span", class_="IPA") # inside siblings, select <span class = "IPA">, because that's where the IPA transcription is
							if listOfSpansIPA != []:
								for spanIPA in listOfSpansIPA:
									parent = spanIPA.parent # select closest parent of <span class = "IPA"> to see if there is a dialect specified
									if parent != None:
										text = parent.text.split(spanIPA.text) # look at what's BEFORE the spanIPA in its parent, because that's where the dialect is specified
										potentialDialects = re.findall('\(([^)]+)\)', text[0]) # The dialect is always between round brackets
										dialectLabel = "unspecified"
										for potentialDialect in potentialDialects:
											if potentialDialect != "key": # there are also bracketed instances of text "key", which we must rule out
												dialectLabel = potentialDialect
									else:
										dialectLabel = "unspecified"
	
									temporaryIPAlist.append([spanIPA.text, dialectLabel])
								isFound = True
						else:
							PronunciationTags = siblingH2.find_all(lambda tag: "Pronunciation" in tag.text)
							if PronunciationTags != []:
								isAfterPronunciation = True
					if listOfTranslations == []:
						listOfTranslations.append("unspecified")
					if listOfPartsOfSpeech == []:
						listOfPartsOfSpeech.append("unspecified")
					if len(listOfPartsOfSpeech) != len(listOfTranslations):
						print("Error: the number of parts of speech is not equal to the number of translations. Solved by setting to 'unspecified'")
						listOfPartsOfSpeech = ["unspecified"]
						listOfTranslations = ["unspecified"]
					for IPA in temporaryIPAlist:
						for i in range(len(listOfPartsOfSpeech)):
							listOfIPAWords.append(IPA+[listOfPartsOfSpeech[i],listOfTranslations[i]])
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
	
	
	fields=['Entry', 'Dialect', 'Part of speech', 'Translation']
	with open(language+'.csv', 'w', encoding='utf-8') as f:
	      
	    write = csv.writer(f)
	      
	    write.writerow(fields)
	    write.writerows(listOfIPAWords)
	




