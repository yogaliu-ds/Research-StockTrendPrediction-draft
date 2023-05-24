#


# Basic
import pandas as pd

# Others
from datetime import datetime, timedelta
import statistics
from transformers import pipeline


def datatype_process(news_data):
    temp_datetime_string = news_data['datetime']

    # iterate the datetime string to datetime
    temp_datetime_list = []
    for i in temp_datetime_string:
        temp_datetime = datetime.strptime(i, '%b %d, %Y')
        temp_datetime_list.append(temp_datetime)

    news_data['datetime'] = temp_datetime_list

    return news_data

# Let's use the original FinBERT first
# Title classifier


# I don't know if I can put it outside the function
classifier = pipeline("sentiment-analysis", model='ProsusAI/finbert')


def title_classifier(news_data):

    # 2. Transform the 'title' to sentiment score
    title_list = news_data['title']

    score_list = []
    for i in title_list:
        result_list = classifier(i)
        result = result_list[0]
        # I don't know if I can do it this way, but...
        # positive: get positive score
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

# 3. Transform the 'content' to sentiment score
# Need to truncate the content. You should decide how to select the content(512 words) for sentiment analysis.
# The article contents have too much words (1000~10000), so it's impossible to just feed them into the FinBERT.
# You need to decide which part you want.


# Function of splitting the content
def split_article(article, max_length):
    """
    Splits a long article into smaller chunks with a maximum length of `max_length`.
    """
    chunks = []
    words = article.split()
    current_chunk = ''
    for word in words:
        if len(current_chunk.split()) + len(word.split()) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = word
        else:
            current_chunk += ' ' + word
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


# Content classifier
def content_classifier(news_data):
    # setting of the content spliter
    max_length = 300
    # article_chunks = split_article(article, max_length)

    # Transform the 'content' to sentiment score
    temp_list = []
    content_list = news_data['content']
    for complete_text in content_list:
        # 1. split
        # You'll get a list.
        split_content = split_article(complete_text, max_length)

        # 2. FinBert calculate the sentiment score
        temp_score_list = []
        for truncated_content in split_content:
            result_list = classifier(truncated_content)
            result = result_list[0]
            # I don't know if I can do it this way, but...
            # positive: get positive score
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
            temp_score_list.append(score)

        # 3. Averaging
        content_average = statistics.mean(temp_score_list)

        # 4. Throw to temp_list
        temp_list.append(content_average)

    # add to the df
    news_data['content_sentiment_score'] = temp_list


# Short-term sentiment score (main Engineering for summation of scores)

def summation_short_term(news_data):
    # 1. Summation by date
    news_data_temp = news_data.groupby('datetime')['title_sentiment_score'].sum()

    # index to column
    news_data_temp = pd.DataFrame({'datetime': news_data_temp.index, 'title_sentiment_score': news_data_temp})

    # 2. Summing up sentiment score in weekends to Friday

    # Add to Friday

    # x for index
    x = -1
    temp_dict = {}
    temp_friday_df = pd.DataFrame(columns=['datetime', 'title_sentiment_score'])

    while True:
        x += 1
        # Use temp
        if news_data_temp['datetime'][x].weekday() == 5:
            # Get Friday datetime
            new_datetime = news_data_temp['datetime'][x] - timedelta(days=1)
            # convert from timestamp to datetime
            new_datetime = new_datetime.to_pydatetime()
            temp_dict = {'datetime': new_datetime, 'title_sentiment_score': news_data_temp['title_sentiment_score'][x]}

            # Append to temp_friday_df
            temp_friday_df = temp_friday_df.append(temp_dict, ignore_index=True)

        elif news_data_temp['datetime'][x].weekday() == 6:
            # Get Friday datetime
            new_datetime = news_data_temp['datetime'][x] - timedelta(days=2)
            # convert from timestamp to datetime
            new_datetime = new_datetime.to_pydatetime()
            temp_dict = {'datetime': new_datetime, 'title_sentiment_score': news_data_temp['title_sentiment_score'][x]}

            # Append to temp_friday_df
            temp_friday_df = temp_friday_df.append(temp_dict, ignore_index=True)

        else:
            pass
        # Clean up temp_dict for next round
        temp_dict = {}

        # Standard is index
        if x == news_data_temp.shape[0] - 1:
            break

    news_data_concat = pd.concat([news_data_temp, temp_friday_df], axis=0, ignore_index=True)

    return news_data_concat


# (3) Mid-term and Long-term sentiment score
def summation_mid_term(news_data_concat):
    n = 7

    # 1. The average of past 14 days
    temp_score = news_data_concat['title_sentiment_score']
    temp_list = []
    x = -1
    while True:
        x += 1
        midterm_score = temp_score[x:x + n].sum()
        temp_list.append(midterm_score)

        # Transform to index, should be subtracted by 1
        if x + (n - 1) == (news_data_concat.shape[0] - 1):
            break

    # 2. Create a list with zeros
    temp_zeros = []
    for i in range(n - 1):
        temp_zeros.append(0)

    # 3. Combine: to the correct length
    temp_midterm_score = temp_zeros + temp_list

    # 4. Combine into one df
    news_data_concat['title_midterm_sentiment'] = temp_midterm_score


def summation_long_term(news_data_concat):
    n = 14

    # 1. The average of past 14 days
    temp_score = news_data_concat['title_sentiment_score']
    temp_list = []
    x = -1
    while True:
        x += 1
        longterm_score = temp_score[x:x + n].sum()
        temp_list.append(longterm_score)

        # Transform to index, should be subtracted by 1
        if x + (n - 1) == (news_data_concat.shape[0] - 1):
            break

    # 2. Create a list with zeros
    temp_zeros = []
    for i in range(n - 1):
        temp_zeros.append(0)

    # 3. Combine: to the correct length
    temp_longterm_score = temp_zeros + temp_list

    # 4. Combine into one df
    news_data_concat['title_longterm_sentiment'] = temp_longterm_score


# Final adjustment
def final_adjustment(news_data_concat):
    # 1. Delete Saturday and Sunday
    weekend_num = 0

    condition_list = []
    for i in news_data_concat['datetime']:
        if (i.weekday() == 5) or i.weekday() == 6:
            condition_list.append(False)

            # Count weekend days
            weekend_num += 1
        else:
            condition_list.append(True)

    news_data_5days = news_data_concat[condition_list]

    # 2. Eliminate useless dates (those with 0 score)
    news_data_final = news_data_5days[news_data_5days['title_sentiment_score'] != 0]

    # 3. Groupby date
    news_data_final = news_data_final.groupby('datetime').sum()

    # move the index to column 'datetime'
    news_data_final['datetime'] = news_data_final.index
