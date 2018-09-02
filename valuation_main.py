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
    pool = Pool(4)
    p=StockProvider(WebProvider())

    symbols=["WMT","FAST","KMB","M","PRU","KSS","VLO","INTC","STX","PFE","TGT","PFG","MET","HD","KRO","TXN","EMN","IP","KLAC","CVS","CMI","WDC","ETN","TROW","FNF","QCOM","OMC","VZ","XOM","HSY","CAH","IBM","K","DRI","EMR","GIS","GPC","MXIM","MO","UNP","NWL","XLNX","CHRW","WEC","ADP","PEP","CLX","VFC","MMM","PAYX","UPS","LMT","HAS","OKE"]
    #symbols=["WMT"]
    stocks=pool.map(p.get_stock, symbols)
    stocks.sort(key=lambda x: -x.total_score())

    print(
        'symbol',
        '\t', 'total',
        '\t', 'target_price',
        '\t', 'target_pe',
        '\t', 'dividend',
        '\t', 'dividend_payout',
        '\t', 'median_analyst',
        '\t', 'growth',
        '\t', 'dividend_cashflow_payout'
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
            '\t', round(s.dividend_cashflow_payout_score()),
            '\t', round(s.median_analyst_score())
        )
