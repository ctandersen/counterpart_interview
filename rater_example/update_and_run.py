import json
from rater_example import rater 

with open("rater_example/rating_table.json", mode="r", encoding="utf-8") as read_file:
    rating_table = json.load(read_file)

# Update base rates -6%
base_rate_change = -0.0
for asset_value, base_rate in rating_table["asset_size_base_rate"].items():
    rating_table["asset_size_base_rate"][asset_value] = base_rate * (1 + base_rate_change)

# Update Hazard Group 2 relativity to 1.50
rating_table["industry_factor"]["HG_2"] = 1.25


# Post premium update
json_input = {"Asset Size": 1200000, 
              "Limit": 5000000, 
              "Retention": 1000000, 
              "Industry": "Hazard Group 2"}

result = rater.execute(json_input, rating_table)
print(result)