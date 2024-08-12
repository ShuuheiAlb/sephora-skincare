
#%%
import pandas as pd
import pathlib

# Open the review files
review_paths = ['reviews_0-250.csv', 'reviews_250-500.csv', 'reviews_500-750.csv',
                'reviews_750-1250.csv', 'reviews_1250-end.csv']

parent_path = pathlib.Path(__file__).parent
df = pd.read_csv(parent_path / 'data' / 'reviews_0-250.csv')
print(df)

#%%

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def is_quality_review(text):
    return len(str(text)) >= 10 or any(char.isalnum() for char in str(text))

def get_sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(str(text))
    return sentiment_scores['compound']

# Filter the quality of reviews first, then "rating"!!!
# Then sample the reviews (5-10%) of each product for sentiment scoring???
reviews_by_product = df.groupby("product_id")["review_text"].apply(list)
sampled_reviews = []
for product_id, review_text in reviews_by_product.items():
    sampled_review_ = pd.Series(review_text).sample(frac=0.05, random_state=42)
    sampled_reviews.append(pd.DataFrame({"product_id": product_id, "review_text": sampled_review_.tolist()}))
sampled_reviews = pd.concat(sampled_reviews, ignore_index=True)

sampled_reviews["is_quality"] = sampled_reviews["review_text"].apply(is_quality_review)
sampled_reviews["sentiment"] = sampled_reviews["review_text"].apply(get_sentiment_score)
# pd.set_option('display.max_colwidth', None)
# sampled_reviews[["review_text", "is_quality", "sentiment"]]
sampled_reviews.to_csv(parent_path / 'data' / 'reviews_0-250_sentiment.csv', index=False)

# %%

# Topic modelling

from top2vec import Top2Vec

TOP2VEC_NUM_SAMPLES = 1000
# Select product_id with categories
top2vec_sampled_reviews = df["review_text"].dropna().sample(n=TOP2VEC_NUM_SAMPLES, random_state=42)
docs_bad = top2vec_sampled_reviews.values.tolist()
topic_model = Top2Vec(docs_bad)
topic_words, word_scores, topic_nums = topic_model.get_topics(3)
for topic in topic_nums:
    topic_model.generate_topic_wordcloud(topic)