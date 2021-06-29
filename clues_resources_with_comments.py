#############################################################################
# This file: clues_resources_with_comments.py
# Date: 5 Jun 2020, 31 May 2020 - started on 19 Apr 2020, comments added
#       29 June 2021
# Authors: Heikki Keskustalo
# Purpose: Defines prototypical functions to modify and use in "clues.py"
##############################################################################
 
from local_with_comments import * # please place local tool imports and paths into local.py

##############################################################################
# Name: prompt()
# Author: Heikki Keskustalo
# Date: 23 Apr 2020
# Purpose: Ask a question from the user
# In: question that we print for the user (string)
# Out: user reply (string)
##############################################################################
def prompt(question: str):
    question = question + ": "
    reply = input(question) # get answer from user 
    return reply            # string

##############################################################################
# Name: read_all_filenames()
# Authors: Heikki Keskustalo and Boyang Zhang
# Date: 22 Apr 2020
# Purpose: return all file names in given directory (will contain input texts)
# In: one directory (string)
# Out: list of filenames (strings)
##############################################################################
def read_all_filenames(subdirectory: str):
    result = os.listdir(subdirectory)
#   # ignore macOS metadata file. Jaana Kalliala (JK) 4 Jun 2021
#   # slows down program, do not use if not needed
#    if ".DS_Store" in result: 
#        ds = result.index(".DS_Store")
#        result.pop(ds)
    return result  # list of input filenames ['letter1.txt',...]

##############################################################################
# Name: get_raw()
# Author: Heikki Keskustalo
# Date: 25 Apr 2020
# Purpose: return file in original raw formatting string
# In: file name as full path name
# Out: file contents in raw format, i.e., no decoding is performed 
##############################################################################
def get_raw(input_filename):
    ifp = open(input_filename, "rb") # bytes file (Python 3)
    raw = ifp.read() # string
    ifp.close()  # close the file
    return raw

# Not currently in use 14 Jun 2021 JK

##############################################################################
# Name: return_decoded()
# Author: Heikki Keskustalo
# Date: 25 Apr 2020
# Purpose: decode string and return Unicode string
# In: raw string (may be in ISO-8859 family format or UTF-8 or UTF-16 etc.)  
# Out: input string but in Unicode format
##############################################################################
def return_decoded(raw):
    detection_result = chardet.detect(raw) # for example, UTF-8-SIG    
    original_data_encoding = detection_result['encoding']
    uraw = raw.decode(original_data_encoding) # UTF-8-SIG to Unicode
    return(uraw) # Unicode string (str)

# Not currently inuse 14 Jun 2021 JK

##############################################################################
# Name: get_basic_info()
# Author: Heikki Keskustalo
# Date: 26 Apr 2020
# Purpose: for one file return 4-tuple (basic information)
# In: directory path;
#     file name
# Out: 4-tuple ([0] filename without path (string);
#               [1] char encoding detected;
#               [2] raw file contents (original encoding);
#               [3] file contents decoded into Unicode
##############################################################################
def get_basic_info(input_directory: str, filename: str):
    full_filename = input_directory + filename
    ifp = open(full_filename, "rb") # bytes file (Python 3)
    raw = ifp.read()                # original char encoding
    ifp.close()                     # close file
    # chardet.detect() detects the character encoding
    # returns a dictionary in form {'encoding': 'Latin-1', 'confidence': 0.99}
    # 14 Jun 2021 JK
    detection_result = chardet.detect(raw) # e.g., UTF-8-SIG or Latin-1
    orig_encoding = detection_result['encoding']
    uraw = raw.decode(orig_encoding) # uraw is now in Unicode
    basic_info_tuple = (filename, orig_encoding, raw, uraw)
    return(basic_info_tuple)

##############################################################################
# Name: print_file_details_report()
# Author: Heikki Keskustalo
# Date: 2, 8 May 2020
# Purpose: Print individual file-level information on screen.
# In:  big_table: a list of tuples.
#      One tuple corresponds to one input file.
#      in tuple (e1, e2, e3, e4) elements e1-e4 have the following meaning:
#              (e1 = file name;
#               e2 = char encoding of original file;
#               e3 = original file contents [raw];
#               e4 = Unicode data [e4 decoded from e3] )
# Out: Boolean value True
##############################################################################
def print_file_details_report(big_table: list):
    CHUNKS = 20 # report 20 files info at a time on screen
    reply = ""
    titleline1 = ("#", "tiedosto", "merkisto-", "pituus", "pituus")
    titleline2 = (" ", " ", "koodaus", "(bytes)", "(code points)")

    print("%-5s %-19s %-10s %-7s %s" % titleline1) 
    print("%-5s %-19s %-10s %-7s %s" % titleline2)

    mx = len(big_table) # max files
    ord = 1             # file count
    for t in big_table: # go through each tuple
        if reply == "": # condition for printing report
            print("%d/%d %-19s %-10s %-7d %d" % \
               (ord, mx, t[0],  t[1], len(t[2]), len(t[3])))
        if ord % CHUNKS == 0 and reply != 'q': # conditions for asking
            reply = prompt("Paina RETURN [q = skip]")
            if reply == "":
                print("%-5s %-19s %-10s %-7s %s" % titleline1) 
                print("%-5s %-19s %-10s %-7s %s" % titleline2)
        ord += 1
    if reply == 'q':
        print("Jatketaan ...") # Continuing ...
    return True

