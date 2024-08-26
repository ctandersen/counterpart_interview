import pytest

from rater_example.rater_example.rater import execute
from rater_example.rater_example.rater import PolicyApplication
from rater_example.rater_example.rater import linear_interpolate

# Create a base policy for testing
@pytest.fixture
def json_input():
    return {"Asset Size": 1200000, 
            "Limit": 5000000, 
            "Retention": 1000000, 
            "Industry": "Hazard Group 2"}

# Base policy premium result, determine in EXCEL / calculator
@pytest.fixture
def premium_result():
    return 4062.11

# Test golden policy works and match EXCEL result
def test_execute_main(json_input, premium_result):
    premium = execute(json_input) 
    assert  premium == premium_result
    

# Test asset size works, both in linear interpolate and on direct boundary
def test_execute_asset_size(json_input, premium_result):
    json_input['Asset Size'] = 2
    premium = execute(json_input) 
    assert  premium < premium_result
    
    json_input['Asset Size'] = 2000000
    premium = execute(json_input) 
    assert  premium > premium_result
    
# Test limit is working correctly
def test_execute_limit(json_input, premium_result):
    json_input['Limit'] = 4000000
    premium = execute(json_input) 
    assert  premium < premium_result
    

# Test retention is working correctly
def test_execute_retention(json_input, premium_result):
    json_input['Retention'] = 0
    premium = execute(json_input) 
    assert  premium > premium_result
    
    json_input['Retention'] = 2000000
    json_input['Limit'] = 4000000
    premium = execute(json_input) 
    assert  premium < premium_result

    json_input['Retention'] = 2000000
    json_input['Limit'] = 5000000
    with pytest.raises(ValueError, match="Target key is out of bounds for interpolation"):
        execute(json_input) 


# Test out of bounds for assets, i.e., above rating thresholds, return an error
def test_execute_high_assets(json_input):
    json_input['Asset Size'] = 300000000
    with pytest.raises(ValueError, match="Target key is out of bounds for interpolation"):
        execute(json_input) 



# Test PolicyApplication class initiates
def test_policyapp_constructor():
    policy_app = PolicyApplication(
        asset_size=1200000,
        limit=1000000,
        retention=1000000,
        industry="Hazard Group 2")
    assert isinstance(policy_app, PolicyApplication)
    


# Setup test for linear interpoloation function
def test_linear_interpolate():
    dct={"0": 1.0,"10":2.0}
    assert linear_interpolate(dct, 5) == 1.5
    assert linear_interpolate(dct, 0) == 1.0
    assert linear_interpolate(dct, 10.0) == 2.0
    with pytest.raises(ValueError, match="Target key is out of bounds for interpolation"):
        linear_interpolate(dct, 11.0) 
        linear_interpolate(dct, 0.5) 
