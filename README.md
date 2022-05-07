# wordle
A Python program to help with hints in solving the Wordle game.

https://powerlanguage.co.uk/wordle/

https://www.nytimes.com/games/wordle/index.html

Requires downloading of English dictionaries.

Sample usage:

 wordle.py -n audes -r ion --p1 o --p2 i --n1 n --n3 i --n4 o

Complete specification:

 wordle.py -d -h -v --debug  --help --version

 where

 * -a, --all            All words
 * -d, --debug          Turn debug statements on
 * -f, --file           Input filename
 * -h, --help           Help text
 * -n, --not            Letters which will discard a word
 * --n1, --n2 ...       Disallowed letters in position 1 (first letter)
 * --p1, --p2 ...       Required in position 1 (first letter)
 * -r, --required       Required letters in the word
 * -v, --version        Report program version

The sample given above can be read as follows:

* Select a word that does not have the letters "a", "u", "d", "e", "s"
* and must require the letters "i", "o", "n"
* and position 1 must have an "o" <--- columns or positions are numbered left to right starting at 0.
* and position 2 must have an "i"
* and position 1 must not have an "n"
* and position 3 must not have an "i"
* and position 4 must not have an "o"
* and select only quality words <--- the word is found in three different dictionaries (default option -a, --all).

Strategy:

* First guess: "audio" <--- Has four vowels and one popular consonant
* First guess: "arose" <--- Has highest frequency letters for 5-letter words
* Second guess: clerk spent, crest, sperm or terms <--- Has only one "e" and four popular consonants
* Second guess: Look at the results of the first line and determine what might be more productive (one of the five words above or some other choice based on the first submission).

Not included here are the English dictionaries, found on GitHub. Three are used:

* english_words = load_words(words_alpha.txt)
* reference_words = load_words("wordlist-umich.txt")
* tenthousand_words = load_words("wordlist.10000.txt")
