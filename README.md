# Scrape-IPA-wordlists-from-Wiktionary

This code scrapes Wiktionary (https://en.wiktionary.org/w/index.php?title=Category:Terms_with_IPA_pronunciation_by_language&from=F) to produce IPA wordlists composed all the words of a given language for which an IPA transcription is provided in Wiktionary.

This is done by executing one function: scrapeFromWiktionaryIPAwords(language), which takes the language of interest as its unique argument.

Executing this function requires:
- to install Selenium and a driver to interface with the chosen browser (instructions here: https://selenium-python.readthedocs.io/installation.html)
- To replace "" in the code by the path to the place you chose for the driver on your computer
- an Internet connection
- To use the same language name as Wiktionary (e.g. "Occitan", "Haitian Creole")
