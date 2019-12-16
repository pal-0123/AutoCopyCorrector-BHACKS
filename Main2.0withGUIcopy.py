no_of_questions,no_of_students=0,0 #Creating global variables for no of questions and no of students.......
############################################### MAKING EVERYTHING READY FOR EVALUATION########################################################
import drive_func
import os
#Creating file paths for uploads and downloads
modelimgpath='./MODEL_ANSWER(img)/'
studentimgpath='./STUDENTS_ANSWER(img)/student'
studenttextpath='./STUDENTS_ANSWER(text)/student'
modeltextpath='./MODEL_ANSWER(text)/'
#Creating file paths for uploads and downloads


MainObjectGD=drive_func.gdrive() #Creating Main Object of class drive_func


##################################################FOR ALL MODEL RELATED STUFF#################################################################
def model_things():

    print("Model Answer Executions starts")
    global no_of_questions
    for i in range(no_of_questions):
        idcaught=MainObjectGD.uploadconverted(modelimgpath+'img'+str(i+1)+'.jpg') #Uploading images from MODEL_ANSWER(img) as doc files
        MainObjectGD.download(idcaught,modeltextpath+'q'+str(i+1))# Downloading text files to MODEL_ANSWER(text) for Evaluation.

    print("Model Answer Executed")
##################################################FOR ALL MODEL RELATED STUFF END #################################################################




#############################################FOR ALL STUDENT RELATED STUFF##############################################################
def student_things():
    
    print("Student Answer Execution starts")
    global no_of_questions
    global no_of_students

    for j in range(no_of_students):
        
        if not os.path.exists('./STUDENTS_ANSWER(text)/student'+str(j+1)+'/'):
            os.makedirs('./STUDENTS_ANSWER(text)/student'+str(j+1)+'/')

        for i in range(no_of_questions):
            idcaught=MainObjectGD.uploadconverted(studentimgpath + str(j+1)+'/img'+str(i+1)+'.jpg') #Uploading images from STUDENTS_ANSWER(img) as doc files
            MainObjectGD.download(idcaught,studenttextpath+str(j+1)+'/'+'q'+str(i+1))# Downloading text files to STUDENTS_ANSWER(text) for Evaluation.

    print("Student Answer Executed")
#############################################FOR ALL STUDENT RELATED STUFF END ##############################################################


############################################### EVERYTHING READY FOR EVALUATION NOW ########################################################








######################################################## EVALUATION BEGINS #################################################################


#...............starting with Natural Language processing.................#


import nltk
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer,PorterStemmer,LancasterStemmer,SnowballStemmer
from collections import OrderedDict
import semanticsimilarity
from nltk.tokenize import  sent_tokenize, word_tokenize



simobject=semanticsimilarity.semsim() #creating object of semantic similarity.............



##############################################################GENERATING KEYWORDS#############################################################################

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


    

#####################################################################GENERATING KEYWORDS END #############################################################################

#...............starting with Natural Language processing ENDS.................#






#######################################################################MAPPING FOR FURTHER PROCESSING################################################################
def mapp_it(s,t1):
      
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
      if "known" in word:
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
                                                      mapp[j].remove(x)
                                                      mapp[0].insert(0,x)
                                                       
                                                       
##      for i in mapp:
##            print (i)
##      print()
      
      return mapp
#######################################################################MAPPING FOR FURTHER PROCESSING END ################################################################








##############################################################ACTUAL MATCHING CONSIDERING ALL CASES###################################################################

