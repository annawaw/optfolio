import abc, json, math, re, statistics
from util import p2f, sigmoid
from web_provider import WebProvider


class Stock:
    def __init__(self):
        return

    @abc.abstractmethod
    def target_price_score(self):
        return


class YahooStock:
    def __init__(self, data):
        stores = data['context']['dispatcher']['stores']
        quote_summary = stores['QuoteSummaryStore']

        self.symbol=quote_summary['symbol']
        self.price=quote_summary['price']['regularMarketPrice']['raw']
        self.shares_outstanding = quote_summary['defaultKeyStatistics']['sharesOutstanding']['raw']
        self.five_year_avg_dividend_yield=quote_summary['summaryDetail']['fiveYearAvgDividendYield']['raw']/100.0
        self.forward_dividend_yield=p2f(quote_summary['summaryDetail']['dividendYield']['fmt'])
        self.forward_dividend_rate = quote_summary['summaryDetail']['dividendRate']['raw']

        try:
            self.dividend_payout_ratio=p2f(quote_summary['summaryDetail']['payoutRatio']['fmt'])
        except KeyError:
            self.dividend_payout_ratio=None

        self.forward_pe=float(quote_summary['summaryDetail']['forwardPE']['fmt'])

        try:
            self.earnings_growth = quote_summary['financialData']['earningsGrowth']['raw']
        except KeyError:
            self.earnings_growth = None

        self.revenue_growth = quote_summary['financialData']['revenueGrowth']['raw']

        try:
            self.free_cashflow = quote_summary['financialData']['freeCashflow']['raw']
        except KeyError:
            self.free_cashflow = None

        self.target_mean_price = quote_summary['financialData']['targetMeanPrice']['raw']
        self.recommendation_mean = quote_summary['financialData']['recommendationMean']['raw']

    def dividend_payout_ratio_rev(self):
        return 1.0/self.dividend_payout_ratio

    def dividend_cashflow_ratio_rev(self):
        return (self.free_cashflow/self.shares_outstanding)/self.forward_dividend_rate if self.free_cashflow is not None else None

    def target_price_score(self):
        return sigmoid(-math.log2(self.price/self.target_mean_price)*4)*100

    def target_pe_score(self):
        return sigmoid(-math.log2(self.forward_pe/25.0)*2)*100

    def dividend_score(self):
        return sigmoid(math.log2(self.forward_dividend_yield/self.five_year_avg_dividend_yield)*2)*100

    def dividend_payout_score(self):
        try:
            #return max(min(100 + 100 * ((0.55 - self.dividend_payout_ratio) / 0.3), 100), 0) if self.dividend_payout_ratio is not None else 0
            return sigmoid(self.dividend_payout_ratio_rev())*100
        except:
            return 0

    def dividend_cashflow_payout_score(self):
        #return max(min(100 + 100 * ((0.55 - self.dividend_cashflow_ratio()) / 0.3), 100), 0)
        return sigmoid(self.dividend_cashflow_ratio_rev())*100 if self.dividend_cashflow_ratio_rev() is not None else 0

    def median_analyst_score(self):
        return max(min(125 - self.recommendation_mean * 25, 100), 0)

    def growth_score(self):
        scores=[
            self._growth_score(self.earnings_growth),
            self._growth_score(self.revenue_growth),
        ]
        return statistics.mean([x for x in scores if x is not None])

    def total_score(self):
        return statistics.mean([
            self.target_price_score(),
            self.target_pe_score(),
            self.growth_score(),
            self.dividend_score(),
            self.dividend_payout_score(),
            self.dividend_cashflow_payout_score(),
            self.median_analyst_score(),
        ])

    def _growth_score(self, growth):
        return sigmoid((growth - 0.04) * 50) * 100 if growth is not None else None

    def __str__(self):
        return f'Stock(symbol={self.symbol}, price={self.price})'


def stock_from_yahoo(provider: WebProvider, symbol: str) -> Stock:
    p=re.compile('root.App.main\s=\s(\{.*?\}});')
    content_str=str(provider.get(f'https://finance.yahoo.com/quote/{symbol}'))

    json_str=p.search(content_str).group(1).replace('\\\\"', '\\"').replace('\\\'', '\'').replace('\\x', '\\\\x')
    data=json.loads(json_str)

    return YahooStock(data)
