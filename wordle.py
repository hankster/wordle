#! /usr/bin/python3
"""
wordle.py -- A Python program to help you solve the wordle game

Sample usage:

 wordle.py -n audes -r ion --p1 o --p2 i --n1 n --n3 i --n4 o

Complete specification:

 wordle.py -d -h -v --debug  --help --version

 where

 -a, --all            All words
 -d, --debug          Turn debug statements on
 -f, --file           Input filename
 -h, --help           Help text
 -n, --not            Letters which will discard a word
 --n1, --n2 ...       Disallowed letters in position 1 (first letter)
 --p1, --p2 ...       Required in position 1 (first letter)
 -r, --required       Required letters in the word
 -v, --version        Report program version

The sample given above can be read as follows:

Select a word that does not have the letters "a", "u", "d", "e", "s"
and must require the letters "i", "o", "n"
and position 1 must have an "o" <--- columns or positions are numbered left to right starting at 1.
and position 2 must have an "i"
and position 1 must not have an "n"
and position 3 must not have an "i"
and position 4 must not have an "o"
and select only quality words <--- the word is found in three different dictionaries (default option -a, --all).

Strategy:
First guess: "audio" <--- Has four vowels and one popular consonant
Second guess: clerk spent, crest, sperm or terms <--- Has only one "e" and four popular consonants
Second guess: Look at the results of the first line and determine what might be more productive (one of the five words above or some other choice based on the first submission).

Letter frequency in English: e a r i o t n s l c u d p
Suggests that a good starting word might be "arise" or "raise"
For 5-letter words the frequency is a, e, s, o, r, i, l, t, n, u, d, c, y
Suggests that a good starting word might be "arose"

Not included here are the English dictionaries, found on GitHub. Three are used:

 english_words = load_words(words_alpha.txt)
 reference_words = load_words("wordlist-umich.txt")
 tenthousand_words = load_words("wordlist.10000.txt")


Copyright (2022) H. S. Magnuski
All rights reserved

"""

import sys
import os, os.path
import time
import getopt
import string
import math
import random

debug = False
discard = ""
required = ""
p1 = ""
p2 = ""
p3 = ""
p4 = ""
p5 = ""
n1 = ""
n2 = ""
n3 = ""
n4 = ""
n5 = ""
allwords = False

def Usage():
    print("Usage: wordle.py -d -h -n -r -v --debug --help --not abc... --n1 abc... --n2 abc...  ... --p1 x --p2 x ... --version")

def load_words(w):
    with open(w) as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

# Find good choices for a second guess
# First guess is "audio"
# Discard words with h, w, y
# wordle.py -n audiohwy -r e

def second(w):
    for l in "abcdefghijklmnopqrstuvwxyz":
        count = 0
        for d in w:
            if d == l:
                count = count + 1
        if count > 1:
                break
    if count > 1:
        return True
    return False

def main(words, ref, ten, cnt):

    awords = []
    qwords = []
    
    for w in words:

        # Words not 5 letters can't be used
        if len(w) != 5 :
            continue

        # Check for required letters
        if len(required) > 0:
            found = True
            for r in required:
                if not r in w:
                    found = False
            if not found:
                continue

        # Check for discards
        throw_away = False
        for d in discard:
            if d in w:
                throw_away = True
        if throw_away:
            continue
        
        if p1 != "":
            if w[0] != p1:
                continue
            
        if p2 != "":
            if w[1] != p2:
                continue
            
        if p3 != "":
            if w[2] != p3:
                continue
            
        if p4 != "":
            if w[3] != p4:
                continue
        
        if p5 != "":
            if w[4] != p5:
                continue
            
        throw_away = False

        if n1 != "":
            for d in n1:
                if w[0] == d:
                    throw_away = True
        if n2 != "":
            for d in n2:
                if w[1] == d:
                    throw_away = True
        if n3 != "":
            for d in n3:
                if w[2] == d:
                    throw_away = True
        if n4 != "":
            for d in n4:
                if w[3] == d:
                    throw_away = True

        if n5 != "":
            for d in n5:
                if w[4] == d:
                    throw_away = True

        if throw_away:
            continue

        # Discard words that aren't in other dictionaries

        if w in ten:
            qwords.append(w)
        elif allwords:
            awords.append(w)
            
    qwords.sort()
    for w in qwords:
        print("Quality word --> ", w)

    awords.sort()
    if allwords:
        print("---")
        for w in awords:
            print("Quality less --> ", w)

def sorting(words): 
    wordsorted = sorted(words, key=len) 
    return wordsorted

    
if __name__ == '__main__':

    #
    # Get options and call the main program
    #                                                                                            

    print("wordle.py -- For 5-letter words the frequency is a, e, s, o, r, i, l, t, n, u, d, c, y")

    filename = 'words_alpha.txt'
    count = 0

    try:
        options, args = getopt.getopt(sys.argv[1:], 'ac:df:g:hn:r:v', ['all', 'count=', 'debug', 'file=', 'game=', 'help', 'not=', 'n1=', 'n2=', 'n3=', 'n4=', 'n5=', 'p1=', 'p2=', 'p3=', 'p4=', 'p5=', 'required=', 'version'])
    except getopt.GetoptError:
        Usage()
        sys.exit(2)

    for o, a in options:
        if o in ("-a", "--all"):
            allwords = True
        if o in ("-c", "--count"):
            count = int(a)
        if o in ("-d", "--debug"):
            debug = True
        if o in ("-f", "--file"):
            filename = a
        if o in ("-h", "--help"):
            Usage()
            sys.exit()
        if o in ("-n", "--not"):
            discard = a
        if o in ("--n1"):
            n1 = a
        if o in ("--n2"):
            n2 = a
        if o in ("--n3"):
            n3 = a
        if o in ("--n4"):
            n4 = a
        if o in ("--n5"):
            n5 = a
        if o in ("--p1"):
            p1 = a
        if o in ("--p2"):
            p2 = a
        if o in ("--p3"):
            p3 = a
        if o in ("--p4"):
            p4 = a
        if o in ("--p5"):
            p5 = a
        if o in ("-r", "--required"):
            required = a
        if o in ("-v", "--version"):
            print("wordle.py Version 1.1")
            sys.exit()
        
    english_words = load_words(filename)
    reference_words = load_words("wordlist-umich.txt")
    tenthousand_words = load_words("wordlist.10000.txt")


    main(english_words, reference_words, tenthousand_words, count)

    sys.exit()
    
