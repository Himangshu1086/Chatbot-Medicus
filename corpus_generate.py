import pandas as pd
import json

# reading the json file
filename = "Data Preparation\Dataset.json"
with open(filename,'r',encoding='utf-8') as file:
        # load existing data into a dict.
        data = json.load(file)



#Create label data for and represent it in a DataFrame
questions = []
answers = []
intent = []


for key in data.keys():
     for qna in data[key]:
        questions.append(qna[0])
        answers.append(qna[1])
        intent.append(key)

# creating the dataFrame
medical_faq = pd.DataFrame(columns=['Question', 'Answer', 'intent'])


medical_faq['Question'] = pd.Series(questions)
medical_faq['Answer'] = pd.Series(answers)
medical_faq['intent'] = pd.Series(intent)


#save as csv
medical_faq.to_csv("medical-dataset.csv", index=False)