import torch

# 1. Import the classifier
from transformers import pipeline

classifier = pipeline("sentiment-analysis", model='ProsusAI/finbert')

# 2. Transform the 'title' to sentiment score
title_list = news_data['title']

score_list = []

pro
for i in title_list :
  result_list = classifier(i)
  result = result_list[0]
  # I don't know if I can do it this way, but...
  # posive: get positive score
  # negative: get negative score
  # neutralL get 0
  if result['label'] == 'positive':
    score = result['score']
  elif result['label'] == 'negative':
    score = - result['score']
  else:
    score = 0
  # Check
  # print(result['label'])
  # print(score)
  score_list.append(score)
news_data['title_sentiment_score'] = score_list






