# -*- coding: utf-8 -*-
import math

class DocumentModel(object):
    """Class used to derive a classification model of documents.
    """
    def _create_bags_of_words(self,wordsets):
        # Compute the global vocabulary
        self.dictionnary=list(reduce(set.union,map(set,wordsets)))
        # Compute the count of each word
        self.worddicts=map(lambda x:self.create_worddict(x,dictionnary),wordsets)

    def create_worddicts(wordlist,dictionnary):
        """Given a list of words (wordlist, representing a document),
        returns the number of occurences of each word of a vocabulary
        (dictionnary) in wordlist.
        """
        return dict([(x,wordlist.count(dictionnary[x])) for x in range(0,len(dictionnary))])

    def _write_input_file(self,worddicts):
        """Writes correctly-formatted input file for LDA-C.
        """
        ustrfile=u""
        length=len(worddicts)
        for docu in range(length):
            ustrfile+=str(length)+u" "+str(worddicts[docu])[1:-1]+"\n"
        file=open("documents.txt","w")
        file.write(ustrfile)
        file.close()

    def compute_lda(self,documents,k):
        """Main function of the class;
        Given a list of lists of words (documents) and a number
        of topics (k), computes the LDA and return beta.
        """
        self._create_bags_of_words(documents)
        self._write_input_file(self.worddicts)

        # Compute LDA calling LDA-C
        import subprocess
        #subprocess.call(["lda","est","1",str(k),"settings.txt","documents.txt","random","data"])
        subprocess.call(["lda","est","estimate",str(k),"settings.txt","documents.txt","random","data"])

        # Load beta from file and return it
        beta=[[] for x in range(0,len(self.dictionnary))]
        file=open("data/final.beta")
        for line in file.readlines():
            betai=map(float,line.split())
            for i in range(0,len(self.dictionnary)):
                beta[i].append(betai[i])
            
        file.close()
    
        return beta

    def compute_inference(self,document):
        """Infer topics in the supplied documents
        """
        worddict=self.create_worddict(document,dictionnary)
        self._write_input_file(worddict)
        
        import subprocess
        subprocess.call(["lda","inf","settings.txt","data/final","documents.txt","docestimate"])
        
        file=open("data/final.beta")
        line = file.readline():
        context=map(float,line.split())
        file.close()
        
        return context
