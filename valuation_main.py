from web_provider import WebProvider,FakeProvider
from quote import stock_from_yahoo
from multiprocessing import Pool


class StockProvider:
    def __init__(self, provider):
        self.provider=provider

    def get_stock(self, symbol):
        try:
            return stock_from_yahoo(self.provider, symbol)
        except Exception as e:
            raise IOError("Error processing " + symbol) from e


if __name__ == '__main__':
    pool = Pool(2)
    p=StockProvider(WebProvider())

    #symbols=["WMT","FAST","KMB","M","PRU","KSS","VLO","INTC","STX","PFE","TGT","PFG","MET","HD","KRO","TXN","EMN","IP","KLAC","CVS","CMI","WDC","ETN","TROW","FNF","QCOM","OMC","VZ","XOM","HSY","CAH","IBM","K","DRI","EMR","GIS","GPC","MXIM","MO","UNP","NWL","XLNX","CHRW","WEC","ADP","PEP","CLX","VFC","MMM","PAYX","UPS","LMT","HAS","OKE"]
    #symbols=["JHG"]
    symbols = ['PFE', 'VZ', 'PG', 'PEP', 'WMT', 'HD', 'XOM', 'IBM', 'MMM', 'UNP', 'INTC', 'MO', 'TXN', 'QCOM', 'UPS', 'LMT', 'CVS', 'ADP', 'VLO', 'EMR', 'TGT', 'PRU', 'KMB', 'ETN', 'VFC', 'TROW', 'OKE', 'GIS', 'PAYX', 'CMI', 'WEC', 'IP', 'XLNX', 'CLX', 'KLAC', 'K', 'MXIM', 'FAST', 'CAH', 'OMC', 'PFG', 'GPC', 'DRI', 'HSY', 'EMN', 'CHRW', 'HAS', 'FNF', 'M', 'NWL', 'HRL', 'PKG', 'SNA', 'RHI', 'WU', 'GRMN', 'CPB', 'JWN', 'HP', 'HOG', 'GPS', 'PACW', 'PII', 'EV', 'LEG', 'LAZ', 'FL', 'AIZ', 'WSM', 'WSO', 'SON', 'JHG', 'UMPQ', 'NUS', 'AEO', 'MSM', 'CBRL', 'FLO', 'LANC', 'MDP', 'FII', 'ERIE', 'BGS', 'NWBI', 'MCY', 'SAFT', 'TUP', 'WDR', 'EIG', 'BPFH', 'AFSI', 'SWM', 'SCS', 'STC', 'AVX', 'CNS', 'NHC', 'VIVO', 'ETH', 'BKE']

    stocks=pool.map(p.get_stock, symbols)
    stocks.sort(key=lambda x: -x.total_score())

    print(
        'symbol',
        '\t', 'total',
        '\t', 'target_price',
        '\t', 'target_pe',
        '\t', 'growth',
        '\t', 'dividend',
        '\t', 'dividend_payout',
        '\t', 'median_analyst'
    )

    for s in stocks:
        print(
            s.symbol,
            '\t', round(s.total_score(), 2),
            '\t', round(s.target_price_score()),
            '\t', round(s.target_pe_score()),
            '\t', round(s.growth_score()),
            '\t', round(s.dividend_score()),
            '\t', round(s.dividend_payout_score()),
            '\t', round(s.median_analyst_score())
        )