##############################################################################
# Name: print_charset_info()
# Author: Heikki Keskustalo
# Date: 6 May 2020
# Purpose: Print individual file-level charset information on screen
# In:  big_table: a list of tuples.
# Out: Boolean value True
##############################################################################
def print_charset_info(big_table: list):
    charsets_observed = []
    for e in big_table:
        merkisto = e[1] # BIG_TABLE column [1] = charset detected
        charsets_observed.append(merkisto)
    # FreqDist() returns frequence distribution as dictionary
    # e.g., {'UTF-8': '213', ...} (14 Jun 2021 JK)
    fdist = nltk.FreqDist(charsets_observed) # repetition list of UTF-8 etc.
    char_sets_found = fdist.keys()
    for chset in char_sets_found:
        print("Merkistojakauma:\n" + \
              "    %d tiedostoa, joiden merkisto on %s" % \
                   (fdist[chset],                   chset))
    return True

##############################################################################
# Name: print_overall_report()
# Author: Heikki Keskustalo
# Date: 23 May 2020
# Purpose: Regarding all files, print general "ballpark figures" about
#          file lengths (average among all files, shortest file (min),
#          longest file (max) observed).
#          Two types of figures are given:
#          -based on raw information (e.g., UTF-8) 
#          -based on Unicode (code points) information.
#          File length may be larger for raw data than Unicode,
#          depending on encoding.
#          For example, Scandinavian letters such as "a with diaeresis" 
#          in UTF-8 take two bytes, but as code points they have length one.
#          Therefore, if raw data is UTF-8 it is the normal case that
#          Finnish texts are longer in raw format than observed as Unicode
#          code points. 
# In:  -BIG_TABLE
#      -index=[2] for raw data field
#      -index=[3] for Unicode field
# Out: Boolean value True
##############################################################################
def print_overall_report(big_table: list, column_index_raw: int, column_index_unicode: int):
    column_indexes = [column_index_raw, column_index_unicode]

    print("Pituusjakauma:")
    for column_index in column_indexes: # use (1) raw, (2) Unicode data
        shortest = -1      # shortest file length as raw or Unicode
        longest = 0        # longest file length as raw or Unicode
        summa = 0          # sum of all: (1) bytes or (2) Unicode Code Points
        for e in big_table: # go through elements e in big_table
            doclen = len(e[column_index]) # raw text or Code Points length
            if shortest == -1:    # very first file:
                shortest = doclen # is shortest so far.
            else:                 # Otherwise: new shorter becomes shortest   
                shortest = min(shortest, doclen) 
            longest =  max(longest, doclen)
            summa = summa + doclen
        print("* keskipituus: %.2f min: %-5d max: %-5d" % \
                             (summa/len(big_table), shortest, longest),\
                             end = '')
        if column_index == column_index_raw:
            print(" tavuina (Bytes)")
        elif column_index == column_index_unicode:
            print(" Unicode-merkkeina (code points)")
# Length distibutions above include all chars in files including tags and
# NULL strings
    print("Huom. pituusjakaumat ylla pitavat sisallaan tiedostojen kaikki")
    print("merkit mukaanlukien kenttakoodit (tags) ja NULL-arvot).")

    return True

##############################################################################
# Name: return_big_table()
# Author: Heikki Keskustalo
# Date: 3 May 2020
# Purpose: Return BIG_TABLE = list of 4-tuples 
#                             t = (filename, charset, raw data, Unicode data)
#               (t[0]: name of input file (as string);
#                t[1]: char encoding of the file (based on .detect());
#                t[2]: original raw contents of file (original char encoding);
#                t[3]: file contents in Unicode format (= decoded from raw))
#
# In: directory address of input files;
#     list of pure filenames in the directory (=without path) 
# Out: BIG_TABLE
#      each tuple contains information from one file
##############################################################################
def return_big_table(input_directory: str, filenames: list):
    big_table = [] # list of 4-tuples, one tuple for each file
    ord = 0
    for filename in filenames:
        ord = ord + 1
        if (ord % 100) == 0:
            print("* %d tiedostoa luettu." % (ord))
        file_info_tuple = get_basic_info(input_directory, filename)
        big_table.append(file_info_tuple) # add tuple to list of all tuples
    return big_table # list of 4-tuples

##############################################################################
# Name: get_field() # name modified to correspond the function (14.6.2021 JK)
# Authors: Heikki Keskustalo
# Date: 7 May 2020
# Purpose: Extract texts based on given tag
# In: document (as string);
#     field tag, e.g., "bsal" denoting <bsal> and </bsal> pair.
# Out: list of the strings extracted,
#      or empty list   
##############################################################################
def get_field(doc_string: str, tag: str):
    list_of_strings = []
    soup = BeautifulSoup(doc_string, 'lxml')
    # find_all(tag) = list with items such as ["<tag>contents</tag>", ...]
    # get_text() returns text inside tags, e.g., above: "contents"
    # (14.6.2021 JK)
    for element in soup.find_all(tag):
        contents_clip = element.get_text()
        list_of_strings.append(contents_clip)
    return list_of_strings

##############################################################################
# Name: get_focus_table()
# Authors: Heikki Keskustalo
# Date: 6 May 2020
# Purpose: From BIG_TABLE create and return small FOCUS_TABLE 
#          FOCUS_TABLE = list of 2-tuples t (one tuple per file), where 
#                        t = (filename, string in selected field):
#               (t[0]: name of original input file (as string), from which
#                     field string is extracted;
#                t[1]: contents of selected field as LIST of Unicode strings,
#                      e.g., for text "<bsal>Rakas</bsal>" if tag== "bsal"
#                      then we extract string "Rakas", and return ["Rakas"].  
#      N.B.! list t[1] normally has exactly one element. 
#
# In: BIG_TABLE: the Major data structure (list of 4-tuples);
#     field tag to search tokens (=words) from, e.g., "bsal" or "esal" 
#     (see above).
# Out: FOCUS_TABLE (list of 2-tuples) containing minimum information wanted:
#      file name of document and defined field contents extracted, as 
#      list of strings.
##############################################################################
def get_focus_table(big_table: list, search_tag: str):
    ord = 0
    focus_table = []    # list two-tuples t = (t[0],t[1]) 
    for e in big_table: # element e[3] contains file in Unicode
        fieldstringlist = get_field(e[3], search_tag) # e.g., ["Rakas vaimo"]
        focus_tuple = (e[0], fieldstringlist) # (filename; list of strings)
        focus_table.append(focus_tuple)
        ord += 1      
        if (ord % 100) == 0:
            print("* Kenttaa %s etsitty %d tiedostosta." % (search_tag, ord))
    return focus_table 

