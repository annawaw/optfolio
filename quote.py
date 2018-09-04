import abc, json, math, re, statistics
from util import p2f, sigmoid, geometric_mean
from web_provider import WebProvider
import score

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
        try:
            self.five_year_avg_dividend_yield=quote_summary['summaryDetail']['fiveYearAvgDividendYield']['raw']/100.0
        except KeyError:
            self.five_year_avg_dividend_yield=None

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

        try:
            self.target_mean_price = quote_summary['financialData']['targetMeanPrice']['raw']
        except KeyError:
            self.target_mean_price = None

        try:
            self.recommendation_mean = quote_summary['financialData']['recommendationMean']['raw']
        except KeyError:
            self.recommendation_mean = None

    def target_price_score(self):
        try:
            return score.target_price_score(
                price=self.price,
                target_price=self.target_mean_price
            )
        except:
            return 0

    def target_pe_score(self):
        return score.pe_score(pe=self.forward_pe)

    def dividend_score(self):
        try:
            return score.dividend_score(
                dividend_yield=self.forward_dividend_yield,
                mean_dividend_yield=self.five_year_avg_dividend_yield
            )
        except:
            return 0

    def dividend_payout_score(self):
        try:
            return geometric_mean([
                score.dividend_payout_score(self.dividend_payout_ratio),
                score.dividend_payout_score(self.forward_dividend_rate / (self.free_cashflow / self.shares_outstanding))
            ])
        except:
            return 0

    def median_analyst_score(self):
        try:
            return max(min(125 - self.recommendation_mean * 25, 100), 0)
        except:
            return 0

    def growth_score(self):
        def _scores():
            if self.earnings_growth is not None:
                yield score.growth_score(self.earnings_growth)
            if self.revenue_growth is not None:
                yield score.growth_score(self.revenue_growth)

        return statistics.mean(_scores())

    def total_score(self):
        return geometric_mean([
            self.target_price_score(),
            self.target_pe_score(),
            self.growth_score(),
            self.dividend_score(),
            self.dividend_payout_score(),
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
