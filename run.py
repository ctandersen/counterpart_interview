from rater_example.rater_example import rater 


json_input = {"Asset Size": 1200000, 
              "Limit": 5000000, 
              "Retention": 1000000, 
              "Industry": "Hazard Group 2"}

result = rater.execute(json_input)
print(result)

# marginal_rate = (1.986 - 1.820)/1000000
# new_limit_rate = 1.986 + marginal_rate * 1000000 * 0.9
# print(new_limit_rate)