
from nltk.tokenize import  sent_tokenize, word_tokenize
import nltk
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer,PorterStemmer,LancasterStemmer,SnowballStemmer
from collections import OrderedDict


def generatekeywords(filepath2):
    # Taking in the file content...........
    f=open(filepath2,"r")
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
    stop_words=set(stopwords.words("english"))
    filtered_word_list=[]
    for i in tagged_word_list:
        if i[0] not in stop_words:
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


    return (final_processed_word_list)





def semanticsimilarity(a,b):
    a,b=a.lower(),b.lower() #converting them into lowercase

    l1=wordnet.synsets(a) #printing synsets of a
    # print(l1) 
    l2=wordnet.synsets(b) #printing synsets of b
    # print(l2) 

    if(len(l1)==0 or len(l2)==0):
        return (0)
    similarity=-1

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


def mapp_it(s,t1):
      
      for i in range(len(t1)):
            t1[i]=t1[i].lower()

      s=s.lower()
      sent=sent_tokenize(s)
      word=word_tokenize(s)
      tag_word=nltk.pos_tag(word)

      tag_t1=nltk.pos_tag(t1)

      noun=[]
      extra_noun=[]
      adj=[]

      #break sentence
      # UH for intersection
      # IN preposition
      #print(sent)
      new_sent=[]
      breaker=[]
      for i in sent:
            tokenize_now=word_tokenize(i)
            pos=nltk.pos_tag(tokenize_now)
            #print(tokenize_now)
            prev=0
            #print(pos)
            for j in range(len(pos)):
                  #print(tokenize_now[j])
                  if pos[j][1]=="UH" or pos[j][1]=="IN" or pos[j][1]=="CC" or  tokenize_now[j]=="?" or tokenize_now[j]=="." or tokenize_now[j]=="," or pos[j][1]=="LS":
                        #print(j)
                        new_sent.append(pos[prev:j:])
                        #print(tokenize_now[prev:j:])
                        breaker.append(pos[j])
                        prev=j+1
            #print(pos)

      #print (new_sent)
      #print()
      #print(breaker)
      #print(new_sent[6])
      #map to main noun
      mapp=[]
      re=0
      for j in range(len(new_sent)):
            re=0
            for i in range(len(new_sent[j])):
                  #print (new_sent[j][i][0])
                  #if j!=0 and breaker[j-1][0]==".":
                        #print(j,len(new_sent[j]))
                     #   re=0
                  if re==0:
                        #print (new_sent[j][i][0])
                        if new_sent[j][i][0] in t1 :
                              re=1
                              mapp.append([new_sent[j][i]])
                              #print(new_sent[j][i])
                        #print (1,len(mapp))
                  elif re==1 and new_sent[j][i][0] in t1:
                        #print (new_sent[j][i])
                        mapp[len(mapp)-1].append(new_sent[j][i])



##      for i in mapp:
##            print (i)
##      print()


      # filter the map
      rem=[]
      las=0
      for i in range(len(mapp)):
          pres=0
          if len(mapp[i])!=1:
              las=i
              for j in mapp[i]:
                  if j[1]=="NN" or j[1]=="NNP":
                      pres=1
          if pres==0:
              for j in mapp[i]:
                  mapp[i-1].append(j)
              rem.append(i)

      for i in range(len(rem)-1,-1,-1):
          #print(rem[i],len(mapp[rem[i]]))
          if len(mapp[rem[i]])!=1:
              for j in range(1,len(mapp[rem[i]])):
                  #print(1)
                  mapp[rem[i]-1].append(mapp[rem[i]][j])
                  
      count=0
      for i in rem:
          z=mapp.pop(i-count)
          count+=1

##      for i in mapp:
##            print (i)
##      print()


      # connect JJ using VBZ
      #print(word[0].find("asd")) -1 when not present
      app=[]
      rem=[]
      for i in range(len(mapp)):
            for j in range(len(mapp[i])):
                  if mapp[i][j][1]=="JJ":
                        nex=1
                        for k in range(len(word)):
                              z=word[k].find(mapp[i][j][0])
                              if z!=-1 and k!=0:
                                    if nltk.pos_tag(word[k-1:k:])[0][1]=="VBZ" or nltk.pos_tag(word[k-1:k:])[0][1]=="VBD" or nltk.pos_tag(word[k-1:k:])[0][1]=="JJ" or nltk.pos_tag(word[k-1:k:])[0][1][:2:]=="RB":
                                          nex=0
                                          break
                        if j==len(mapp[i])-1:
                              nex=0
                        if nex:
                              #print(mapp[i][j+1],mapp[i][j])
                              app.append([mapp[i][j+1],mapp[i][j]])
                              rem.append([i,mapp[i][j]])
                              rem.append([i,mapp[i][j+1]])
                        else:
                               app.append([mapp[i][j-1],mapp[i][j]])
                               rem.append([i,mapp[i][j]])
                               rem.append([i,mapp[i][j-1]])

      for i in rem:
          mapp[i[0]].remove(i[1])

      mapp+=app

      for i in mapp:
          if i==[]:
              mapp.remove([])

