import sample

ticker = ['TSLA', 'AAPL', 'TSLA', 'AMZN', 'GOOG', 'AAPL', 'TSLA', 'FZM.F', '7974.T', 'AAPL']
currencies = ['USD', 'EUR', 'GBP', 'JPY']

dollar_converter = sample.conversions.CurrencyConverter('USD')
euro_converter = sample.conversions.CurrencyConverter('EUR')
yahoo_scraper = sample.scraper.YahooScraper()

for t in ticker:
    print(yahoo_scraper.get_data(t))
    print(yahoo_scraper.get_company_data(t))

for c in currencies:
    print(dollar_converter.convert(c, 1))
    print(euro_converter.convert(c, 1))
