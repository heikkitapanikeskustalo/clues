##############################################################################
# This file: clues.py
# Date: 1-11 Jun 2020, 3-29 May 2020, 22-30 Apr 2020; additional comments:
#       1-28 Jun 2021 by Jaana Kalliala and Heikki Keskustalo 
# Author: Heikki Keskustalo
# Purpose: Interactively read text files (Finnish) from given directory; report
#          information regarding words in user-given field.
# For more details see: DESCRIPTION at the end of this file.
##############################################################################

from clues_resources_with_comments import *

# Begin main

accept = "" # RETURN as user reply: continue printing
skip = "q"  # q as user reply: skip printing for present question

# Finnish historian is assumed to be interacting with interface

print("  Clues/EVOLUZ v 1.0 June 2020")
print("* Vuorovaikutteinen johtolankojen etsinta tekstista") 
print("  Tutkijan versio - very verbose mode.") 

opening_message = "\nKirjoita syotetietojen hakemisto" + \
            "\n(yksi dokumentti per tiedosto, ei muita tietoja)" + \
            "\n esim. /home/ccheke/evoluz-2020/letterdata/input/" + \
            "\nHyvaksy oletushakemisto painamalla RETURN]"

        # Note: input directory must contain ONLY input files

        # 14 Jun 2021 Jaana Kalliala (JK)

basic_msg = " paina RETURN [%s = skip]"

# User is asked to give dir-path of input files 14 Jun 2021 (JK)

input_directory = prompt(opening_message)

# Please edit input data path:

if len(input_directory)==0: # RETURN was pressed: accept the following dir
    input_directory = "LOCAL_DIR_PATH/letterdata/input/" 
    

print("* Kaytetaan hakemistoa %s" % (input_directory)) # Using directory ...

# Press RETURN if you want to read the texts or s to stop:

response = prompt("Paina RETURN jos haluat lukea tekstit" + \
                   "\n[tai s=stop program]") 

if "s" in response or "S" in response:
    print("* Ok. Keskeytetaan ohjelman suoritus.") # Exiting ...
    sys.exit() 

print("Luetaan tiedostot.") # Reading files ...

filenames = read_all_filenames(input_directory) # filenames list (without path)

# Reads ALL files from given input directory (no extra files are allowed);
# detects the original character encoding (e.g., UTF-8 or ISO-8859-1);
# decodes texts into Unicode; reports information about the input
# files in chunks of 100 files; returns a list of 4-tuples regarding
# information about the files. 14 Jun 2021 JK

# BIG TABLE: of tuples (0:filename; 1:charset; 2:raw data; 3:Unicode data)

BIG_TABLE = return_big_table(input_directory, filenames)

print("* %d tiedostoa luettu." % (len(BIG_TABLE))) # files read

# Constructs a frequency distribution of the character encodings detected
# and prints it in form of: 
# Char distribution: x files having char encoding y. 14 Jun 2021 JK

# Historical input files may have varying and even mixed character sets
# within one file; therefore we print detailed information.

# report overall about char encodings found in files (e.g., UTF-8 or Latin-1)

print_charset_info(BIG_TABLE)

col_2 = 2 # BIG_TABLE column [2]: raw contents of file (original encoding)
col_3 = 3 # BIG_TABLE column [3]: Unicode contents (raw decoded)

# Counts the file lengths in characters (including tags and NULL values) for
# both the input data and the decoded Unicode data. Prints the longest,
# shortest and the mean average values to give an understanding what kinds
# of input files were observed. 14 Jun 2021 JK

print_overall_report(BIG_TABLE, col_2, col_3) 

print("Listataanko tiedot tiedostoittain?", end='') # Print file-wise info?

vastaus = prompt(basic_msg % (skip)) # user's answer

if vastaus == accept:
    print_file_details_report(BIG_TABLE)
    # Above: print file-specific information in chunks of 20 files:
    # running ordinal, filename, original encoding, file length (both
    # original and Unicode) 14 Jun 2021 JK

print("Tiedostot luettu (koko sisalto).") # All input files read

##############################################################################
print("Poimitaan kentat: niiden johtolankoja tutkitaan. Esim.") # Collect tags
print("alkutervehdykset  (kentta: bsal)") # e.g., "beginning salutation" bsal
print("lopputervehdykset (kentta: esal):") # e.g., "ending salutation"

tag = "-" # this tag value allows entering the main loop

freqwordlists = [] # will become [bsal_freqlist, esal_freqlist]
dictionaries =  [] # will become [d1, d2] where d1 for bsal and d2 for esal
focustables =   [] # will become [f1, f2] where f1 for bsal and f2 for esal
fieldcount = 0     # at least one search field must be defined 
fields_triplets = [] # will become [(tag1, d1, f1), (tag2, d2, f2)] (11.6.2021 Jaana Kalliala)