##############################################################################
# Name: evoluz_tokenize()
# Authors: Heikki Keskustalo
# Date: 7 May 2020
# Purpose: Tokenize string into a list of "words".
##############################################################################
def evoluz_tokenize(stringi: str):
    tokenlist = evoluztokenizer.tokenize(stringi) # see local.py for wtokenize
    return tokenlist # list

##############################################################################
# Name: print_fields_lengths()
# Author: Heikki Keskustalo
# Date: 8-9 May 2020
# Purpose: Print individual file-level information on screen
#          about given field.
# In:  FOCUS_TABLE: a list of 2-tuples;
#      search_tag: tag requested, e.g., "bsal" or "esal".
#
#      One fields-info  tuple corresponds to one input file.
#
#      We assume that there is one document per input file.
#
#      Usually exactly one requested field-tag exists per document (=file).
#
#  tuple (e1, e2) elements are:
#              (e1 = file name;
#               e2 = list of field strings (string may contain spaces,
#                    punctuation etc.) in selected field.
#
# Out: Boolean value True
##############################################################################
def print_fields_lengths(focus_table: list, tag: str):
    CHUNKS = 20 # print info on screen in chunks of 20 (files)
    reply = ""
    titleln = ("#", "tiedostonimi", "kentta", "kpl", "#", "merkkia")
    print("%-5s %-19s %-7s %-7s %-7s %-7s" % titleln)
    ord = 1 # file ordinal
    maxfiles = len(focus_table) # how many files are there?

    for t in focus_table: # go through each tuple in list
        if reply == "":   # CONDITION for printing ('q' prevents printing) 
            if len(t[1]) == 0: # 1 of 3: Field tag was missing.
                print("%d/%d %-19s %-7s %-7d %-7s %-7s" % \
                      (ord, maxfiles, t[0],  tag, len(t[1]), "-", "-")) 
            elif len(t[1]) == 1: # 2 of 3: Normal case: one multi-word field.
                field_strings = t[1] #                  e.g., ["Rakas vaimo"] 
                print("%d/%d %-19s %-7s %-7d %-7s %-7d" % \
                     (ord, maxfiles, t[0],  tag, len(t[1]), "1", \
                      len(field_strings[0]))) 
            elif len(t[1]) >= 2: # 3 of 3: Two or more fields.
                field_strings = t[1] # e.g., ["Rakas vaimo", "hei yllatys"] 
                field_o = 0 # here we need field ordinal (repeated fields)
                for field in field_strings:
                    field_o += 1 
                    print("%d/%d %-19s %-7s %-7d %-7d %-7d" % \
                         (ord, maxfiles, t[0], tag, len(t[1]), field_o, \
                          len(field))) 
        if reply != 'q'and ord % CHUNKS == 0: # CONDITION for asking what to do
            reply = prompt("Paina RETURN [q = skip]")
            if reply == "":
                print("%-5s %-19s %-7s %-7s %-7s %-7s" % titleln)
        ord += 1 # file ordinal
    if reply == 'q':
        print("Ok. Ohitetaan kenttien tulostus merkkijonoina.")
        print("Jatketaan kenttatietojen kasittelya.")

    return True

##############################################################################
# Name: print_fields_contents()
# Author: Heikki Keskustalo
# Date: 16 May 2020
# Purpose: Print field contents at individual file-level.
# In:  FOCUS_TABLE: a list of 2-tuples;
#      search_tag: tag requested, e.g., "bsal" or "esal".
#      The meaning of the tuple (e1, e2) elements is as follows:
#              (element 1 = original file name;
#               element 2 = list of strings in selected field)
# Out: Boolean value True
##############################################################################
def print_fields_contents(focus_table: list, search_tag: str):

    # search_tag is not currently used - could be used for monitoring
    # 21 Jun 2021 JK

    CHUNKS = 20 # report 20 files chunks
    reply = ""
    print("%-5s %-19s %s" % ("#", "tiedosto    ", "kenttasisalto"))
    ord = 1               # file count
    for t in focus_table: # go through each tuple
        if reply == "":   # CONDITION for printing field contents
            print("%-5d %-19s %s" % (ord, t[0],  t[1]))
        if ord % CHUNKS == 0 and reply != 'q': # CONDITIONS for asking
            reply = prompt("Paina RETURN [q = skip]")
            if reply == "":
                print("%-5s %-19s %s" % ("#", "tiedosto    ", "kenttasisalto"))
        ord += 1
    if reply == 'q':
        print("Jatketaan kenttatietojen kasittelya.\nKENTTA PILKOTTIIN SANOIKSI.")
    return True