##      for i in mapp:
##            print (i)
##      print()

      # mapp with only NN match to previous
      rem=[]
      for i in range(1,len(mapp)):
            pres=0
            for j in mapp[i]:
                  if j[1][:2:]!="NN" :
                        pres=1
                        break
            if pres==0:
                  rem.append(i)
            

      for i in range(len(rem)-1,-1,-1):
          for j in mapp[rem[i]]:
              mapp[rem[i]-1].append(j)
          z=mapp.pop(rem[i])

##      for i in mapp:
##            print (i)
##      print()


      # filter the map
      rem=[]
      las=0
      for i in range(1,len(mapp)):
          pres=0
          if len(mapp[i])!=1:
              las=i
              for j in mapp[i]:
                  if j[1][:2:]=="NN":
                      pres=1
          if pres==0:
              rem.append(i)
                  
      count=0
      for i in rem:  
          z=mapp.pop(i-count)
          count+=1

##      for i in mapp:
##            print (i)
##      print()
          
      # make JJ to JJ or JJ to RB connections
      las=-1
      for i in range(len(tag_word)):
            if tag_word[i][1]=="JJ" or tag_word[i][1][:2:]=="RB":
                  if las==i-1:
                        mapp.append([tag_word[i],tag_word[i-1]])
                  las=i 

      # every following main to be matched to global main noun
      for i in range(1,len(mapp)):
            mapp[0].append(mapp[i][0])

                  
##      for i in mapp:
##            print (i)
##      print()
      
      z1=0
      if "known as" in s:
            z="known"
            z1=1
      elif "called" in word:
            z="called"
            z1=1
      if z1:
            sent=sent_tokenize(s)
            for i in sent:
                  if z in i:
                        t=word_tokenize(i)
                        tag=nltk.pos_tag(t)
                        for x in tag:
                              
                              if x[1][:2:]=="NN":
                                    for j in range(len(mapp)):
                                          for k in range(len(mapp[j])):
                                                #print(mapp[j][k][0],x[0])
                                                if mapp[j][k][0]==x[0]:
                                                      z=mapp[j].pop(k)
                                                      mapp[0].insert(0,x)
                                                       
                                                       
##      for i in mapp:
##            print (i)
##      print()
      
      return mapp


