import documentmodel,worddatabase
import sqlobject
import math

class WordModel(object):
    """Defines the model for words (gives probability
    of each word given previous words and context)
    """
    def __init__(self,documents):
        """Initialize an new Word model.
        Only one WordModel should be present at any given time,
        as initializing a new WordModel starts a complete
        database reconstruction.
        """
        self.words={}
        self.documentmodel=documentmodel.DocumentModel()
        
        self._restart_database()
        self._populate_database(documents)
        
    def _string_to_word(self,txtstring):
        """Given a word (txtstring), returns the associated
        database object. Create it if necessary.
        """
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
        """Destroys current database if it exists;
        Create tables.
        """
        try:
            models.Quadruplet.dropTable()
            models.Triplet.dropTable()
            models.Duplet.dropTable()
            models.Word.dropTable()
            models.WordTopic.dropTable()
            models.Topic.dropTable()

        models.Quadruplet.createTable()
        models.Triplet.createTable()
        models.Duplet.createTable()
        models.Word.createTable()
        models.WordTopic.createTable()
        models.Topic.createTable()


    def _populate_database(self,documents):
        """Populates an empty database with training data.
        """
        # Transform a document in a list of words
        tokenized_documents=map(self.tokenize,documents)
        for doc in tokenized_documents:
            self._add_document_to_database(map(self._string_to_word,doc))

        # Compute LDA on the documents
        # Use the log of the number of document as a rule of thumb for the
        # number of topics (sqrt can be another heuristic)
        beta = self.documentmodel.compute_lda(tokenized_documents,ceil(math.log(len(tokenized_documents))))

        
        self._add_word_occurences(self.documentmodel.dictionnary,worddicts)
        
        self._add_categories_to_databases(beta,self.documentmodel.dictionnary)

    def _add_word_occurences(self,wordlist,worddicts):
        """Adds the nomber of occurence of each word in
        wordlist, according to worddicts, in the database
        """
        import copy
        # Merge word counts across documents
        globaldict=copy.deepcopy(worddicts[0])
        glen=len(globaldict)
        for i in range(1,len(worddicts)):
            for j in range(glen):
                globaldict[j]+=worddicts[i][j]

        # Add these consolidated counts to database
        for i in range(glen):
            word=self._string_to_word(wordlist[i])
            word.occurences=globaldict[i]

    def _add_categories_to_databases(self,beta,vocabulary):
        """Adds probability of each word given a topic to the database
        """
        topics=[models.Topic(topicid=i) for i in range(len(beta[0]))]

        for i in xrange(len(vocabulary)):
            for j in range(len(topics)):
                wordtopic=models.WordTopic(probability=beta[i][j],topic=topics[j],word=self._string_to_word(vocabulary[i]))           

    def tokenize(self,document):
        """Splits a document (string) in a list of words/tokens.
        """
        from nltk.tokenize import *
        tokenizer=RegexpTokenizer('\w+')
        wordlist=tokenizer.tokenize(document)
        return map(str.lower,wordlist)


    def _add_document_to_database(self,wordlist):
        """Adds quadruplets, triplets and duplets found in
        a document represented by wordlist in the database.
        """
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