##############################################################################
# Name: print_fieldam_info()
# Authors: Heikki Keskustalo
# Date: 16 May 2020
# Purpose: Report distribution of number of required tags among documents
# In:  FOCUS_TABLE: a list of 2-tuples;
#      search_tag: tag requested, e.g., "bsal" or "esal".
#      The meaning of the tuple (e1, e2) elements is as follows:
#              (element 1 = original file name;
#               element 2 = list of strings in selected field)
# Out: Boolean value True (lisätty/kopioitu ed. funktiosta 14.6.2021 Jaana Kalliala)
##############################################################################
def print_fieldam_info(focus_table: list, search_tag: str):
    fieldam_list = []     # e.g., 4133 integers expressing nr of search_tag
    for t in focus_table: # go through each tuple in list
        fieldam_list.append(len(t[1]))  # produces usually list [1, 1, ..., 1]
    fdist = nltk.FreqDist(fieldam_list) # repetition list of tag amounts
    field_amounts = fdist.keys()
    print("Kenttaa %s etsitty %d dokumentista: haun tulos:" % \
                  (search_tag, len(focus_table)))
    for am in field_amounts:
        print(" * ", fdist[am], "tiedostossa kussakin oli", \
               am, "kpl kenttia \"%s\"" % (search_tag))
    return True

##############################################################################
# Name: get_token_frequences()
# Authors: Heikki Keskustalo
# Date: 17 May 2020
# Purpose: For input list containing tokens with repetition,
#          return (token, frequence) pairs, ordered by frequence
# In:  list of tokens (including the repetition)
# Out: list of tuples:
#          (token, freq)
#      Example: for input list ['a', 'b', 'a']
#               we return tuple list [('a', 2), ('b', 1)]  
##############################################################################
def get_token_frequences(token_list: list):

    # N.B. lines marked with "###" are not needed 15 Jun 2021 JK

    token_freq_pairs = [] ###
    fdist = nltk.FreqDist(token_list)
    tokens = fdist.keys() ###
    for token in tokens: ###
        newtuple = (token, fdist[token]) ###
        token_freq_pairs.append(newtuple) ###
    token_freq_list = fdist.most_common()
    print("%d erilaista sanaa" % (len(token_freq_list)))
    return token_freq_list

##############################################################################
# Name: report_token_frequences()
# Authors: Heikki Keskustalo
# Date: 15 May 2020
# Purpose: For list of tuples t = (t[0], t[1]) = (token, freq)
#          report about tokens and related frequences.
# Note: we have here "nice model" for asking reply and reacting to it!
# In: list of 2-tuples
# Out: Boolean value True
#      Example: for input [('a', 2), ('b', 1)] report related information.
##############################################################################
def report_token_frequences(token_freq_list: list):
    CHUNKS = 20 # report 20 token chunks
    reply = ""
    otsikkorivi = ("sana ", "kpl     ", "-----", "--------")
    print("%s %s\n%s %s" % otsikkorivi)
    ord = 1               # file count
    for t in token_freq_list: # go through each tuple
        if reply == "":   # CONDITION for printing token information
            print("%s %d" % (t[0],  t[1]))
        if ord % CHUNKS == 0 and reply != 'q': # nice: CONDITION for asking
            reply = prompt("Paina RETURN [q = skip]")
            if reply == "":
                print("%s %s\n%s %s" % otsikkorivi)
        ord += 1
    if reply == 'q':
        print("Ok. Ohitetaan sanatietojen tulostusta.")
        print("jatketaan %d sanan kasittelya." % (len(token_freq_list)))
    return True

##############################################################################
# Name: get_file_contents()
# Authors: Heikki Keskustalo
# Date: 27 May 2020
# Purpose: get the contents of a file
# In: filename (name of the file as string)
# Out: file CONTENTS (Unicode string) 
##############################################################################
def get_file_contents(filename: str):
    ifp = open(filename, "r") # UTF-8 input file
    uraw = ifp.read()
    ifp.close()
    if isinstance(uraw, str): # 10 Sep 2019
        return uraw # Unicode file contents -- Python 3 change
    else:
        print("*** Fatal: unable to convert to Unicode.")
        sys.exit()
        return False

##############################################################################
# Name: create_omorfi_input_file()
# Authors: Heikki Keskustalo
# Date: 31 May 2020
# Purpose: Create text file containing "ladder" (=one word per line) of
#          words, at most 400 words in the ladder (cohort division).
#          Warning: this function first removes possible existing file.
# In:  name of the file in which we write the ladder string;
#      the ladder string containing the words.
# Out: Boolean value True
##############################################################################
def create_omorfi_input_file(omorfi_in_filename, cohort_ladder):
    os.system("/bin/rm -f " + omorfi_in_filename) # Remove old file if exists
    new_file = open(omorfi_in_filename, "w") # Prepare to write
    new_file.write(cohort_ladder)             # LADDER OF 400 WORDS
    new_file.close() # we have now input word in UTF-8 in file
    return True

##############################################################################
# Name: remove_omorfi_output_file()
# Authors: Heikki Keskustalo
# Date: 31 May 2020
# Purpose: Before starting Omorfi analyses we remove the old output file
#          if it exists.
# In:  Name of the Omorfi output file, in which we will spool results
#      of the morphological analysis, in chunks of 400 
# Out: Boolean value True
##############################################################################
def remove_omorfi_output_file(out_Omorfi_filename: str): 
    if "tmp" in out_Omorfi_filename:
        print("OK filename %s" % (out_Omorfi_filename))
        os.system("/bin/rm -f " + out_Omorfi_filename) # Remove old file
    else:
        print("Dangerous tmp file, exiting.")
        sys.exit()
    return True

    # comment: could be combined with function create_omorfi_output_file()
    # 21 Jun 2021 JK

