#!/bin/python3

# quoteloader.py
#
# author: Eddy Wong
# date: Oct 13, 2020 

# import the existing word and sentence tokenizing  
# libraries 

# Imports
import csv
from hashlib import sha1
# NLP imports
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize 
# DSE imports
from cassandra.cluster import Cluster, EXEC_PROFILE_GRAPH_DEFAULT
from cassandra.datastax.graph import GraphProtocol
from cassandra.datastax.graph.fluent import DseGraph



class QuoteLoader:
    def __init__(self, name):
        self.name = name

    ############################################################
    # def initialize(self)
    # Class function Initialize. Any boot-up calls here, like 
    # loading the timezone table
    # Param: None
    # Return: [side effect] It loads the timezone table
    # and sets a class variable that points to it
    ############################################################
    def initialize(self):
        print("Initialize")

        # Loading or defining stop lists

        # Stop list comming from nltk
        self.stop_words = set(stopwords.words('english'))

        # My own custom stoplist
        self.custom_stop_words = {'.', '-', "'s", 'it','and','is','...','so'}


    ############################################################
    # def connect(self,ip):
    # Class function to connect to DSE
    # Param: ip - IP address where DSE server lives
    # Return: [side effect] It inits a session variable that keeps
    # a connection to DSE
    ############################################################
    def connect(self,ip):
        # Not blank
        if ip and ip.strip():
            self.ip = ip
        else:
            self.ip = '10.101.33.239' # default

        # Create an execution profile, using GraphSON3 for Core graphs
        self.ep = DseGraph.create_execution_profile(
            'gquotes',
            graph_protocol=GraphProtocol.GRAPHSON_3_0)
        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: self.ep}, contact_points=[self.ip])
        self.session = self.cluster.connect()

        self.g = DseGraph.traversal_source(session=self.session)

    ########################################
    # Convenience function to gen SHA1 hash
    def make_sha1(s, encoding='utf-8'):
        return sha1(s.encode(encoding)).hexdigest()


    def processFile(self, file):

        # Dict objs
        person = {}
        quote = {}
        keyword = {}


        with open(file) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
            
            # skipping header
            next(csvreader)

            for row in csvreader:

                # The third column is the quote
                quote_str = row[5]
                person['name'] = row[1]
                person['title'] = row[2]
                person['company'] = row[3]

                print("== " + person['name'] + " ==")
                self.addPersonToG(person)

                print("=== Quote ===")
                quote['snippet'] = quote_str
                quote['quote_id'] =  QuoteLoader.make_sha1(quote['snippet'])
                
                print(quote['snippet'])
                keyw_list = []
                keyw_list = self.processQuote(quote['snippet'])

                self.addQuoteToG(quote)

                self.addMentionedToG(person, quote)

                for k in keyw_list:
                    keyword['key'] = k
                    self.addKeywordToG(keyword)

                    self.addFoundinToG(keyword, quote)

                    self.addImpliedToG(person, keyword)



    #######################################################
    # Given a quote (string), returns an array of keywords
    def processQuote(self, quote):

        filtered_sentence = []
        stopped_sentence = []

        print("=== Quote ===")
        print(quote)

        word_tokens = word_tokenize(quote)
        
        # convert to lowercase
        filtered_sentence  = [w.lower() for w in word_tokens]

        # filter by stop words
        for w in filtered_sentence: 
            if w not in self.stop_words and w.isalpha() and w not in self.custom_stop_words: 
                stopped_sentence.append(w.lower()) 
          
        print("== Raw Tokens ==")
        print(word_tokens)

        #filtered_sentence = [w for w in word_tokens if not w in custom_stop_words] 

        print("== Filtered ==") 
        print(stopped_sentence)

        return stopped_sentence

    ######################
    # Processes one row
    def processRow(self, row):
        print("Processing row")



    # Vertex Adding convenience functions

    def addPersonToG(self, person):
        
        sha_id = QuoteLoader.make_sha1(person['name'])
        print ("Adding Person: " + person['name'] + "|" + sha_id)

        # TODO: Check if person exists first
        
        p = self.g.addV('person') \
            .property('person_id', sha_id) \
            .property('company', person['company']) \
            .property('name', person['name']) \
            .property('title', person['title']) \
            .next()
        

    def addQuoteToG(self, quote):
        print ("Adding Quote")

        sha_id = QuoteLoader.make_sha1(quote['snippet'])
        print ("Adding Quote: " + quote['snippet'][0:10] + "|" + sha_id)

        q = self.g.addV('quote') \
            .property('quote_id', sha_id) \
            .property('snippet', quote['snippet']) \
            .next()

    def addKeywordToG(self, keyword):

        print ("Adding Keyword: " + keyword['key'] )

        # TODO: Check if exists, if yes, increase count

        q = self.g.addV('keyword') \
            .property('key', keyword['key']) \
            .next()

    # Edge Adding convenience Functions

    def addMentionedToG(self, person, quote):
        # Person -> Quote
        print ("Adding Mention")

        traversal1 = self.g.V().has('person', 'name', person['name'])

        traversal2 = traversal1.addE('mentioned') \
            .to(self.g.V().has('quote', 'quote_id', quote['quote_id']))

        traversal2.iterate()


    def addFoundinToG(self, keyword, quote):

        # Keyword -> Quote
        print ("Adding Foundin")

        traversal1 = self.g.V().has('keyword', 'key', keyword['key'])

        traversal2 = traversal1.addE('foundin') \
            .to(self.g.V().has('quote', 'quote_id', quote['quote_id']))

        traversal2.iterate()

    def addImpliedToG(self, person, keyword):
        # Person -> Keyword
        print ("Adding Implied")

        traversal1 = self.g.V().has('person', 'name', person['name'])

        traversal2 = traversal1.addE('implied') \
            .to(self.g.V().has('keyword', 'key', keyword['key']))

        traversal2.iterate()



if __name__ == '__main__':
    ql = QuoteLoader("ql1")         # Constructor
    ql.initialize()                 # Init
    ql.connect('10.101.33.239')     # Connect


    ql.processFile("golden-quotes1.csv")
    #ql.readFile("golden-quotes.csv.csv")  


