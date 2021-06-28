# Clues – Description, Notes and Ideas for Modifications

28.06.2021 Jaana Kalliala and Heikki Keskustalo

## Purpose

*Clues* is a general-purpose tool designed for non-topical information interaction. The program interactively reads XML-tagged text documents from a given directory, reports statistics the user wants, and allows searching within XML fields specified by the user. The contents of the fields can be morphologically analysed (`<tag>This text is analysed.</tag>`) and the search performed based on the words in the fields and/or their metadata. 

*Clues* can be tailored to meet the user’s needs. The present version, for example, interacts with the user in Finnish and uses the [Omorfi application](https://github.com/flammie/omorfi) to perform morphological analysis on Finnish text. This application can be replaced with other analysis tools.

## Input

*Clues* is given the path to the directory containing input documents. To allow calculation of statistics, the directory must only contain input documents intended, no other files. One file should correspond to one document and the documents must include XML field tags. Field tags and search terms given by the user can be used as input for the program during interactive searching.


## Process

The process begins with locating the input information directory specified by the user. Each file is read as raw data, the original character encoding (e.g., ISO-8859-1 or UTF-8) of the files is detected, and the files are decoded into Unicode format. This information is saved into a list variable named `BIG_TABLE`. Each item in `BIG_TABLE` list corresponds to one input file.

Next, the user is asked to provide two XML tag names, which are processed one at a time. Based on a tag given by the user, the data structure `FOCUS_TABLE` for each tag type is formed. This is a list that consists of 2-tuples, where the first item of the tuple is the file name, and the second is a list of tag contents (usually a one-item-list, since in most cases each tag occurs only once within a document). The text content of the selected field tag is tokenised next; then analysis on the tokens is performed (we used Omorfi). An output file is created and the morphological analysis results are saved into the file.

During each step, user-selected listings and statistics are printed in detail. Statistics include amounts, lengths and frequency distributions of characters or words. The statistics can be field or document specific; or they can combine data from all documents.

This is followed by the search phase. In the present version the user gives one search key for each tag provided earlier.

The morphological analysis in this version includes metadata (e.g. parts of speech, grammatical cases or genders associated with proper names), but also all the word tokens themselves as they appear in the original documents and their lemmatized (i.e. dictionary) forms. It is possible to search all of these.

As the last step, the results matching all the search criteria are printed (file names and tag field contents).


## Output

As the final output, *Clues* gives the filenames and XML field contents matching all the user-specified search criteria. Also as a needed step, a morphological analysis file is created and statistics and listings printed for the user (e.g. frequency distributions).


## Notes

* Functions `get_raw()` and `return_decoded()` defined in `clues_resources.py` are not used (`get_basic_info()` performs these actions)
* Functions `remove_omorfi_output_file()` and `create_omorfi_output_file()` could be combined
* `command_path` defined in `add_Omorfi_cohort_analyses()` could be moved to `local.py`
* If you use Omorfi application, please see documentation of command `omorfi-disambiguate-text` – what kind of format the input for Omorfi should be, and what the analysis output file looks like
* More information on the tokenizer used: see evoluztokenizer
* The function `get_file_contents(omorfi_analysis_file)`, which opens and reads the Omorfi analysis file, is called by two functions `run_omorfi()` and `load_dict()`, but only one is actually necessary. `run_omorfi()` also returns the analysis in a dictionary form, but this is not used anywhere.
* The program allows the user to give any number of tags, but the present version requires using 2 tags
* Exception: `quit` (`‘q’`) is not allowed as tag

## Ideas for Modifications

* Possibility to search more than two fields simultaneously
* Dividing the code into segments (e.g. all the code connected to Omorfi into one segment for easier replacement)
* The case of gender searching: typology lists of words that reveal gender (e.g. sister)
* Possibility to exclude words as search keys used (e.g. when dealing with historical letters in Finnish, it would be practical to be able to exclude proper names in allative in ending salutation field)