##############################################################################
# Name: add_Omorfi_cohort_analyses()
# Authors: Heikki Keskustalo
# Date: 31 May 2020
# Purpose: Note: We run Omorfi for a cohort of words and add result at the end
#          of output file. If clues code is reused, other applications than
#          Omorfi, which produce clue-relevant metadata (such as gender), 
#          regarding the word tokens in selected XML fields, could be used 
#          instead.
# In:  Name of the Omorfi input (gradually in steps of 400 words) 
#      Name of the Omorfi output file (all words, e.g., to contain 1274 words)
# Out: Boolean value True
##############################################################################
def add_Omorfi_cohort_analyses(in_Omorfi_filename: str, out_Omorfi_filename: str):
    # command_path could be defined in local code file (15 Jun 2021 JK)
    command_path = "/home/username/omorfi/src/omorfi/src/bash/"  
    pure_command = "omorfi-disambiguate-text.sh -X "
    command = command_path + pure_command
    full_command_line_string = command + in_Omorfi_filename + \
                                 " >> " + out_Omorfi_filename
    os.system(full_command_line_string)

    return True

    # See Omorfi documentation for information regarding input and output
    # of omorfi-disambiguate-text

##############################################################################
# Name: create_omorfi_output_file()
# Authors: Heikki Keskustalo
# Date: 31 May 2020
# Purpose: Create empty file.  We will spool Omorfi analyses into this
#          file later, in chunks of 400 words.
# In: Name of the empty file which will be created 
# Out: Boolean value True
##############################################################################
def create_omorfi_output_file(out_Omorfi_filename: str): 
    new_file = open(out_Omorfi_filename, "w") # Prepare to write
    new_file.close() 
    return True

    # comment: could be combined with remove_omorfi_output_file() function
    # 21 Jun 2021 JK

##############################################################################
# Name: run_omorfi()
# Authors: Heikki Keskustalo
# Date: 25 May 2020
# Purpose: run Omorfi metadata for Finnish word
# In:  O_inflag: tmp filename substring defined in local.py
#      tag to use in several cohort-level input_filenames for Omorfi analyses;
#      name of output_filename where to print;
#      list of tuples (word, freq) of words to analyze.
#      -To avoid annoying error messages of using too large inputs,
#      we process the datas in cohorts of 400 words
# N.B.!
#      We need several input files for Omorfi (each has at most 400 words)
#      but this function will produce one Omorfi output file, not several.
# Out: Analysis result
##############################################################################
def run_omorfi(O_inflag: str, tag: str, out_Omorfi_filename: str, taajuussanasto: list):

    # Perform morphological analysis for the words
    print("Suoritetaan sanoille morfologinen analyysi.") 

    # Comment: these functions could be combined  15 Jun 2021 JK
    remove_omorfi_output_file(out_Omorfi_filename) # Remove old output file
    create_omorfi_output_file(out_Omorfi_filename) # Create empty output file

    start = 0                       # split into cohorts of 400 words
    stop = len(taajuussanasto) - 1  # ("mini ladders")
    css = 400 # cohort step size, e.g., [0]-[399], [400]-[799], etc.   

    # simply make for each cohort a unique input file

    for i in range(start, stop, css): # [0, 400, 800, ...]
        # Write into file a cohort-of-400-words (Omorfi input)
        cohort_ladder_string = ""
        for t in taajuussanasto[i:i+css]:
            cohort_ladder_string += t[0] + "\n" # Ladder of 400 words
        in_Omorfi_filename = O_inflag + tag + str(i) # several names are needed
        create_omorfi_input_file(in_Omorfi_filename, cohort_ladder_string)
        # Launch Omorfi for words cohort; ADD these result at the end of output
        add_Omorfi_cohort_analyses(in_Omorfi_filename, out_Omorfi_filename)

    # Get the desired text parts from Omorfi analysis output file
    analysis = get_file_contents(out_Omorfi_filename) 

    print("Morfologinen analyysi tiedostossa: %s" % (out_Omorfi_filename)) 
    return analysis # Unicode

    # get_file_contents(out_Omorfi_filename) is called both above and in
    # loc() function 21 Jun 2021 JK

##############################################################################
# Name: print_field_length_distribution()
# Author: Heikki Keskustalo
# Date: 20 May 2020
# Purpose: Print field length distribution (based on how many characters
#          field string contains, report the length distribution)
# In:  FOCUS_TABLE: a list of 2-tuples;
#              (element 1 = original file name;
#               element 2 = list of strings in selected field)
#      search_tag: tag requested, e.g., "bsal" or "esal".
# Example: 
# Out: Boolean value True
##############################################################################
def print_field_length_distribution(focus_table: list, search_tag: str):

    # search_tag is not currently used - could be used for reporting
     
    fieldlen_list = [] # one integer per field expressing its length

    for t in focus_table: # go through each tuple in list
        for field in t[1]:  # t[1] is a list of multi-words strings
            fieldlen_list.append(len(field)) # e.g., len("Dear wife") is 9
    fdist = nltk.FreqDist(fieldlen_list) 
    tulos = fdist.most_common()

    print("%-8s %-7s %-8s %-7s %-8s %-7s %-8s %-7s" % \
         ("kenttaa", "pituus", "kenttaa", "pituus", "kenttaa", "pituus", \
          "kenttaa", "pituus"))
    i = 0 # print 4 columns
    for (f_len, f_freq) in tulos: # go through, e.g., [..., (9, 456), ...]
        print("%-8d %-8d" % (f_freq, f_len), end='')
        i += 1
        if i % 4 == 0:
            print("")   
    print("")
    return True

