
# quoteloader.py
#
# author: Eddy Wong
# date: Oct 13, 2020 

# import the existing word and sentence tokenizing  
# libraries 

import csv
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize 

stop_words = set(stopwords.words('english'))

custom_stop_words = {'.', '-', "'s", 'it','and','is','...','so'}

filtered_sentence = []

with open('golden-quotes1.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in spamreader:

        quote = row[3]
        print("=== Quote ===")
        print(quote)

        word_tokens = word_tokenize(quote)
        
        #filtered_sentence = [w for w in word_tokens if not w in stop_words]
        #filtered_sentence = [w for w in word_tokens if not w in custom_stop_words] 
          
        for w in word_tokens: 
            if w not in stop_words and w.isalpha(): 
                filtered_sentence.append(w.lower()) 
          
        print("== Tokens ==")
        print(word_tokens)

        #filtered_sentence = [w for w in word_tokens if not w in custom_stop_words] 

        print("== Filtered ==") 
        print(filtered_sentence) 

#print("== Stop_words ==")
#print(stop_words)

