    
class PolicyApplication:
    def __init__(self, asset_size, limit, retention, industry):
        self.asset_size = asset_size
        self.limit = limit
        self.retention = retention
        self.industry = industry
        
    '''Create a tranformation from policy info to rating table variable 
    for Hazard Group, default to HG, could return error value as well
    '''
    @property
    def hazard_group(self):
        match self.industry:
            case "Hazard Group 1":
                return "HG_1"
            case "Hazard Group 2":
                return "HG_2"
            case "Hazard Group 3":
                return "HG_3"
            case _:
                return "HG_1"
            
def linear_interpolate(dictionary, target_key):
    '''
    Linear interpolates a target value amoungst a dictionary with intermediate key, value pairs
    '''

    # Convert the keys to integers for ability to properly sort keys
    dictionary = {float(k):v for k,v in dictionary.items()}         
    
    # Sort the dictionary keys
    sorted_keys = sorted(dictionary.keys())                   
    
    if target_key in dictionary:    
        return dictionary[target_key]
    
    for i in range(len(sorted_keys) - 1):
        if sorted_keys[i] <= target_key <= sorted_keys[i+1]:
            x0, y0 = sorted_keys[i], dictionary[sorted_keys[i]]
            x1, y1 = sorted_keys[i+1], dictionary[sorted_keys[i+1]]
            return y0 + (y1 - y0) * (target_key - x0) / (x1 - x0)
        
    # If the value was not directly in dictionary or not in the range of the sorted keys 
    # (i.e., smaller than smallest value or larger than largest value) retun an Error
    raise ValueError("Target key is out of bounds for interpolation")



def execute(pol_json, rating_table=None):
    '''
    Calculates the D&O policy premium from a json input (i.e., API call) containing a policy's _
    rating application information
    '''
    
    policy_app = pol_json
    policy = PolicyApplication(
        asset_size=policy_app['Asset Size'],
        limit=policy_app['Limit'],
        retention=policy_app['Retention'],
        industry=policy_app['Industry']
        )
    
    # Default rating table, can update table through input
    if not rating_table:
        rating_table = {
            "lcm": 1.7,
            "industry_factor": {
                "HG_1": 1.00,
                "HG_2": 1.25,
                "HG_3": 1.50
            },
            "asset_size_base_rate":{
                "1": 1065,
                "1000000":	1819,
                "2500000":	3966,
                "5000000":	3619,
                "10000000":	4291,
                "15000000":	4905,
                "20000000":	5120,
                "25000000":	5499,
                "50000000":	6279,
                "75000000":	6966,
                "100000000":7156,
                "250000000":8380
            },
            "limit_retention_factor":{
                    "0":	    -0.760,
                    "1000":	    -0.600,
                    "2500":	    -0.510,
                    "5000":	    -0.406,
                    "7500":	    -0.303,
                    "10000":	-0.231,
                    "15000":	-0.128,
                    "20000":	-0.064,
                    "25000":	0.000,
                    "35000":	0.105,
                    "50000":	0.175,
                    "75000":	0.277,
                    "100000":	0.350,
                    "125000":	0.406,
                    "150000":	0.452,
                    "175000":	0.491,
                    "200000":	0.525,
                    "225000":	0.555,
                    "250000":	0.581,
                    "275000":	0.605,
                    "300000":	0.627,
                    "325000":	0.648,
                    "350000":	0.666,
                    "375000":	0.684,
                    "400000":	0.700,
                    "425000":	0.715,
                    "450000":	0.730,
                    "475000":	0.743,
                    "500000":	0.756,
                    "525000":	0.807,
                    "550000":	0.819,
                    "575000":	0.831,
                    "600000":	0.842,
                    "625000":	0.853,
                    "650000":	0.864,
                    "675000":	0.874,
                    "700000":	0.883,
                    "725000":	0.893,
                    "750000":	0.902,
                    "775000":	0.910,
                    "800000":	0.919,
                    "825000":	0.927,
                    "850000":	0.935,
                    "875000":	0.943,
                    "900000":	0.950,
                    "925000":	0.957,
                    "950000":	0.964,
                    "975000":	0.971,
                    "1000000":	1.000,
                    "2000000":	1.415,
                    "2500000":	1.526,
                    "3000000":	1.637,
                    "4000000":	1.820,
                    "5000000":	1.986,
                    "6000000":	2.135
            }
        }  
      
    # Determine premium rating components
    base_rate = linear_interpolate(rating_table["asset_size_base_rate"], policy.asset_size) # need to finalize interpolation   
    limit_factor = linear_interpolate(rating_table["limit_retention_factor"], policy.limit + policy.retention)   
    retention_factor = linear_interpolate(rating_table["limit_retention_factor"],policy.retention)
    industry_factor = rating_table["industry_factor"][policy.hazard_group]
    lcm = rating_table["lcm"]    
    
    # Calculate premiums from rating components based on premium rules provided
    policy_premium = round( base_rate * (limit_factor - retention_factor) * industry_factor * lcm, 2)
    
    return policy_premium    
    
    