##############################################################################
# Name: get_padding()
# Author: Heikki Keskustalo
# Date: 24 May 2020
# Purpose: Return short space string based on input integer
# In:  Integer determining output, e.g., for 34567 we want zero
#      padding, for 2345 we want 1 padding, for 837 we want 2 paddings,
#      for 75 we want 3 paddings, and for 5 we want 5 paddings. 
# Out: String of 0, 1, 2, 3 or 4 spaces
##############################################################################
def get_padding(freq: int):
    if freq >= 1 and freq <=9:
        pad = 4 * " "
    elif freq >= 10 and freq <=99:
        pad = 3 * " "
    elif freq >= 100 and freq <=999:
        pad = 2 * " "
    elif freq >= 1000 and freq <=9999:
        pad = 1 * " "
    else:
        pad = ""
    return(pad) # string which helps beaufity printing (tabulator is avoided)

##############################################################################
# Name: print_field_character_distribution()
# Author: Heikki Keskustalo
# Date: 20 May 2020
# Purpose: Print overall freq distribution of chars ('a', 'b', 'c', etc.)
#          in selected field.  
#          We are interested in how common various letters
#          and other symbols are in the selected field.
# In:  FOCUS_TABLE: a list of 2-tuples;
#              (element 1 = original file name;
#               element 2 = list of strings in selected field)
#      search_tag
# Out: Boolean value True
##############################################################################
def print_field_character_distribution(focus_table: list, search_tag: str):

    # search_tag is not currently used - could be used for monitoring 21 Jun 2021 JK

    char_list = [] # collect all individual characters here

    for t in focus_table: # go through each tuple in list
        for fstring in t[1]:  # t[1] is a list of multi-words strings
            merkkilista = [ch for ch in fstring] # "aab" -> ['a', 'a', 'b']
            char_list += merkkilista # always catenate new chars

    fdist = nltk.FreqDist(char_list) 
    ch_freq = fdist.most_common()

    # Characters (unicode escape form) with their frequences
    print("Merkit (unicode_escape -esitys) frekvensseineen:")
    format_string = "%-4s (%-3s)   %-4s (%-3s)   %-4s (%-3s)" + \
    "   %-4s (%-3s)   %-4s (%-3s)"
    format_tuple = ("ch", "kpl", "ch", "kpl", "ch", "kpl", "ch", \
                    "kpl", "ch", "kpl")

    print(format_string % format_tuple)
    i = 0 # print 5 columns
    for (ch, fr) in ch_freq: # go through, e.g., [('a', 456), ('i', 337), ...]
        print("%-3s (%d) " % (ch.encode("unicode_escape"), fr), end='')
        padding = get_padding(fr)
        # Formatting considers numbers of different lengths but not
        # characters of different lengths 14 Jun 2021 JK
        print("%s" % (padding), end='')
        i += 1
        if i % 5 == 0:
            print("")   
    print("")
    return True

##############################################################################
# Name: get_all_field_tokens()
# Author: Heikki Keskustalo
# Date: 24 May 2020
# Purpose: Cumulate all tokens from given field over all documents.
# In:  FOCUS_TABLE: a list of 2-tuples;
#      tag.
# Here:        (element 1 = original file name;
#               element 2 = list of strings in selected field)
# Here:         element 2 (in other words t[1]) is a list which normally has
#               one multi-word string, but we loop the list just in case
#               sometimes there might be more than one strings in the
#               list (depending on the input documents)
# Out: list of all tokens of given field type (cumulated over documents)
##############################################################################
def get_all_field_tokens(FOCUS_TABLE: list, tag: str):
    all_docs_ftokens = [] 
    for t in FOCUS_TABLE: # t = (filename, list of multi-word strings)
        doc_strings = "" 
        for field_string in t[1]: # we have only ONE multi-word string in t[1]
            doc_strings += field_string # if t[1] has not MULTIPLE STRINGS, 
            doc_strings += " "          # remove this line if necessary
        ftokens = evoluz_tokenize(doc_strings) # field tokens from one doc 
        all_docs_ftokens += ftokens # catenate field tokens from one doc to all
    # In the field ... we discovered altogether ... N words
    print("Kentassa %s havaittiin kaikkiaan %d sanaa (= mukana toisto!)" % \
                   (tag, len(all_docs_ftokens)))
    return(all_docs_ftokens) # list of all tokens in all docs in given field

##############################################################################
# Name: remove_tokens()
# Authors: Heikki Keskustalo
# Date: 5, 8 Jun 2020
# Purpose: given wordlist and stoplist (containing "NULL") as inputs,
#          removes stopwords ("NULL") from wordlist.
#          -Returns a new list.
#          -Reports how many "NULL" strings were encountered.
#          We assume that missing field values are marked as NULL,
#          for example <bsal>NULL</bsal>
# In: wordlist;
#     stoplist
# Out: new word list: wordlist from which stoplist elements have been removed
##############################################################################
def remove_tokens(wordlist: list, stoplist: list):
    newlist = []
    stopwordcount = 0 # how many NULLs are there?
    for word in wordlist:
        if word in stoplist:
            stopwordcount += 1
        else: # "NULL" is not accepted as a real word token
            newlist.append(word)
    print("NULL-sanoja kentassa havaittiin %d kpl." % (stopwordcount))
    print("NULL-sanojen poiston jalkeen %d juoksevaa sanaa." % len(newlist))
    return newlist