def match(mapp1,mapp2):
      count=0
      neg=0
      for i in mapp1:
            main=i[0][0]
            flg=0
            pres=-5
            for j in mapp2:
                  sim=simobject.givesim(main,j[0][0])
                  if sim>0.9:
                        flg=1
                        pres=-1
                        c=count
                        for k in range(1,len(i)):
                              pres=0
                              for l in j:
                                    sim_word=simobject.givesim(l[0],i[k][0])
                                    if sim_word>0.8 and l!=j[0]:
                                          pres=1
                                          count+=1
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
                                                            
                                                            sim_word=simobject.givesim(ant,i[k][0])
                                                            if sim_word>0.8:
                                                                  pres=1
                                                                  count+=1
                                                                  break
                              #print(c,count)
                              if c==count:
                                    if pres!=2:
                                          pres=0
                                          for y in j:
                                                for z in mapp2:
                                                      if y==z[0]:
                                                            for x in z:
                                                                  if simobject.givesim(i[k][0],x[0])>0.8:
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
                              if simobject.givesim(x[0],i[0][0])>0.9:
                                    for k in range(1,len(i)):
                                          pres=0
                                          for l in y:
                                                sim_word=simobject.givesim(l[0],i[k][0])
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
                                                                                    sim_word=simobject.givesim(ant,i[k][0])
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
                                                                        if simobject.givesim(i[k][0],x[0])>0.8:
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
##############################################################ACTUAL MATCHING CONSIDERING ALL CASES END ###################################################################



######################################################## EVALUATION BEGINS END #################################################################







############################################################ UTILIZING THE ABOVE FUNCTIONS AND GENERATING SCORE########################################################################


def generatescore():

    global no_of_questions
    global no_of_students
    print(no_of_questions)
    print(no_of_students)
    for i in range(no_of_questions):

        filepath=modeltextpath+'q'+str(i+1)
        model_keywords=generatekeywords(filepath)
        f=open(filepath,"r")
        model_content=f.read()
        f.close()
        index=0
        for k in range(len(model_content)):
            if(model_content[k].isalpha()):
                index=k
                break
        model_content=model_content[index:]

        for j in range(no_of_students):
            filepath=studenttextpath+str(j+1)+'/'+'q'+str(i+1)
            student_keywords=generatekeywords(filepath)
            f=open(filepath,"r")
            student_content=f.read()
            f.close()
            
            index=0
            for l in range(len(student_content)):
                index2=0
                if(student_content[l].isalpha()):
                    index2=l
                    break
            student_content=student_content[index2:] 
               
            score=match(mapp_it(model_content,model_keywords),mapp_it(student_content,student_keywords))
            
            #Generating a score.txt file for final results
            score=round(score*100,2)
            if(j==0 and i==0):
                with open("score.txt",'w') as f:
                   
                    f.write(str(score)+"% ")
            else:
                with open("score.txt",'a') as f:
                    f.write(str(score)+"% ")
            print(score)
        
        with open("score.txt",'a') as f:
                    f.write("\n")
        





############################################################ UTILIZING THE ABOVE FUNCTIONS END AND GENERATING SCORE ########################################################################













################################################################### GUI #######################################################################



from tkinter import *
import tkinter.messagebox
import webbrowser
myApp=Tk()
myApp.title("AutoCheckMyAnswer")

#*************Instruction Tab*************
instruction_frame=Frame(myApp)
instruction_frame.pack(side=TOP,fill=X,expand=1)
def showInstructions():
    webbrowser.open("instructions.txt")
instr_button=Button(instruction_frame,text="Instructions",width=15,height=10,fg="purple",bg="yellow",command=showInstructions)
instr_button.pack(side=LEFT,padx=10,pady=10,expand=True)

#*****************************************
#***********Secondary Window 1**************
def window_for_no_of_questions():
    #new window to enter no. of questions
    global no_of_questions
    # global students
    
    def confirm():                     #confirm button for upload
        global no_of_questions
        
        question = entry_field.get()
        no_of_questions=int(question)
        model_things()   #students stores no. of students
        # print(no_of_questions)
        def destroy_popups():
            popup.destroy()
            master.destroy()
        
        popup = Tk()
        popup.wm_title("!")
        
        B1 = Button(popup, text="Done !!",bg="green",fg="yellow", command = destroy_popups)
        B1.pack()
        popup.mainloop()
    
    #menu to enter no. of questions
    master=Tk()
    label=Label(master,text="Enter No.of Questions",fg="purple")
    label.grid(row=0,column=0,sticky=N+E+S+W)

    entry_field=Entry(master)
    entry_field.grid(row=0,column=1,sticky=N+E+S+W)

    entry_field.focus_set()
    
    entry_button = Button(master,text="Confirm",bg="green",fg="yellow",command=confirm)
    entry_button.grid(row=1,column=1,sticky=N+E+S+W)
    
    wait_label=Label(master,text="Please wait for 5-6 minutes a popup will appear after processing is finished")
    wait_label.grid(row=2,column=0,columnspan=2,sticky=N+E+S+W)

    master.mainloop()

