from base64 import encode
import pickle
from textwrap import indent 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.metrics.pairwise import cosine_similarity
import json
import time
import nltk
from nltk.stem.lancaster import LancasterStemmer
# nltk.download('punkt')



tfv = TfidfVectorizer(min_df=1)
label_encode = LE()
stemmer = LancasterStemmer()




def cleanup(sentence):
    sentence = sentence.lower()
    word_tok = nltk.word_tokenize(sentence)
    stemmed_words = [stemmer.stem(w) for w in word_tok]
    return ' '.join(stemmed_words)


model = pickle.load(open('pickles\\model.pkl','rb'))
tfv = pickle.load(open('pickles\\tfidf.pkl','rb'))
le = pickle.load(open('pickles\\le.pkl','rb'))


def load_dataset():
    dataset = pd.read_csv("assets\\final-dataset.csv")
    return dataset



def top_5_similar_qns(cos_sim_array):
    indx = []
    for ind , score in enumerate(cos_sim_array):
        indx.append([score[0][0] , ind])
    indx.sort(reverse=True)
    return indx[:5]





# function to add json for top 5 query
def write_file(new_data, filename ="assets\\questions_top_5.txt"):
        file_data = open(filename,'w',encoding='utf-8')
        for data in new_data :
            file_data.write(f'{data} \n')
        file_data.close()


def get_text(filename ="assets\\questions_top_5.txt"):
    file_data = open(filename,'r')
    queries = []
    index = []
    ind = 1
    for line in file_data:
        if ind%2==0:
            queries.append(line)
        else :
            index.append(line)
        ind +=1
        print(line)
    file_data.close()
    qns = []
    for i in range(5):
        qns.append([index[i] , queries[i]])
    return qns


def query_2nd(query,index):
    query = cleanup(query.strip())
    query_vec = tfv.transform([query])
    pred = model.predict(query_vec)[0]
    intent = le.inverse_transform([pred])
    chatbot_df = load_dataset() 
    question_set = chatbot_df[ chatbot_df['Intent']==intent[0]]
    ans = question_set.iloc[index].Answer
    return ans





def chat_response(query):
    # clean the query
    query = cleanup(query.strip())
    # vectorized the query
    query_vec = tfv.transform([query])
    # predict the intent 
    pred = model.predict(query_vec)[0]
    intent = le.inverse_transform([pred])
    # find the question set based on the intent classified
    chatbot_df = load_dataset() 
    question_set = chatbot_df[ chatbot_df['Intent']==intent[0]]
    # apply cosine similarity to get the top 5 similar match
    cos_sims = []
    for question in question_set['Question']:
        sims = cosine_similarity(tfv.transform([question]), query_vec)
        cos_sims.append(sims)
    # top 5 questions with index and scores
    top_5_match = top_5_similar_qns(cos_sims)
    print(top_5_match)
    top_5_qns = []
    qnsn = []
    for idx in range(5):
        top_5_qns.append(top_5_match[idx][1])
        top_5_qns.append(question_set.iloc[top_5_match[idx][1]].Question)
    top_5_qns.append(intent[0])
    print(top_5_qns)
    write_file(top_5_qns)
    print(get_text())
    time.sleep(2)
    if(top_5_match[0][0]>=0.40):
            max_score_idx = top_5_match[0][1]
            return question_set.iloc[max_score_idx].Answer
    else:
        return "Sorry, I could not understand you question!"




if __name__=='__main__':
    load_dataset()