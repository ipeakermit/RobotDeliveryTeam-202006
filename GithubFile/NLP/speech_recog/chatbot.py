#import necessary libraries
import io
import random
import string # to process standard python strings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from pocketsphinx import LiveSpeech

nltk.download('popular', quiet=True) # for downloading packages
# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
#Reading in the corpus
with open('chatbot-corpus.txt','r') as fin:
    raw = fin.read().lower()

#Tokenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Keyword Matching
#Do greetings via wordnet
#def Check_wordnet(word):
#    for synonym in wordnet.synsets(word):
#        for lemma in synonym.lemmas():
            
        

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    return_array = []
    for synonym in wordnet.synsets(sentence):
        for lemma in synonym.lemmas():
            return_array.append(lemma.name())
    #return a random string
    return random.choice(return_array)

def baxter_commands(user_response): 
    basic_commands_array = ['forward', 'stop', 'slow', 'spin', 'turn', 'execute']
    commands = user_response.split(" ")
    run_cmd = '*rospy cmd*'
    run_flag = False
    print(commands)
    for i in commands:
        if run_flag == False:
            if user_response not in basic_commands_array:
                return False
            if ('forward' == i):
                print('moving forward....')
                ##insert rospy command here
            if ('stop' == i):
                print('stopping.......')
                ##insert rospy command here
            if ('slow' == i):
                print('slowing down.....')
                ##insert rospy command here
            if ('spin' == i):
                print("spinning........")
                ##insert rospy command here
            if ('turn' == i):
                print("turning.....")
                ##insert rospy command here
            if ('execute' == i):
                run_flag = True
        else:
            if i not in basic_commands_array:
                run_cmd = run_cmd+" "+i
            else:
                print("execute the rospy command: "+run_cmd)
                ##insert rospy command here




# Generating response
def Use_Corpus(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

#implement script controls. e.g: rosie execute script move
print("Rosie: If you want to exit, say Bye!")
for phrase in LiveSpeech():
    print('you said:')
    print(phrase)
    
    user_response = str(phrase)
    user_response = user_response.lower()

    #Insert Baxter bot commands#
    if baxter_commands(user_response) == False:
        ##Conversational
        if(user_response!='bye'):
            analyse = wordnet.synsets(user_response)
            if isinstance(analyse,list) == True and not analyse == []:
                definition = analyse[0].definition()
                print(definition)
                if ('greeting' in definition):
                    print("Rosie: "+greeting(user_response))
            else:
                print("Rosie:")
                print(Use_Corpus(user_response))
                sent_tokens.remove(user_response)
        else:
            print("Rosie: Bye! take care..")  
            break