##############################################################################
# Name: load_dict()
# Author: Heikki Keskustalo
# Date: 27 May 2020
# Purpose: Performs the following sequence:
#          -reads existing Omorfi analyses for several word tokens (keys)
#          -splits file lines into tuples (key; Omorfi analyses)
#          This is non-trivial because the file format contains run time
#          comments starting with hashtag symbol (#) and we must see that
#          comments do not interfere with the data we desire.
#          -creates empty dictionary d = {}
#          -loads information into d: 
#          Note:
#               d[key] = Omorfi analyses
#          -returns the loaded dictionary d
# In:  Input file name (file contains the Omorfi analyses for all words)
# Out: dictionary d
##############################################################################
def load_dict(omorfi_analysis_file: str):
    s = get_file_contents(omorfi_analysis_file) # This is also performed in
                                                # run_omorfi() function, one
                                                # is unnecessary 21.6.2021 JK 
    d = {}
    # See Omorfi documentation for information about its output
    recordending = '\n\"<' # each one word with analyses ends this way
    keyword_separator = '>\"\n\t' # separates keyword  from its analyses

    lista = s.split(recordending) # individual word-level records 
    for record in lista:
        key_analyses = record.split(keyword_separator) 
        if len(key_analyses) != 2:
            print("Could not split Omorfi analysis line, exiting ...") 
            sys.exit()
        else:
            key = key_analyses[0]      # the word itself
            analyses = key_analyses[1] # Omorfi analyses of the word
            if key[0:2] == '\"<':
                key = key[2:] 
            d[key] = analyses
    return d

##############################################################################
# Name: verify_dict()
# Author: Heikki Keskustalo
# Date: 27 May 2020
# Purpose: Verifies that every key in token list is found in dict d.
#          Otherwise prints error messages. 
# In:  dictionary d;
#      list of tuples (word, freq)
# Out: Boolean value True
##############################################################################
def verify_dict(d: dict, taajuussanasto: list):
    found_keys = 0
    for tuple in taajuussanasto:
        word = tuple[0] # tuple[0]=word, tuple[1]=freq
        if word in d:
            found_keys += 1
        else:
            print("%s not in dictionary" % word)
    print("Omorfi-analyysit ladattu %d sanalle" % (found_keys))
    return True

##############################################################################
# Name: inspect_dict()
# Authors: Heikki Keskustalo
# Date: 31 May 2020
# Purpose: Return word matching Omorfi metadata search criterion
# In: d = {}  i.e., Omorfi output as dictionary (21 Jun 2021 JK)
#     user_string (here: substring to search)
# Out: Matching words as list
##############################################################################
def inspect_dict(d: dict, user_string: str):
    matching_words = []
    for key in d:
        if user_string in d[key]:
            matching_words.append(key)
    return matching_words # list

##############################################################################
# Name: ask_about_length_table()
# Authors: Heikki Keskustalo
# Date: 2 Jun 2020
# Purpose: General reporting function
# In: search_tag;
#     basic_msg;
#     skip;
#     accept;
#     FOCUS_TABLE
# Out: Boolean value True
##############################################################################
def ask_about_length_table(search_tag, basic_msg, skip, accept, FOCUS_TABLE):
    print("PITUUSTAULUKKO (%s)?" % (search_tag), end = '') 
    vastaus = prompt(basic_msg % (skip))
    if vastaus == accept:
        print_field_length_distribution(FOCUS_TABLE, search_tag)
    return True

##############################################################################
# Name: CatenateFilename
# Authors: Heikki Keskustalo
# Date: 6 Jun 2020
# Purpose: return catenated filename
# In: start string defined in local.py, usually "tmp_out_"
#     tag string, for example "bsal" or "esal"
# For one tag field we will create one large Omorfi output, but
#     we may need to create several Omorfi input files, because we
#     split the input onto cohorts of at most 400 lines.
# Out: catenated string (Omorfi output filename)
##############################################################################
def CatenateFilename(start: str, tag: str):
    filenamestring = start + "Omorfi_" + tag # start = "tmp_out_"
    return(filenamestring)

##############################################################################
# Name: ask_about_char_table()
# Authors: Heikki Keskustalo
# Date: 2 Jun 2020
# Purpose: General reporting function
# In: search_tag;
#     basic_msg;
#     skip;
#     accept;
#     FOCUS_TABLE
# Out: Boolean value True
##############################################################################
def ask_about_char_table(search_tag, basic_msg, skip, accept, FOCUS_TABLE):
    # Character table:
    print("MERKKITAULUKKO (%s)?" % (search_tag), end = '')
    vastaus = prompt(basic_msg % (skip))
    if vastaus == accept:
        print_field_character_distribution(FOCUS_TABLE, search_tag)
    return True

##############################################################################
# Name: ask_about_file_level_list()
# Authors: Heikki Keskustalo
# Date: 2 Jun 2020
# Purpose: General reporting function
# In: search_tag;
#     basic_msg;
#     skip;
#     accept;
#     FOCUS_TABLE
# Out: Boolean value True
##############################################################################
def ask_about_file_level_list(search_tag, \
                              basic_msg, skip, accept, FOCUS_TABLE):
    # Do we list amount of fields and lengths of fields?
    print("Listataanko kenttien (%s) maara- ja pituus" % (search_tag))
    print("tiedostoittain?", end = '')
    vastaus = prompt(basic_msg % (skip))
    if vastaus == accept:
        print_fields_lengths(FOCUS_TABLE, search_tag)
    return True

##############################################################################
# Name: ask_about_field_contents()
# Authors: Heikki Keskustalo
# Date: 2 Jun 2020
# Purpose: General reporting function
# In: search_tag;
#     basic_msg;
#     skip;
#     accept;
#     FOCUS_TABLE
# Out: Boolean value True
##############################################################################
def ask_about_field_contents(search_tag, basic_msg, skip, accept, FOCUS_TABLE):
    # Do we show field contents (strings)?
    print("Naytetaanko kenttien (%s) sisalto (merkkijonot)?" % (search_tag))
    vastaus = prompt(basic_msg % (skip))
    if vastaus == accept:
        print_fields_contents(FOCUS_TABLE, search_tag)
    return True

