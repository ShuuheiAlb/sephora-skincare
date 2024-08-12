
#%%
import csv
import pathlib

# Open the product file
parent_path = pathlib.Path(__file__).parent
with open(parent_path / 'data' / 'product_info.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)
    data = list(reader)

print(data)

#%%
import ast
import re

# Iterate through the input data
df_ingredient = []
for row in data:
    product_id = row['product_id']
    # Converting string to list format, selecting only single items
    try:
        ingredients = ast.literal_eval(row['ingredients'])
        assert len(ingredients) == 1
        ingredient_list = re.split(r',\s+', ingredients[0].replace(r"\(.*\)", "").replace(r"\[.*\]", ""))
        ingredient_list = [_.strip('.') for _ in ingredient_list]
    except:
        ingredient_list = []
    
    # Create a new row for each ingredient
    for ingredient in ingredient_list:
        new_row = {'product-id': product_id, 'ingredient': ingredient}
        df_ingredient.append(new_row)

#%%
# Now for the highlight
df_highlight = []
for row in data:
    product_id = row['product_id']
    try:
        highlight_list = ast.literal_eval(row['highlights'])
    except:
        highlight_list = []
    for highlight in highlight_list:
        new_row = {'product-id': product_id, 'highlight': highlight}
        df_highlight.append(new_row)


#%%
# Open the output CSV file and write the new data
def save_data(new_data, col_name):
    with open(parent_path / 'data' / f'product_{col_name}s.csv', 'w', newline='') as output_file:
        fieldnames = ['product-id', col_name]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_data)
save_data(df_ingredient, "ingredient")
save_data(df_highlight, "highlight")

print("Data processing complete!")

# %%
