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
            self.ip = '10.101.33.239'

        # Create an execution profile, using GraphSON3 for Core graphs
        self.ep = DseGraph.create_execution_profile(
            'gquotes',
            graph_protocol=GraphProtocol.GRAPHSON_3_0)
        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: self.ep}, contact_points=[self.ip])
        self.session = self.cluster.connect()

        self.g = DseGraph.traversal_source(session=self.session)

    # Convenience function
    def make_sha1(s, encoding='utf-8'):
        return sha1(s.encode(encoding)).hexdigest()


    def readFile(self, file):
        with open(file) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
            
            # skipping header
            next(csvreader)

            for row in csvreader:

                # The third column is the quote
                quote = row[5]
                person = row[1]

                print("== " + person + " ==")
                self.addPerson(person)

                print("=== Quote ===")
                print(quote)

                self.processQuote(quote)


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




    def addPerson(self, person):
        #def make_sha1(s, encoding='utf-8'):
        #return sha1(s.encode(encoding)).hexdigest()
        
        sha_id = QuoteLoader.make_sha1(person)
        print ("Adding Person: " + person + "|" + sha_id)

        
        p = self.g.addV('person') \
            .property('person_id', sha_id) \
            .property('company', 'DataStax') \
            .property('name', person) \
            .property('title', 'CEO') \
            .next()
        



    def addQuote(self, quote):
        print ("Adding Quote")

    def addKeyword(self, keyword):
        print ("Adding Keyword")


    def addMention(self, person, quote):
        print ("Adding Mention")

    def addFoundin(self, keyword, quote):
        print ("Adding Foundin")

    def addImplied(self, keyword, quote):
        print ("Adding Implied")



if __name__ == '__main__':
    ql = QuoteLoader("ql1")         # Constructor
    ql.initialize()                 # Init
    ql.connect('10.101.33.239')     # Connect


    ql.readFile("golden-quotes1.csv")
    #ql.readFile("golden-quotes.csv.csv")  


