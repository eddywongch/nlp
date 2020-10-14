
# quoteloader.py
#
# author: Eddy Wong
# date: Oct 13, 2020 

# import the existing word and sentence tokenizing  
# libraries 

import csv
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize 

# Stop list comming from nltk
stop_words = set(stopwords.words('english'))

# My own custom stoplist
custom_stop_words = {'.', '-', "'s", 'it','and','is','...','so'}

filtered_sentence = []
stopped_sentence = []

with open('golden-quotes1.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    next(csvreader)

    for row in csvreader:

        # The third column is the quote
        quote = row[3]
        print("=== Quote ===")
        print(quote)

        word_tokens = word_tokenize(quote)
        
        #filtered_sentence = [w for w in word_tokens if not w in stop_words]
        #filtered_sentence = [w for w in word_tokens if not w in custom_stop_words] 
        
        # convert to lowercase
        filtered_sentence  = [w.lower() for w in word_tokens]

        for w in filtered_sentence: 
            if w not in stop_words and w.isalpha() and w not in custom_stop_words: 
                stopped_sentence.append(w.lower()) 
          
        print("== Raw Tokens ==")
        print(word_tokens)

        #filtered_sentence = [w for w in word_tokens if not w in custom_stop_words] 

        print("== Filtered ==") 
        print(stopped_sentence) 

#print("== Stop_words ==")
#print(stop_words)

