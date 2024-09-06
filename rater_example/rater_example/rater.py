from dataclasses import dataclass
from numbers import Number
from typing import List, Dict, Optional, Union


JsonObj = Dict[str, any]


HAZARD_GROUP_LOOKUP = {
    "Hazard Group 1": "HG_1",
    "Hazard Group 2": "HG_2",
    "Hazard Group 3": "HG_3"
}

@dataclass
class PolicyApplication:
    asset_size: int
    limit: int
    retention: int
    industry: str

    @property
    def hazard_group(self):
        """
        Create a tranformation from policy info to rating table variable
        for Hazard Group, default to HG_1.
        """
        return HAZARD_GROUP_LOOKUP.get(self.industry, "HG_1")


def convert_dict_keys(dictionary: dict, key_type: type) -> dict:
    """
    Converts dictionary keys to specified type
    """
    return {key_type(k):v for k,v in dictionary.items()}


@dataclass
class RatingTable:
    lcm: float
    industry_factor: Dict[str, int]
    asset_size_base_rate: Dict[int, int]
    limit_retention_factor: Dict[int, float]

    def __post_init__(self):
        # sort dicts in-case they are not sorted
        self.asset_size_base_rate = dict(sorted(self.asset_size_base_rate.items()))
        self.limit_retention_factor = dict(sorted(self.limit_retention_factor.items()))

    @staticmethod
    def from_json(json_data) -> 'RatingTable':
        return RatingTable(
            lcm=json_data['lcm'],
            industry_factor=json_data['industry_factor'],
            asset_size_base_rate=convert_dict_keys(json_data['asset_size_base_rate'], int),
            limit_retention_factor=convert_dict_keys(json_data['limit_retention_factor'], int)
        )


DEFAULT_RATING_TABLE = RatingTable(
    lcm=1.7,
    industry_factor={
        "HG_1": 1.00,
        "HG_2": 1.25,
        "HG_3": 1.50
    },
    asset_size_base_rate={
        1: 1065,
        1000000: 1819,
        2500000: 3966,
        5000000: 3619,
        10000000: 4291,
        15000000: 4905,
        20000000: 5120,
        25000000: 5499,
        50000000: 6279,
        75000000: 6966,
        100000000: 7156,
        250000000: 8380
    },
    limit_retention_factor={
        0: -0.760,
        1000: -0.600,
        2500: -0.510,
        5000: -0.406,
        7500: -0.303,
        10000: -0.231,
        15000: -0.128,
        20000: -0.064,
        25000:	0.000,
        35000:	0.105,
        50000:	0.175,
        75000:	0.277,
        100000:	0.350,
        125000:	0.406,
        150000:	0.452,
        175000:	0.491,
        200000:	0.525,
        225000:	0.555,
        250000:	0.581,
        275000:	0.605,
        300000:	0.627,
        325000:	0.648,
        350000:	0.666,
        375000:	0.684,
        400000:	0.700,
        425000:	0.715,
        450000:	0.730,
        475000:	0.743,
        500000:	0.756,
        525000:	0.807,
        550000:	0.819,
        575000:	0.831,
        600000:	0.842,
        625000:	0.853,
        650000:	0.864,
        675000:	0.874,
        700000:	0.883,
        725000:	0.893,
        750000:	0.902,
        775000:	0.910,
        800000:	0.919,
        825000:	0.927,
        850000:	0.935,
        875000:	0.943,
        900000:	0.950,
        925000:	0.957,
        950000:	0.964,
        975000:	0.971,
        1000000:1.000,
        2000000:1.415,
        2500000:1.526,
        3000000:1.637,
        4000000:1.820,
        5000000:1.986,
        6000000:2.135
    })


def linear_interpolate(dictionary: Dict[int, Number], target_key: Number) -> float:
    """
    Linear interpolates a target value amoungst a dictionary with intermediate key, value pairs.

    Required that dictionary keys are sorted!
    """

    # # Sort the dictionary keys
    sorted_keys = dictionary.keys()

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


def execute(pol_json: JsonObj, rating_table: Optional[Union[RatingTable, JsonObj]] = None):
    """
    Calculates the D&O policy premium from a json input (i.e., API call) containing a policy's _
    rating application information
    """

    policy = PolicyApplication(
        asset_size=pol_json['Asset Size'],
        limit=pol_json['Limit'],
        retention=pol_json['Retention'],
        industry=pol_json['Industry']
        )

    # Default rating table, can update table through input
    if not rating_table:
        rating_table = DEFAULT_RATING_TABLE
    else:
        if not isinstance(rating_table, RatingTable):
            rating_table = RatingTable.from_json(rating_table)

    # Determine premium rating components
    base_rate = linear_interpolate(rating_table.asset_size_base_rate, policy.asset_size) # need to finalize interpolation
    limit_factor = linear_interpolate(rating_table.limit_retention_factor, policy.limit + policy.retention)
    retention_factor = linear_interpolate(rating_table.limit_retention_factor, policy.retention)
    industry_factor = rating_table.industry_factor[policy.hazard_group]
    lcm = rating_table.lcm

    # Calculate premiums from rating components based on premium rules provided
    policy_premium = round( base_rate * (limit_factor - retention_factor) * industry_factor * lcm, 2)

    return policy_premium

