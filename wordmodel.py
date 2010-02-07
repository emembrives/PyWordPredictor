import documentmodel,worddatabase
import sqlobject
import math

class WordModel(object):
    def __init__(self):
        self.words={}
        self.documentmodel=documentmodel.DocumentModel()

    def _string_to_word(self,txtstring):
        if self.words.has_key(txtstring):
            return self.words[txtstring]

        word=models.Word.select(models.Word.q.data==txtstring)
        if word.count()==0:
            word=models.Word(data=txtstring,occurences=1)
        else:
            word=word[0]
        words[txtstring]=word
        return word


    def _restart_database(self):
        try:
            models.Quadruplet.dropTable()
            models.Word.dropTable()
            models.Context.dropTable()

        models.Quadruplet.createTable()
        models.Word.createTable()
        models.Context.createTable()

    def _populate_database(self,documents):
        tokenized_documents=map(self.tokenize,documents)
        for doc in tokenized_documents:
            self._add_document_to_database(map(self._string_to_word,doc))

        beta = self.documentmodel.compute_lda(tokenized_documents,ceil(math.log(len(tokenized_documents))))
        self._add_word_occurences(s
        


        self._add_categories_to_databases(beta,self.documentmodel.worddicts)

    def _add_categories_to_databases(self,beta,worddicts):
        
        pass

    def tokenize(self,document):
        from nltk.tokenize import *
        tokenizer=RegexpTokenizer('\w+')
        wordlist=tokenizer.tokenize(document)
        return map(str.lower,wordlist)


    def _add_document_to_database(self,wordlist):
        if len(wordlist)>3:
            for i in range(0,len(wordlist)-3):
                w1,w2,w3,w4=wordlist[i:i+4]
                quad=models.Quadruplet.select(AND(AND(AND(models.Quadruplet.q.w1==w1,models.Quadruplet.q.w2==w2),models.Quadruplet.q.w3==w3),models.Quadruplet.q.w4==w4),clauseTables=['word'])
                if quad.count()==0:
                    quad=models.Quadruplet(w1=w1,w2=w2,w3=w3,w4=w4,occurences=0)
                else:
                    quad=quad[0]
                quad.occurences+=1

        if len(wordlist)>2:
            for i in range(0,len(wordlist)-2):
                w1,w2,w3=wordlist[i:i+3]
                trip=models.Triplet.select(AND(AND(models.Triplet.q.w1==w1,models.Triplet.q.w2==w2),models.Triplet.q.w3==w3),clauseTables=['word'])
                if trip.count()==0:
                    trip=models.triplet(w1=w1,w2=w2,w3=w3,occurences=0)
                else:
                    trip=trip[0]
                trip.occurences+=1

        if len(wordlist)>1:
            for i in range(0,len(wordlist)-1):
                w1,w2=wordlist[i:i+2]
                dup=models.Duplet.select(AND(models.Duplet.q.w1==w1,models.Duplet.q.w2==w2),clauseTables=['word'])
                if dup.count()==0:
                    dup=models.Duplet(w1=w1,w2=w2,occurences=0)
                else:
                    dup=dup[0]
                dup.occurences+=1