def match(mapp1,mapp2):
      count=0
      neg=0
      for i in mapp1:
            main=i[0][0]
            flg=0
            pres=-5
            for j in mapp2:
                  sim=semanticsimilarity(main,j[0][0])
                  if sim>0.9:
                        flg=1
                        pres=-1
                        for k in range(1,len(i)):
                              c=count
                              pres=0
                              for l in j:
                                    sim_word=semanticsimilarity(l[0],i[k][0])
                                    if sim_word>0.75 and l!=j[0]:
                                          pres=1
                                          count+=1
                                          #print(count,i[k][0],l[0])
                                          x=0
                                          for z in range(len(mapp2)):
                                                if mapp2[z][0][0]==l[0]:
                                                      if mapp2[z][1][0]=="not" or mapp2[z][1][0]=="nor" or mapp2[z][1][0]=="neither" or mapp2[z][1][0]=="never":
                                                            x=1                                          
                                                            #count-=1
                                                            #neg+=1
                                                            break
                                          if x==1:
                                                pres=2
                                          break
                                    elif sim_word==0 :
                                          for z in range(len(mapp2)):
                                                if mapp2[z][0][0]==l[0]:
                                                      if mapp2[z][1][0]=="not" or mapp2[z][1][0]=="nor" or mapp2[z][1][0]=="neither" or mapp2[z][1][0]=="never":
                                                            ant=""
                                                            for s in wordnet.synsets(mapp2[z][0][0]):
                                                                  p=1
                                                                  for le in s.lemmas():
                                                                        if le.antonyms():
                                                                              ant+=le.antonyms()[0].name()
                                                                              p=0
                                                                              break
                                                                  if p==0:
                                                                        break
                                                            
                                                            sim_word=semanticsimilarity(ant,i[k][0])
                                                            if sim_word>0.8:
                                                                  pres=1
                                                                  count+=1
                                                                  break
                              #sprint(c,count)
                              if c==count:
                                    if pres!=2:
                                          pres=0
                                          for y in j:
                                                for z in mapp2:
                                                      if y==z[0]:
                                                            for x in z:
                                                                  if semanticsimilarity(i[k][0],x[0])>0.8:
                                                                        pres=1
                                                                        #print(1)
                                                                        break
                                                            if pres==1:
                                                                  #print(2)
                                                                  break
                                                if pres==1:
                                                      #print(3)
                                                      break
                                          if pres==1:
                                                count+=1
                                          else:
                                                neg+=1
            if flg==0:
                  for y in mapp2:
                        for x in y:
                              if semanticsimilarity(x[0],i[0][0])>0.9:
                                    for k in range(1,len(i)):
                                          pres=0
                                          for l in y:
                                                sim_word=semanticsimilarity(l[0],i[k][0])
                                                if sim_word>0.8 and l!=j[0]:
                                                      x=0
                                                      for z in range(len(mapp2)):
                                                            if mapp2[z][1][0]=="not" or mapp2[z][1][0]=="nor" or mapp2[z][1][0]=="neither" or mapp2[z][1][0]=="never":
                                                                  ant=""
                                                                  x=1
                                                                  break
                                                            elif sim_word==0:
                                                                  for z in range(len(mapp2)):
                                                                        if mapp2[z][0]==l[0]:
                                                                              if mapp2[z][1][0]=="not" or mapp2[z][1][0]=="nor" or mapp2[z][1][0]=="neither" or mapp2[z][1][0]=="never":
                                                                                    ant=""
                                                                                    for s in wordnet.synsets(mapp2[z][0][0]):
                                                                                          p=1
                                                                                          for le in s.lemmas():
                                                                                                if le.antonyms():
                                                                                                      ant=le.lantonyms()[0].name()
                                                                                                      p=0
                                                                                                      break
                                                                                          if p==0:
                                                                                                break
                                                                                    sim_word=semanticsimilarity(ant,i[k][0])
                                                                                    if sim_word>0.8:
                                                                                          pres=1
                                                                                          break
                                                                                    
                                          if pres==1:
                                                count+=1
                                          else:
                                                for y in j:
                                                      for z in mapp2:
                                                            if y==z[0]:
                                                                  for x in z:
                                                                        if semanticsimilarity(i[k][0],x[0])>0.8:
                                                                              pres=1
                                                                              break
                                                                  if pres==1:
                                                                        break
                                                      if pres==1:
                                                            break
                                                if pres==1:
                                                      count+=1
                                                else:
                                                      neg+=1
      #print(count,neg)
      if neg==0 and count==0:
            return 0.0
      return count/(count+neg)


# from model ans
s1="Photosynthesis is a process by which plants and algae, convert sunlight to chemical energy."
x=word_tokenize(s1)
#print(nltk.pos_tag(x))
#print(nltk.pos_tag(['chemical','energy']))
t1=['photosynthesis','process','plants','algae', 'sunlight','chemical', 'energy']
mapp1=mapp_it(s1,t1)
# print(mapp1)
# print (s1)

# student ans
s2="photosynthesis convert, sunlight to mass."
t2=['photosynthesis','mass','sunlight']
#s2="Create a map of the workspace\n using the laser and known position. values. The map should be created as a 20 array with some resolution Keep a count of how many times an obstade at a grid is discovered by the lasers.\n (7.) Extend question o such that every\n grid you count the number of times the obstade is disconered and the number of times the obstace is not discovered by the lasers."
#t2=['16', 'map', 'workspace', 'laser', 'position', 'values', '20', 'array', 'resolution', 'count', 'many', 'times', 'obstade', 'grid', 'lasers', '7', 'question', 'o', 'such', 'number', 'obstace']
mapp2=mapp_it(s2,t2)
# print(mapp2)
# print(s2)
#mapp2=[[('photosynthesis', 'NN'), ('process', 'NN'), ('plants', 'NNS'), ('algae', 'NNS'), ('certain', 'JJ'), ('bacteria', 'NNS'), ('energy', 'NN'), ('sunlight', 'NN'), ('chemical', 'JJ'), ('energy', 'NN')]]

print(match(mapp1,mapp2))

                                                                  
                                                
                                                                        
                                          
                                                      
                                                      
                  