while tag != "":
    fieldcount += 1
    (FOCUS_TABLE, tag) = GET_FIELD_INFORMATION(BIG_TABLE, fieldcount)
    # Prompt user for "target field" tag, e.g., "bsal"; or RETURN to start searching
    # Returns tuple (FOCUS_TABLE, tag) where FOCUS_TABLE is a list of tuples
    # (filename, ["field contents", "field contents",...]), usually 1 contents
    # string per file. 14 Jun 2021 JK 
    if tag != "": 
        print_fieldam_info(FOCUS_TABLE, tag)
#       Count and print frequency distribution: how many this type of fields per file
#       Next we will call for 4 functions, and, depending on user's choises:
#         1. Print field length distribution of the field searched for
#            found in each document in the form of "fields length" (all documents)
#         2. Print character-level frequency distibution regarding the field 
#            from highest to lowest in the form of "ch amount" (all documents)
#         3. Print char distributions of the field by file, in chunks of 20 files 
#         4. Print contents of the field (text), chunks of 20 files
#            in form of ordinal, file name, contents of the field/fields 15 Jun 2021 JK
        ask_BLOCK(tag, basic_msg, skip, accept, FOCUS_TABLE) # block of 4 calls
#       Collect field contents from all files, tokenize, and print token info
#       (including repetition); tokenizer is defined in local file. 15 Jun 2021
        all_docs_ftokens = get_all_field_tokens(FOCUS_TABLE, tag)
#       Remove tokens specified in list null_code_list.
#       This stopword list is defined in local file.
#       Currently we have defined only one stopword ('NULL'). 
#       Returns the new word list (from which stopwords have been removed);
#       how many words were removed, and the length of the new list.
#       15 Jun 2021 JK
        accepted_docs_ftokens = remove_tokens(all_docs_ftokens, null_code_list)
#       Returns the frequency distribution of the new word list
#       and prints the number of different words. 15 Jun 2021 JK 
        freksanasto = get_token_frequences(accepted_docs_ftokens) 
#       Prints words occurring in the target field in descending 
#       frequency order ("word freq"), in chunks of 20 files. 15 Jun 2021 JK
        ask_about_word_freq_information(basic_msg, skip, accept, freksanasto)
#       Create name for Omorfi output file; name prefix is defined in local file
#       15 Jun 2021 JK
        omorfi_out = CatenateFilename(O_out, tag)
# Uses Omorfi to analyze words in target field
# (omorfi-disambiguate-text.sh -X).
# We give input words in chunks of 400 words at a time, leading
# often to many input files.  Filename prefix for input is given
# in local file. One word per line is used in input.
#
# Function runs Omorfi analysis (text/Unicode), and saves the result 
# into output file, and prints its name to user.
# One output file is always formed, although there may be many 
# input files.
# N.B. Old output file is removed automatically.
# Note: variable sana_analyysit not used by function.
#       function calls function get_file_contents(), which is
#       called again in load_dict(). One of the function calls
#       is actually unnecessary. 15 Jun 2021 JK 
        sana_analyysit = run_omorfi(O_in, tag, omorfi_out, freksanasto)
#       Returns Omorfi analysis results as a dictionary
#       {'word1': 'analysis', 'word2': 'analysis'} 
#       15 Jun 2021 JK 
        d = load_dict(omorfi_out)
#       Checks that all tokens are found in the analysis dictionary 15 Jun 2021 JK
        verify_dict(d, freksanasto) # each key must be in dict
# Add to list variables target field's information: 
#   - freqwordlists: frequency distribution of tokenized word list
#   - dictionaries: morphological analysis in dictionary form
#   - focustables: FOCUS_TABLE: items as tuples (filename, [field contents])
#   - fields_triplets which is used later, which combines
#     the field tag, its analysis dictionary, and FOCUS_TABLE
# LOOP -- return to beginning of LOOP
# 15 Jun 2021 JK
        freqwordlists.append(freksanasto)
        dictionaries.append(d)
        focustables.append(FOCUS_TABLE)
        fields_triplets.append((tag, d, FOCUS_TABLE)) # 11 Jun 2021 JK

##############################################################################

# Program ends with error messages if the user has not intered exactly two
# field codes.

if len(freqwordlists) != 2:
    print("2 fields must be defined, found %d, exit." % len(freqwordlists))
    sys.exit()

# Next: information loading has been completed:
# START INFORMATION RETRIEVAL

print("OK. Kenttatietojen latausvaihe on loppuunsaatettu.\n")
print("ALOITETAAN TIEDONHAKU (JOHTOLANKOJEN KASITTELY).")

