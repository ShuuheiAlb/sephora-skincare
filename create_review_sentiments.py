
#%%
import pandas as pd
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# File paths
review_paths = ['reviews_0-250', 'reviews_250-500', 'reviews_500-750',
                'reviews_750-1250', 'reviews_1250-end']
parent_path = Path(__file__).parent

# Transform functions
def is_quality_review(text):
    return len(str(text)) >= 10 or any(char.isalnum() for char in str(text))

def get_sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(str(text))
    return sentiment_scores['compound']

#%%
for path in review_paths:
    # Open the file if the sentiment file does not exist yet
    file_path = parent_path / 'data' / f'{path}.csv'
    sentiment_file_path = parent_path / 'data' / f'{path}_sentiment.csv'
    if sentiment_file_path.exists():
        continue
    print(f"Starting file {path}")
    df = pd.read_csv(file_path, index_col=0)

    # Sample 5-10% of each product for sentiment scoring + quality
    def sample_kwargs(x):
        return dict(frac=0.05, random_state=42) if len(x) > 200 else dict(n=min(10, len(x)), random_state=42)
    sampled_df = df.groupby("product_id")[["author_id","review_text"]].apply(lambda x: x.sample(**sample_kwargs(x)))
    sampled_df["is_quality"] = sampled_df["review_text"].apply(is_quality_review)
    sampled_df["sentiment"] = sampled_df["review_text"].apply(get_sentiment_score)
    sampled_df_flat = sampled_df.reset_index().drop(columns="review_text", index=1)
    # pd.set_option('display.max_colwidth', None)
    sampled_df_flat.to_csv(parent_path / 'data' / f'{path}_sentiment.csv', index=False)

# %%
