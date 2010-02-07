# -*- coding: utf-8 -*-
import math

class DocumentModel(object):
    def _create_bags_of_words(self,wordsets):
        # prepare documents to compute LDA
        self.dictionnary=list(reduce(set.union,map(set,wordsets)))
        self.worddicts=map(lambda x:self.create_worddict(x,dictionnary),wordsets)

    def create_worddicts(wordlist,dictionnary):
        return dict([(x,wordlist.count(dictionnary[x])) for x in range(0,len(dictionnary))])

    def _write_input_file(self):
        # write input file
        ustrfile=u""
        length=len(self.worddicts)
        for docu in range(length):
            ustrfile+=str(length)+u" "+str(self.worddicts[docu])[1:-1]+"\n"
        file=open("documents.txt","w")
        file.write(ustrfile)
        file.close()

    def compute_lda(self,documents,k):
        self._create_bags_of_words(documents)
        self._write_input_file()

    # compute LDA
        import subprocess
        subprocess.call(["lda","est","1",str(k),"settings.txt","documents.txt","random","data"])

    # load beta
        beta=[[] for x in range(0,len(self.dictionnary))]
        file=open("data/final.beta")
        for line in file.readlines():
            betai=map(float,line.split())
            for i in range(0,len(self.dictionnary)):
                beta[i].append(betai[i])
            
        file.close()
    
        return beta
        # docfeat=[]
        # for i in range(0,len(documents)):
        #     featvector=[0 for x in range(0,k)]
        #     for word in wordsets[i]:
        #         addvects(featvector,beta[list(dictionnary).index(word)])
        #     docfeat.append(featvector)
    
        # return docfeat
