
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

# Create a list to store the new data
new_data = []

# Iterate through the input data
for row in data:
    product_id = row['product_id']
    try:
        # Converting string to list format, selecting only single items
        ingredients = ast.literal_eval(row['ingredients'])
        assert len(ingredients) == 1
        # Split the ingredients by commas
        ingredient_list = [x.strip(' ').strip('.') for x in ingredients[0].split(', ')]
    except:
        ingredient_list = []
    
    # Create a new row for each ingredient
    for ingredient in ingredient_list:
        new_row = {'product-id': product_id, 'ingredient': ingredient}
        new_data.append(new_row)

# Open the output CSV file and write the new data
with open(parent_path / 'data' / 'product_ingredients.csv', 'w', newline='') as output_file:
    fieldnames = ['product-id', 'ingredient']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_data)

print("Data processing complete!")
# %%
# Highlights?
