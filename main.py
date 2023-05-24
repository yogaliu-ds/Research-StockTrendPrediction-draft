








# Save to csv, just in case
news_data_final.to_csv('/content/drive/MyDrive/Research/sentiment_score/sum_sentiment_score.csv', index=False)
# check csv
x = pd.read_csv('/content/drive/MyDrive/Research/sentiment_score/sum_sentiment_score.csv')
print(x)