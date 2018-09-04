import math
from util import p2f, sigmoid


def target_price_score(price: float, target_price: float) -> float:
    return sigmoid(-math.log2(price / target_price) * 4) * 100


def pe_score(pe: float) -> float:
    return sigmoid(-math.log2(pe/20) * 2) * 100


def dividend_score(dividend_yield: float, mean_dividend_yield: float) -> float:
    return sigmoid(math.log2(dividend_yield / mean_dividend_yield) * 8) * 100


def dividend_payout_score(dividend_payout_rate: float) -> float:
    return sigmoid(4.0 / dividend_payout_rate - 6.0) * 100


def growth_score(growth_rate: float) -> float:
    #return sigmoid(math.log2(1.0 + growth_rate - 0.03) * 20.0) * 100
    return sigmoid((1-1/(1+growth_rate))*60-1.8)*100
