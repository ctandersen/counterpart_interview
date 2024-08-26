# D&O Premium rating function
This package contains a single function that calculate a premium update using policy rating data from a json file

The json data must contain the following information:
"Asset Size", "Limit", "Retention" and "Industry"

## How to use
After installing the package use the following import: <br>

**from rater_example import rater**

Then use the following commands
**json_input = {"Asset Size": 1200000, 
              "Limit": 5000000, 
              "Retention": 1000000, 
              "Industry": "Hazard Group 2"}**

**result = rater.execute(json_input)**