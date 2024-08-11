
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
# Assuming problem stems from newlines in review_text
# Iterate rows with longest number of cols, then merge two cells that belongs to review_text,
#    until all are merged

TARGET_COLS = 19
REVIEW_TEXT_COL_IDX = 9

df_fixed = df.copy()
while df_fixed.shape[1] > TARGET_COLS:
    problematics = df_fixed.iloc[:, -1].notnull()
    column_names = df_fixed.columns
    #print(df_fixed[problematics])

    df_fixed.loc[problematics, column_names[REVIEW_TEXT_COL_IDX]] += "\n" + df_fixed.loc[problematics, column_names[REVIEW_TEXT_COL_IDX+1]].astype(str).to_numpy()
    df_fixed.loc[problematics, column_names[(REVIEW_TEXT_COL_IDX+1):-1]] = df_fixed.loc[problematics, column_names[(REVIEW_TEXT_COL_IDX+2):]].to_numpy()
    df_fixed = df_fixed.iloc[:, :-1]

df_fixed.to_csv(parent_path / 'data' / 'reviews_0-250_corrected.csv', index=False)

#%%

# Filter the quality of reviews first
# Then sample reviews of each product/ingredient for sentiment scoring???
# -- What number?

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def is_quality_review(text):
    return len(str(text)) >= 10 or any(char.isalnum() for char in str(text))

def get_sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(str(text))
    return sentiment_scores['compound']

df_fixed["is_quality"] = df_fixed["review_text"].apply(is_quality_review)
df_fixed["sentiment"] = df_fixed["review_text"].apply(get_sentiment_score)
# pd.set_option('display.max_colwidth', None)
# df_fixed[["review_text", "is_quality", "sentiment"]]

# %%