##############################################################################
# Name: ask_about_word_freq_information()
# Authors: Heikki Keskustalo
# Date: 2 Jun 2020
# Purpose: General reporting function
# In: basic_msg;
#     skip;
#     accept;
#     frekvenssisanasto 
# Out: Boolean value True
##############################################################################
def ask_about_word_freq_information(basic_msg, skip, accept, \
                                    frekvenssisanasto):
    # Do we list word and frequence information?
    print("Listataanko sanasto- ja frekvenssitiedot?", end = '')
    vastaus = prompt(basic_msg % (skip))
    if vastaus == accept:
        report_token_frequences(frekvenssisanasto)
    return True

##############################################################################
# Name: GET_FIELD_INFORMATION()
# Authors: Heikki Keskustalo
# Date: 2 and 6 Jun 2020
# Purpose: Returns a pair (FOCUS_TABLE, search_tag) based on user-given field
#          If field is RETURN then exit symbol for request was observed.
#          N.B.! FOCUS_TABLE is limited to FIELD-RELATED information!
# In: BIG_TABLE;
#     fieldcount = (1, 2, ...) ordinal of requested field so far
# Out: pair (FOCUS_TABLE, search_tag)
##############################################################################
def GET_FIELD_INFORMATION(BIG_TABLE: list, fieldcount: int):
    # Start working with field ... GIVE FIELD TAG (e.g., bsal or esal)
    # or RETURN to move into searching phase
    print("Otetaan kasittelyyn kentta %d" % (fieldcount))
    print("ANNA KENTTAKOODI (esim. bsal tai esal) tai RETURN")
    search_tag = prompt("siirtyaksesi HAKUVAIHEESEEN ---------------->")

    if search_tag == "":
        FOCUS_TABLE = []   
    elif search_tag == "q":
        print("Virheellinen kentta %s, exit." % (search_tag))
        search_tag = "" # N.B.! q is not accepted field symbol
        FOCUS_TABLE = []
        sys.exit()
    else:
        print("Etsitaan kenttia (%s), odota ..." % (search_tag)) # Searching
        FOCUS_TABLE = get_focus_table(BIG_TABLE, search_tag)
    return (FOCUS_TABLE, search_tag)

##############################################################################
# Name: report_words()
# Authors: Heikki Keskustalo
# Date: 2, 13 Jun 2020
# Purpose: prints word list information
# In: word list
# Out: Boolean value true
##############################################################################
def report_words(matching_words):
    # The following words matched the search criterion:
    print("* Seuraavat sanat tasmasivat hakuehtoon:")
    for w in  matching_words:
        print("%s " % w, end='')
    print("")
    return True

##############################################################################
# Name: loc()
# Authors: Heikki Keskustalo
# Date: 2 Jun 2020
# Purpose: returns a set of BIG_TABLE indexes of those docs
#          the given field of which contains the token in word list
# In: list: word list
# Out: set: set of indexes of documents which have field containing that word
##############################################################################
def loc(search_words, FOCUS_TABLE):
    s1 = "hakuehtoon tasmaavaa" # matching search conditions:
    s2 = "kirjetta" # "letters" could be "documents" (16 Jun 2021 JK)
    doc_matches = [] # indexes (same as in BIG TABLE) of matching docs

    # Numbers FOCUS_TABLE items (start=zero), thus numbers correspond to 
    # indexes of items in lists. FOCUS_TABLE and BIG_TABLE lists have 
    # same items in same order, thus their indexes correspond each other.
    # FOCUS_TABLEs are actually used but description refers to BIG_TABLE 
    # which is the starting point to form distinct FOCUS_TABLEs.
    # 
    # Retrieved set is here based on the intersection of the 
    # matching results for the given search conditions, and
    # it can be used for printing results (17 Jun 2021 JK)
    for (i, t) in enumerate(FOCUS_TABLE, start=0): # t = (fname; list of multi-word strings)
        docs_field_strings = ""
        for field_string in t[1]: # only ONE multi-word string appears in t[1]
            docs_field_strings += field_string # if t[1] has not multiple items,
            docs_field_strings += " "          # remove this line if necessary.
                                               # (Same observation as in function
                                               # get_all_field_tokens())
        ftokens = evoluz_tokenize(docs_field_strings) # doc's field tokens 
        match_found = False
        for w in search_words: # check every doc regarding all search words
            if not match_found:
                if w in set(ftokens):
                     match_found = True    # if search word found in field
                     doc_matches.append(i) # then save index of this doc
    doc_set = set(doc_matches) # set from a list
    print("\n* Loydettiin %d %s %s:" % (len(doc_set), s1, s2))
    return(doc_set) # set of doc indexes containing any required word

##############################################################################
# Name: ask_BLOCK()
# Authors: Heikki Keskustalo
# Date: 5 Jun 2020
# Purpose: Performs sequence of function calls. They ask user
#          whether he/she wants to see various types of monitoring
#          information reported.
# In: search_tag;
#     basic_msg;
#     skip;
#     accept;
#     FOCUS_TABLE.
# Out: Boolean value True
##############################################################################
def ask_BLOCK(search_tag, basic_msg, skip, accept, FOCUS_TABLE):
    ask_about_length_table(search_tag, basic_msg, skip, accept, FOCUS_TABLE)
    ask_about_char_table(search_tag, basic_msg, skip, accept, FOCUS_TABLE)
    ask_about_file_level_list(search_tag, basic_msg, skip, accept, FOCUS_TABLE)
    ask_about_field_contents(search_tag, basic_msg, skip, accept, FOCUS_TABLE)
    return True

# added default types of parameters to functions 14 Jun 2021 JK