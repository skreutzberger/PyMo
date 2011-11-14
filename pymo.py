#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

PyMo  - The Simple Terminal Browser for MongoDB

Licensed under the FreeBSD License 
------------------------------
Copyright (c) 2011 Sebastian Kreutzberger. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY SEBASTIAN KREUTZBERGER ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL SEBASTIAN KREUTZBERGER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Sebastian Kreutzberger.

Further links, helpful for development:
http://api.mongodb.org/python/current/api/pymongo/index.html
http://pypi.python.org/pypi/pymongo/
http://www.sanhu123.com/computer/362-working-with-mongodb-and-pymongo.html
http://www.youlikeprogramming.com/2010/12/python-and-mongodb-using-pymongo-quick-reference/
"""
import sys, time, os
from pprint import pprint
import pymongo

class Pymo:

    green = '\033[0;32m'
    yellow = '\033[0;33m'
    red = '\033[0;31m'
    reset = '\033[00m'

    conn = None
    conn_name = None
    db = None
    db_name = None
    coll = None
    coll_name = None
    doc_id = None
    doc = None
  
    def  __init__(self):
        self.enter_host()

    def quit(self):
        print("Goodbye!")
        exit()
    
    def clear(self):
        os.system('clear')  

    def enter_host(self):
        while True:
            inp = ""
            loop = True
            while loop:
                inp = raw_input(self.yellow+"Host (leave empty for localhost): "+self.reset)
                if not inp:
                    inp = "localhost"
                if inp == "q":
                    self.quit()
                try:
                    self.conn = pymongo.Connection(inp, 27017)
                    loop = False
                except:
                    print("Could not connect to "+inp)
                    pass
            self.conn_name = inp
            self.select_database()
     

    def select_database(self):
        while True:
            self.clear()
            counter = 1
            results = self.conn.database_names()
            print(self.green+"Existing databases at "+self.conn_name+":"+self.reset)
            for result in results:
                print(str(counter)+" "+result)
                counter = counter + 1 
            loop = True
            while loop:
                inp = raw_input(self.yellow+"Database (1-"+str(counter-1)+"): "+self.reset)
                if inp == "q":
                    self.quit()
                if inp == "b":
                    return False
                if inp == "r":
                    loop = False
                if inp != "r": 
                    valid_input = False
                    try:
                        inp_int = int(inp)
                        if inp_int > 0 and inp_int <= counter-1:
                            valid_input = True
                        else:
                            print(self.red+"Please enter a value between 1 and "+str(counter-1)+self.reset)
                    except:
                        print(self.red+"Please enter a numeric value."+self.reset)     
                    if valid_input:
                        self.db_name = results[inp_int-1]
                        try:
                            self.db = self.conn[self.db_name]    
                            loop = False
                        except:
                            print(self.red+"Could not use database "+self.db_name+self.reset)
            self.select_collection()
            
            
    def select_collection(self):
        while True:
            self.coll = None
            self.clear()
            counter = 1
            results = self.db.collection_names()
            print(self.green+"Existing collections in "+self.db_name+":"+self.reset)
            for result in results:
                print(str(counter)+" "+result)
                counter = counter + 1 
            loop = True
            while loop:
                inp = raw_input(self.yellow+"Collection (1-"+str(counter-1)+"): "+self.reset)
                if inp == "q":
                    self.quit()
                if inp == "b":
                    return False
                if inp == "r":
                    loop = False
                if inp != "r": 
                    valid_input = False
                    try:
                        inp_int = int(inp)
                        if inp_int > 0 and inp_int <= counter-1:
                            valid_input = True
                        else:
                            print(self.red+"Please enter a value between 1 and "+str(counter-1)+self.reset)
                    except:
                        print(self.red+"Please enter a numeric value."+self.reset)     
                    if valid_input:
                        self.coll_name = results[inp_int-1]
                        self.coll = self.db[self.coll_name]  
                        try:
                            self.coll = self.db[self.coll_name]    
                            loop = False
                        except:
                            print(self.red+"Could not use collection "+self.coll_name+self.reset)
            if self.coll:
                self.show_latest_documents()

    def show_latest_documents(self):
        while True:
            self.doc = None
            self.clear()
            results = self.coll.find()
            documents = []
            for result in results:
                if "_id" in result:

                    documents.append(result)
            if len(documents) > 0:
                print(self.green+"Existing documents in "+self.coll_name+":"+self.reset)
                counter = 1
                for document in documents:
                    print(str(counter)+" "+str(document["_id"]))
                    counter = counter + 1     
            else:
                print("The collection is empty")      
            loop = True
            while loop:
                if len(documents) > 0:
                    inp = raw_input(self.yellow+"Document (1-"+str(counter-1)+"): "+self.reset)
                else:
                    inp = raw_input(self.yellow+"Your options are [b]ack, [r]eload, [q]uit: "+self.reset)    
                if inp == "q":
                    self.quit()
                if inp == "b":
                    return False
                if inp == "r":
                    loop = False
                if inp != "r":
                    valid_input = False
                    try:
                        inp_int = int(inp)
                        if inp_int > 0 and inp_int <= counter-1:
                            valid_input = True
                        else:
                            print(self.red+"Please enter a value between 1 and "+str(counter-1)+self.reset)
                    except:
                        print(self.red+"Please enter a numeric value."+self.reset)     
                    if valid_input:
                        self.doc = documents[inp_int-1]
                        self.doc_id = documents[inp_int-1]["_id"]
                        loop = False
            if self.doc:
                self.show_document()

    def show_document(self):
        while True:
            self.clear()
            result = self.coll.find_one({"_id": self.doc_id})
            if result:
                pprint(result)   
            else:
                print(self.green+"The document with the id "+str(self.doc_id)+" is not existing"+self.reset)      
            loop = True
            while loop:
                if result:
                    inp = raw_input(self.yellow+"Your options are [u]pdate, [d]elete, [b]ack, [r]eload, [q]uit: "+self.reset)
                else:
                    inp = raw_input(self+yellow+"Your options are [b]ack, [r]eload, [q]uit: "+self.reset)    
                if inp == "q":
                    self.quit()
                if inp == "b":
                    return False
                if inp == "r":
                    loop = False
                if inp != "r":
                    valid_input = False
                    
                    if inp == "d":
                        self.coll.remove({'_id': self.doc_id})
                        return False
                    if inp == "u":
                        #print("This feature is not implemented, yet. Sorry!")
                        self.update_document()
                        loop = False


    def update_document(self):
        while True:
            self.clear()
            result = self.coll.find_one({"_id": self.doc_id})
            if not result:
                print(self.green+"The document with the id "+str(self.doc_id)+" is not existing"+self.reset)  
                return False 
            else:
                inp_key = raw_input(self.yellow+"Field name you want to update/insert (leave empty to go back): "+self.reset)
                if not inp_key:
                    return False
                inp_value = raw_input(self.yellow+"Field value: "+self.reset)
                try:
                    self.coll.update({'_id': self.doc_id}, {'$set': {inp_key: inp_value}}, upsert = True)
                    inp_try = raw_input(self.yellow+"Update another field ([y]es or [n]o): "+self.reset)
                    if inp_try != "y":
                        return False   
                except:
                    print(self.red+"Could not update the document"+self.reset)
                    inp_try = raw_input(self.yellow+"Try again ([y]es or [n]o): "+self.reset)
                    if inp_try != "y":
                        return False        
        

##########
# ! Output
###########
os.system('clear')  
print("Welcome to PyMo - the simple terminal browser for MongoDB.")
print("Keys that always work: [b]ack, [r]eload & [q]uit.")
pm = Pymo()
	