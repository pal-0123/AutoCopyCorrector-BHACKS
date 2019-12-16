import nltk
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer,PorterStemmer,LancasterStemmer,SnowballStemmer
from collections import OrderedDict

class semsim:
   
    def givesim(self,a,b):
        a,b=a.lower(),b.lower() #converting them into lowercase

        l1=wordnet.synsets(a) #printing synsets of a
        # print(l1) 
        l2=wordnet.synsets(b) #printing synsets of b
        # print(l2) 

        if(len(l1)==0 or len(l2)==0):
            return (0)
        

        synonymsofl1=[]
        antonymsofl2=[]

        # Synonnyms of l1............
        for i in l1:
            for l in i.lemmas():
                synonymsofl1.append(l.name())
        # Synonnyms of l1............


        # Antonyms of l2...............
        for i in l2:
            for l in i.lemmas():
                if(l.antonyms()):
                    antonymsofl2.append(l.antonyms()[0].name())
        # Antonyms of l2...............


        for i in synonymsofl1:
            for j in antonymsofl2:
                if(i==j):
                    return (0) # If exactly opposite return similarity as zero.
            
                    
        
        max1similarity=-1
        for i in l1:
            for j in l2:
                if (i.wup_similarity(j)==None):
                    continue
                if(max1similarity<i.wup_similarity(j)):
                    max1similarity=i.wup_similarity(j)
        max2similarity=-1
        for i in l2:
            for j in l1:
                if (i.wup_similarity(j)==None):
                    continue
                if(max2similarity<i.wup_similarity(j)):
                    max2similarity=i.wup_similarity(j)
            
        return (max(max1similarity,max2similarity))
