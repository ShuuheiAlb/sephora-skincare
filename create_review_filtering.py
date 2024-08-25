
#%%
import pandas as pd
from pathlib import Path

# File paths
parent_path = Path(__file__).parent
review_paths = ['reviews_0-250', 'reviews_250-500', 'reviews_500-750',
                'reviews_750-1250', 'reviews_1250-end']

# Transform functions
def is_quality_review(text):
    return len(str(text)) >= 10 or any(char.isalnum() for char in str(text))

def get_sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(str(text))
    return sentiment_scores['compound']

#%%
for path in review_paths:
    # Open each file then select skincare in the last one year
    file_path = parent_path / 'data' / f'{path}.csv'
    print(f"Starting file {path}")

    skincare_ids = pd.read_csv(parent_path / 'data' / 'skincare_info.csv')["product_id"].unique()
    df = pd.read_csv(file_path, index_col=0)
    df = df[df["product_id"].isin(skincare_ids)]
    df = df[df["submission_time"] > '2023-01-01']
    df.to_csv(parent_path / 'data' / f'sc_{path}.csv', index=False)

# %%
