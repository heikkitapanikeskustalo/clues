##############################################################################

# This file: local.py

# Date: 6 Jun 2020, 15 May 2020 - 4 May 2020

# Author: Heikki Keskustalo

# Purpose: Define resources to use during analysis of Finnish word-clues.

##############################################################################

# The Python functions of "clues" were utilized to retrieve documents (letters)
# based on gender metadata (Male or Female) observed regarding the words in two
# specified XML fields of letters (= beginning and ending salutations). 
# Gender was observed based on the first persons names via calling the
# external application Omorfi (using its gender metadata about first names), please
# see Omorfi's GitHub site and Pirinen, T.A. (2015) "Development and use of 
# computational morphology of Finnish in the open source and open science era: 
# notes on experiences with Omorfi Development. SKY Journal of Linguistics
# 2015, 28, 381-393.  Functions of "clues" help reading input files (one document
# per file) and reporting detailed information regarding the character sets and 
# other details about the input files.

# The functions of "clues" need to be modified before use to perform the
# desired retrieval - based on the words strings or possibly utilizing
# an external resource producing word-level metadata, if metadata is needed
# in retrieval.

O_in =  "tmp_in_"  # filename start for analyzer input (= word "ladder")

O_out = "tmp_out_" # filename start for analyzer output (= morph analysis)

null_code_list = ['NULL'] # missing value indicator; not reported as words

# 1. General resources:

import sys # sys.exit()

import os # os.system() for command lines

import os.path

import chardet # char set detection

import re  # regular expressions

# 2. NLP (natural language processing) resources

from bs4 import BeautifulSoup # to select fields from document

import nltk # to utilize Natural Language Toolkit

from nltk.tokenize import RegexpTokenizer # tokenize string into words

evoluztokenizer = RegexpTokenizer('[\w][\w\-]*') # See documentation of RegexpTokenizer



# end of file.



