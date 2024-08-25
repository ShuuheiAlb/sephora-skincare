
#%%
import pathlib
import pandas as pd

# Open the product file
parent_path = Path(__file__).parent
data = pd.read_csv(parent_path / 'data' / 'product_info.csv')
data = data[data["primary_category"] == "Skincare"]
print(data)

#%%
import ast
import re

# Iterate through the input data
df_ingredient = []
for _, row in data.iterrows():
    product_id = row['product_id']
    # Converting string to list format, selecting only single items
    try:
        ingredients = ast.literal_eval(row['ingredients'])
        assert len(ingredients) == 1
        # (soon: Split with comma except 1,2,2-chemical etc, remove percentage)
        # Remove brackets: these are "may contain" sections, *contains
        ingredient_list = re.split(r',\s+', ingredients[0].replace(r"\(.*\)", "").replace(r"\[.*\]", ""))
        ingredient_list = [re.sub(r'[0-9]+\%', "", _).strip('. ') for _ in ingredient_list]
    except:
        ingredient_list = []
    
    # Create a new row for each ingredient
    for i, ingredient in enumerate(ingredient_list):
        new_row = {'product-id': product_id, 'ingredient': ingredient, 'order': i}
        df_ingredient.append(new_row)

#%%
# Now for the highlight
df_highlight = []
for _, row in data.iterrows():
    product_id = row['product_id']
    try:
        highlight_list = ast.literal_eval(row['highlights'])
    except:
        highlight_list = []
    for highlight in highlight_list:
        new_row = {'product-id': product_id, 'highlight': highlight}
        df_highlight.append(new_row)

#%%
# Write the new data
data.to_csv(parent_path / 'data' / "skincare_info.csv", index=False, header=True)
pd.DataFrame(df_ingredient).to_csv(parent_path / 'data' / "skincare_ingredients.csv", index=False, header=True)
pd.DataFrame(df_highlight).to_csv(parent_path / 'data' / "skincare_highlights.csv", index=False, header=True)

print("Data processing complete!")

# %%
