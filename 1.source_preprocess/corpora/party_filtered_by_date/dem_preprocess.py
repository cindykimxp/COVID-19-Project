import pandas as pd
import random, csv
#----------------------------------------------------------------------------------------
# make corpora, develop (10%), train (80%), test (10%)
COVID_data = pd.read_csv('COVID_data.csv')
COVID_data=COVID_data.sort_values(by='date')

dem_COVID_data = COVID_data[COVID_data['party']!="R"]
rep_COVID_data = COVID_data[COVID_data['party']=="R"]

# selected data from the scraped tweets
tweets = dem_COVID_data['tweet_cleaned'].tolist()
dates = dem_COVID_data['date'].tolist()
party = dem_COVID_data['party'].tolist()
state = dem_COVID_data['state'].tolist()
username = dem_COVID_data['username'].tolist()

#----------------------------------------------------------------------------------------
# indice list
def indices_gen():
    indices = []
    for i in range(len(rep_COVID_data)):
        indices.append(i)
    return indices
#----------------------------------------------------------------------------------------
# actual tokenization into word & POS tag using NLTK word_tokenize function
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def tokenizer(type,indices):
    count = 0
    file = open("dem_{}.txt".format(type),"w")
    
    # 80% train, 10% dev and 10% test.
    if type == 'test':
        indices = indices[:len(indices)//10]
    elif type == 'dev':
        indices = indices[len(indices)//10:2*len(indices)//10]
    elif type == 'train':
        indices = indices[2*len(indices)//10:]

    for i in indices: 
        file.write('C.{} I.{} P.{} S.{} U.{} {}\n'.format(count,i,party[i],state[i],username[i],dates[i])) 
        words = word_tokenize(tweets[i])
        for j in pos_tag(words):
            file.write('{}\t{}\n'.format(j[0],j[1])) 
        count+=1
        file.write('\n')
#     print(count)

#----------------------------------------------------------------------------------------
# clean data using stopwords & either stem/lemmatize the words using NLTK tools

import nltk, re
nltk.download('stopwords')
from nltk.corpus import stopwords

#stemming 
from nltk.stem.snowball import SnowballStemmer
englishStemmer=SnowballStemmer("english")

#lemmatizing
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer 
wordNet_lemmatizer = WordNetLemmatizer() 

# generate a stopword list, that combines NLTK's pre-existing list & closed_class_stop_words from stop_list.py
# further includes negation words: n't, not, no, cannot

def stopwords_combiner():
    closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','i','we','us','much','and/or','p.m.','p.m','pm','a.m.','p.m','am'
                           ]
    stopwords_list = stopwords.words("english")
    stopwords_list+=["'d","'re","'ve","'ll","'d","'s","'m",'\n','\t']
    
    for cc_sw in closed_class_stop_words:
        if cc_sw not in stopwords_list:
            stopwords_list.append(cc_sw)

    negation = ['no','not','cannot']

    for n in negation: 
        stopwords_list.remove(n)

    for sw in stopwords_list:
        if "n't" in sw:
            stopwords_list.remove(sw)
    return stopwords_list


stopwords_list = stopwords_combiner()
punctuation = "@#$%^&*)(_-—+=}{|\/><~?:!.,;’''’’\"``"
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\u2600-\u26FF\u2700-\u27BF"
                           "]+", flags=re.UNICODE)



# simply pos tag to simpler terms for wordNet_lemmatizer
def pos_tagger(nltk_tag): 
    if nltk_tag.startswith('J'): 
        return 'a' 
    elif nltk_tag.startswith('V'): 
        return 'v'
    elif nltk_tag.startswith('N'): 
        return 'n'
    elif nltk_tag.startswith('R'): 
        return 'r' 
    else:           
        return None
    
#lemmatize
def lemmatizer(word,nltk_tag):
    tag = pos_tagger(nltk_tag)
    if tag != None:
        lemma = wordNet_lemmatizer.lemmatize(word, tag)
    else:
        lemma = word
    return lemma
# either stem or lemmatize corpora
def root_finder(type,root_type):
    file = open('dem_{}.txt'.format(type))
    lines = file.readlines()
    file.close()
    
    output_file = open("dem_{}_{}.txt".format(type,root_type),"w")

    start = True
    for item in lines:
        root = ''
        if (item == '\n'):
            start = True
        if start:
            output_file.write('{}\n'.format(item))
#             print(item)
            start = False
        else:
            items = item.split()
            raw_word = items[0]
            word = (emoji_pattern.sub(r'', raw_word))

            if len(word)>0:
                if word[0].isalpha() or word == '2019-nCoV':
                    if '––' in word:
                        words = word.split('––')
                        for w in words:
                            if w not in punctuation and w.lower() not in stopwords_list:
                                if (root_type == 'stem'):
                                    root = englishStemmer.stem(w)
                                elif (root_type == 'lemma'):
                                    root = lemmatizer(w,items[1])
                    else:
                        if word not in punctuation and word.lower() not in stopwords_list:
                            if (root_type == 'stem'):
                                root = englishStemmer.stem(word)
                            elif (root_type == 'lemma'):
                                root = lemmatizer(word,items[1])
                    if (len(root)>0):
                        output_file.write('{}\t{}\n'.format(root,items[1])) 
#                         print(root,items[1])
        if (item == '\n'):
            start = True

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
# call functions

# shuffle indices & save them 
indices = indices_gen()

# tokenize & turn tweets into corpora 
tokenizer('full',indices)
tokenizer('dev',indices)
tokenizer('train',indices)
tokenizer('test',indices)
    
# clean the corpora by stemming & lemmatizing them
root_finder('dev','stem')
root_finder('dev','lemma')
root_finder('train','stem')
root_finder('train','lemma')
root_finder('test','stem')
root_finder('test','lemma')
root_finder('full','stem')
root_finder('full','lemma')
