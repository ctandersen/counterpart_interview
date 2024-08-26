# D&O Premium rating function
This package contains a single function that calculate a premium update using policy rating data from a json file

The json data must contain the following information:
"Assets", "Limit", "Retention" and "Hazard Group"

## How to use
_After installing the package use the following import:_ <br>

**from rater_example import rater**

_Then use the following commands_
**json_input = {"Asset Size": 1200000, 
              "Limit": 5000000, 
              "Retention": 1000000, 
              "Industry": "Hazard Group 2"}

result = rater.execute(json_input)**