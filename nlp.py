import numpy as np
import pandas as pd

def sentiment_analysis(agg_df, word_sentiment_split = 0.5):

    # Get neutral sentiment value, flip negative sentiment value:
    agg_df.loc['Neutral', 'Sentiment'] = agg_df.at['Neutral', 'Sentiment Type'] * (1 / sum(agg_df['Sentiment Type']))
    agg_df.loc['Negative', 'Sentiment'] = abs(agg_df.at['Negative', 'Sentiment'])

    # Initialise sentiment types
    positive_words, positive_sentiment = agg_df.at['Positive', 'Sentiment Type'], agg_df.at['Positive', 'Sentiment']
    negative_words,negative_sentiment =  agg_df.at['Negative', 'Sentiment Type'], agg_df.at['Negative', 'Sentiment']
    neutral_words, neutral_sentiment =  agg_df.at['Neutral', 'Sentiment Type'], agg_df.at['Neutral', 'Sentiment']
    
    # Initialise classification weightage
    total_words = positive_words + neutral_words + negative_words

    weighted_positive_words = positive_words / total_words
    weighted_neutral_words = neutral_words / total_words
    weighted_negative_words = negative_words / total_words

    # Initialise sentiment weightage
    total_sentiment = positive_sentiment + neutral_sentiment + negative_sentiment

    weighted_positive_sentiment = positive_sentiment / total_sentiment
    weighted_neutral_sentiment = neutral_sentiment / total_sentiment
    weighted_negative_sentiment = negative_sentiment / total_sentiment

    # Create final weightage for each sentiment:
    positive_final = weighted_positive_words * word_sentiment_split + weighted_positive_sentiment * (1 - word_sentiment_split)
    neutral_final =  weighted_neutral_words * word_sentiment_split + weighted_neutral_sentiment * (1 - word_sentiment_split)
    negative_final = weighted_negative_words * word_sentiment_split + weighted_negative_sentiment * (1 - word_sentiment_split)

    final_dict = {'😊 Positive': positive_final,
                  '😐 Neutral': neutral_final, 
                  '😠 Negative': negative_final}

    return pd.Series(data = final_dict)