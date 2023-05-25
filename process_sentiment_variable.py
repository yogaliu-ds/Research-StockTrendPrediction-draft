import pandas as pd
from sentiment_variable import datatype_process, title_classifier, content_classifier, summation_short_term, summation_mid_term, summation_long_term, final_adjustment

stock_id = 'MSFT'
news_data_location = 'data/microsoft_article_business.csv'

df = pd.read_csv(news_data_location)

df = datatype_process(df)
# df = title_classifier(df)
df = content_classifier(df)
# df = summation_short_term(df)
# df = summation_mid_term(df)
# df = summation_long_term(df)

print(df)


# # Save to csv, will use in the next py
# df.to_csv('data/processed_sentiment_variable.csv', index=False)
# # check csv
# x = pd.read_csv('data/processed_sentiment_variable.csv')
# print(x)



