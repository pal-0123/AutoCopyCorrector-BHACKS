import nltk
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer,PorterStemmer,LancasterStemmer,SnowballStemmer
from collections import OrderedDict
import semanticsimilarity


simobject=semanticsimilarity.semsim()



# Taking in the file content...........
f=open("q1","r")
file_content=f.read()
f.close()
# print(file_content)
# Taking in the file content...........



# Collecting word list........
word_list=nltk.word_tokenize(file_content)
# Collecting word list........


#POS tagging ...............
tagged_word_list=nltk.pos_tag(word_list)
#POS tagging ...............




# Removing stop words..........
stopwords=set(stopwords.words("english"))
filtered_word_list=[]
for i in tagged_word_list:
    if i[0] not in stopwords:
        filtered_word_list.append(i)
# Removing stop words..........



#stemming word........
stemmed_word_list=[]
for i in filtered_word_list:
    if(i[0][len(i[0])-2:]=='ly'):
        k=LancasterStemmer().stem(i[0])
        if (simobject.givesim(k,i[0])>=0.6):
            stemmed_word_list.append(i)
        else :
            stemmed_word_list.append(i)
    elif (i[0][len(i[0])-1]!='e'):
        k=PorterStemmer().stem(i[0])
        if (simobject.givesim(k,i[0])>=0.6):
            stemmed_word_list.append(i)
        else :
            stemmed_word_list.append(i)
    else:
        stemmed_word_list.append(i)
#stemming word........



#Lemmatising word list..............
lemmatizer=WordNetLemmatizer()
lemmatized_word_list=[]
for i in stemmed_word_list:
    k=lemmatizer.lemmatize(i[0])
    if (simobject.givesim(k,i[0])>=0.6):
        lemmatized_word_list.append(i)
    else :
        lemmatized_word_list.append(i)
    
#Lemmatising word list.............


# Finally keeping only essentiall POS.............
final_processed_word_list=[]
for i in tagged_word_list:
    if(i[1]=='CD' or i[1]=='FW' or i[1]=='NN' or i[1]=='NNS' or i[1]=='NNP' or i[1]=='NNPS' or i[1]=='JJ'):

        final_processed_word_list.append(i[0])
# Finally keeping only essentiall POS.............
final_processed_word_list=list(OrderedDict.fromkeys(final_processed_word_list))


print(final_processed_word_list)