#***********************************************************

def window_for_evaluate():

    global no_of_questions
    global no_of_students
    # print(no_of_questions)
    # print(no_of_students)
    def confirm():                  
        global no_of_questions
        global no_of_students
        generatescore()
        def destroy_popups():
            popup.destroy()
            master.destroy()
        
        popup = Tk()
        popup.wm_title("!")
        
        B1 = Button(popup, text="Done !!",bg="green",fg="yellow", command = destroy_popups)
        B1.pack()
        popup.mainloop()

    master=Tk()
    entry_button = Button(master,text="Generate Students Score",bg="green",fg="yellow",command=confirm)
    entry_button.grid(row=0,column=0,columnspan=2,sticky=N+E+S+W)
    
    wait_label=Label(master,text="Please wait for 5-6 minutes a popup will appear after Evaluation is finished")
    wait_label.grid(row=1,column=0,columnspan=2,sticky=N+E+S+W)

    master.mainloop()

#***********Secondary Window 2******************************
def window_for_no_of_students():
    #new window to enter no. of students
    global no_of_questions
    global no_of_students
    
    def confirm():                     #confirm button for upload
        student = entry1_field.get()   #students stores no. of students
        # print(students)
        global no_of_questions
        global no_of_students
        no_of_students=int(student)
    
        # print(nstud)
        student_things()
        # print(type(nstud),nstud+3)
        def destroy_popups():
            popup1.destroy()
            master1.destroy()
        
        popup1 = Tk()
        popup1.wm_title("!")
        
        B2 = Button(popup1, text="Done !!", bg="green",fg="yellow",command = destroy_popups)
        B2.pack()
        popup1.mainloop()
    
    #menu to enter no. of questions
    master1=Tk()
    label1=Label(master1,text="Enter No.of Students",fg="purple")
    label1.grid(row=0,column=0,sticky=N+E+S+W)

    entry1_field=Entry(master1)
    entry1_field.grid(row=0,column=1,sticky=N+E+S+W)

    entry1_field.focus_set()
    
    entry1_button = Button(master1,text="Confirm",bg="green",fg="yellow",command=confirm)
    entry1_button.grid(row=1,column=1,sticky=N+E+S+W)
    
    wait_label1=Label(master1,text="Please wait for 5-6 minutes a popup will appear after processing is finished")
    wait_label1.grid(row=2,column=0,columnspan=2,sticky=N+E+S+W)

    master1.mainloop()

#***********************************************************

firstFrame=Frame(myApp)
firstFrame.pack(fill=BOTH,expand=1)

secondFrame=Frame(myApp)
secondFrame.pack(fill=BOTH,expand=1)

for x in range(2):
    Grid.columnconfigure(firstFrame, x, weight=1)

for y in range(2):
    Grid.rowconfigure(firstFrame, y, weight=1)

for x in range(2):
    Grid.columnconfigure(secondFrame, x, weight=1)

for y in range(2):
    Grid.rowconfigure(secondFrame, y, weight=1)

button1=Button(firstFrame,text="Model Answers",width=15,height=10,fg="purple",bg="yellow",command=window_for_no_of_questions)
button1.grid(row=0,column=0,sticky=N+E+S+W)

button2=Button(firstFrame,text="Students' Answers",width=15,height=10,fg="purple",bg="yellow",command=window_for_no_of_students)
button2.grid(row=0,column=1,sticky=N+E+S+W)

button3=Button(secondFrame,text="Evaluate",width=15,height=10,fg="purple",bg="yellow",command=window_for_evaluate)
button3.grid(row=1,column=0,sticky=N+E+S+W)

button4=Button(secondFrame,text="Results",width=15,height=10,fg="purple",bg="yellow",command=window_for_no_of_questions)
button4.grid(row=1,column=1,sticky=N+E+S+W)
myApp.mainloop()


################################################################### GUI END #######################################################################



############################################################ UTILIZING THE ABOVE FUNCTIONS AND GENERATING SCORE########################################################################




############################################################ UTILIZING THE ABOVE FUNCTIONS END AND GENERATING SCORE ########################################################################









