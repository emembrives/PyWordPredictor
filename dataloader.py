# -*- coding: utf-8 -*-
# PyWordPredictor - XML-RPC word prediction server
# Copyright (C) 2010 - Etienne Membrives
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import nltk, re, locale

import worddatabase as wdb


class DataImporter(object):
    def __init__(self,files):
        self.files=files
        self.database = wdb.Database("data.sql")
        self.database.clear()

        self._prepare_text()

    def _prepare_text(self):
        for p in self.files:
            f=open(p,'r')
            data=f.read()
            data=data.split('\n\n')
            data=map(lambda x:x.replace('\n',' '),data)
            data=filter(lambda x:x.startswith('--') or x.count(' ')>1,data)
            self.import_text(data)

    def import_words_to_database(self,sentence):
        if len(sentence)<2:
            return
        w=wdb.Word.select(data="")
        if len(w)!=0:
            w=w[0]
            w.set(occurences=w.occurences+1)
        else:
            w=wdb.Word(data="",occurences=1)
        window=[w]
        wnull=w
        i=0
        while i<len(sentence):
            window=self._addtodb(window)
            wl=wdb.Word.select(data=sentence[i])
            if len(wl)==0:
                w=wdb.Word(data=sentence[i],occurences=1)
            else:
                w=wl[0]
                w.set(occurences=w.occurences+1)
            window+=[w]
            i+=1
        window=self._addtodb(window)
        window+=[wnull]
        window=self._addtodb(window)
        return

    def _addtodb(self,window):
        if len(window)<4:
            return window
        elif len(window)>4:
            raise IndexError(str(window)+" has more than 4 elements")
        else:
            l=wdb.Quadruplet.select(w0=window[0],w1=window[1],w2=window[2],w3=window[3])
            if len(l)==0:
                quad=wdb.Quadruplet(w0=window[0],w1=window[1],w2=window[2],w3=window[3],occurences=1)
            else:
                quad=l[0]
                quad.set(occurences=quad.occurences+1)
            return window[1:]

    def import_text(self, text):
        sent_tokenizer=nltk.data.load('tokenizers/punkt/french.pickle')
        sentences=map(lambda x:sent_tokenizer.tokenize(x),text)
        for par in sentences:
            token_sents=map(self.tokenize,par)
            map(self.import_words_to_database,token_sents)

    def tokenize(self, sent):
        char_list="""'"«»:"""
        prepared_sent=sent
        for char in char_list:
            prepared_sent=prepared_sent.replace(char,char+" ")
        prepared_sent.replace(".","")
        return prepared_sent.split(" ")
        
