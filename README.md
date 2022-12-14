# Description

This script scrapes Wiktionary (https://en.wiktionary.org/w/index.php?title=Category:Terms_with_IPA_pronunciation_by_language&from=F) to produce IPA wordlists composed of all the words of a given language for which an IPA transcription is provided in Wiktionary. The output is a csv file containing the IPA transcription, dialect tag (if specified by Wiktionary), part of speech tag and translation of each word. Square brackets or slashes delimiting IPA transcriptions are preserved from the Wiktionary data. An example of output file is provided in this repository.

The output is produced by executing one function: scrapeFromWiktionaryIPAwords(language, removeComplexWords = False), which takes the language of interest as its first argument, and an optional second argument "removeComplexWords". If the latter is set to True, the program ignores the entries of Wiktionary that contain one or more spaces.

# Requirements

- Install Selenium and a driver to interface with the chosen browser (instructions here: https://selenium-python.readthedocs.io/installation.html)
- Replace \<Path to driver\> in the code by the path to the place you chose for the driver on your computer
- An Internet connection
- Use the same language name as Wiktionary (e.g. "Occitan", "Haitian Creole")
- If you don't use Chrome, adapt the code to the browser you use (it should be easy)
  

# Other info
The execution of the script takes approximately 01:05 minute per 200 entries (=1 Wiktionary page) on my laptop. For scraping the French IPA wiktionary (79,825 entries), it would hence take approximately 07:15 hours to run.

## Disclaimer:

The HTML structure of Wiktionary varies slitghtly from language to language. This script is intended to be quite robust, but I cannot guarantee that it works perfectly for all languages of Wiktionary.