CHUNKS = 3 # report in 3 field-pairs chunks

##############################################################################

#fields_triplets = [("bsal", dictionaries[0], focustables[0]),\
#                   ("esal", dictionaries[1], focustables[1])]

# Above we assume that 2 field tags are given in order: bsal, esal.
# The variable was moved into loop above. 11 Jun 2021 JK

user_cmd = "x" # default start
while user_cmd != skip:
    all_fields_results = [] # will contain two sets for two fields
    for (tag, dict, focus_table) in fields_triplets: # LOOP over fields
        user_cmd = prompt("Anna hakuehto (%s) (%s = skip)" % (tag, skip))
        if user_cmd != skip:
#             Return list of dictionary keys, the value of which contains
#             the search string. 15 Jun 2021 JK.
#             e.g., value of key "Mona" is analysis " ... Female ..."
            word_matches = inspect_dict(dict, user_cmd)
#           Print the key list. 15 Jun 2021 JK.
            report_words(word_matches)
#           Seach result is simply a set of BIG_TABLE indexes
#           FOCUS_TABLE has corresponding indexes which are later
#           used for printing output results. 
            field_result = loc(word_matches, focus_table) # set of doc indexes
            all_fields_results.append(field_result) # list of sets of indexes
        else:
            sys.exit()  # N.B.! Here 
                        # "q=skip" works this way!
                        # 15 Jun 2021 JK


    # Form intersection of index sets (BIG_TABLE/FOCUS_TABLE)
    # regarding files (documents), fulfilling both search conditions  
    #
    # N.B.! We assume exactly 2 target fields (2 field tags)
    # in making result set and when we inform the user.
    # Please modify this if you need other kinds of search criteria.
    # 17 Jun 2021 JK
    resultset = all_fields_results[0].intersection(all_fields_results[1])
    print("* %d kirjetta tasmasi MOLEMPIIN ehtoihin." % (len(resultset)))
#   Number of letters matched BOTH search conditions.
    reply = prompt("Naytetaanko vastauksia? RETURN [q = quit, e = exit]")
#   Do we show results? Please enter RETURN to show (q to quit; e to exit).
    if "e" in reply or "E" in reply:
        print("* Ok. Keskeytetaan ohjelman suoritus.") # exit
        sys.exit() 

    # Both search conditions were matched:
    s_ti = "Kumpikin hakuehto tayttyi:" # title for search results
    ord = 1

    # resultset contains indexes of matching documents in lists
    # Show results in chunks of three:
    #    ("filename", "tag1 e.g. bsal")
    #    ("filename", "tag2 e.g. esal")    15 Jun 2021 JK
    for i in resultset: # DOC INDEX i
        if reply == "":   # with this CONDITION we print
            print("%s\n%s\n%s\n" % (s_ti, focustables[0][i],focustables[1][i]))
        if ord % CHUNKS == 0 and reply != 'q': # nice: CONDITION for asking
            reply = prompt("Lisaa? RETURN [q = skip]")
        ord += 1

    if reply == 'q':
        print("Keskeytys. Aloitetaan uusi haku.")

# End of program.
#################

# ALGORITHM: 
# (1) locate input files (ask location)
# (2) read each file as raw string
# (3) detect charset of file contents, e.g., ISO-8859-1 or UTF-8
# (4) decode files contents into Unicode:
#     -- save first level input data into BIG TABLE data structure
#     -- each line in BIG TABLE will correspond to one input file
#     -- each line is a 4-tuple of file-related information
#     -- technically, BIG TABLE is a list (of 4-tuples)
# (5) ask tag of field to analyze, select required field,
#     such as <bsal> or <esal>
# (6) tokenize field string
# (7) produce word-frequence distribution and other related information
# (8) run application such as Omorfi to analyze words (singular "NULL"
#     in field is the exception)
#
# War time letters example:
#   - user gives location of files containing Finnish historical letters
#   - encoding of inputs is UTF-8-SIG; will be decoded into Unicode
#   - field tag is "<bsal>" (denoting beginning salutation, i.e., greeting) 
#               or "<esal>" (denoting ending salutation, i.e., signature)
#
#    The original input data (raw data) may contain any character 
#    encoding, e.g., Latin-1, UTF-8-SIG, UTF-8 or other.
#
#    Whenever we write ourselves any text data subsequently into files, 
#    it will always be precisely UTF-8, and not for example UTF-8-SIG.
#
#    This is our way to get the control of the data.
#
#    Text files created will be arranged readily into UTF-8 (not anymore
#    the original encoding of the data, which might be something
#    different, e.g., UTF-8-SIG or Latin-1).
#
#    -However, strings are processed (in function bodies) in Unicode form.
##############################################################################

# end of file.


