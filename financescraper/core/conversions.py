import requests
import json
import logging

from financescraper.core import scraper
from financescraper.datacontainer.circular_buffer import CircularBuffer


class CurrencyConverter:
    def __init__(self, target_currency_code, use_buffer=True, buffer_size=10, holding_time=1800):
        self.target_currency_code = target_currency_code
        self.yahoo_scraper = scraper.YahooScraper(False)
        self.use_buffer = use_buffer

        if use_buffer:
            # add internal buffer to reduce load times on rapid, repeated requests
            self.buffer = CircularBuffer(buffer_size, holding_time)

    # sets the number of currency to conversion ratio pairs that can be saved in the internal buffer
    def set_buffer_size(self, size):
        if self.use_buffer:
            self.buffer.set_size(size)

    # sets the maximum duration in seconds for which values are allowed to be held in the buffer
    def set_holding_time(self, holding_time):
        if self.use_buffer:
            self.buffer.set_holding_time(holding_time)

    # converts the amount from its base currency to the target currency defined during initialization
    def convert(self, base_currency_code, amount):
        exchange_rate = self._get_exchange_rate(base_currency_code, self.target_currency_code)
        if exchange_rate is None:
            return exchange_rate
        else:
            return amount * exchange_rate

    # internal function fetching the exchange rate from base to target currency and saving it to the internal buffer
    def _get_exchange_rate(self, base_curr, dest_curr):
        if self.use_buffer:
            rate = self.buffer.get(base_curr)
        else:
            rate = None

        if rate is None:
            res = self.yahoo_scraper.session.get(self.yahoo_scraper.url + base_curr + dest_curr + "=X")
            if not (res.status_code == requests.codes.ok):  # pragma: no cover
                logging.error('Data fetching failed for conversion from ' + base_curr + ' to ' + dest_curr)
                return None

            raw_data = res.text

            object_start = raw_data.find("root.App.main") + 16
            object_end = raw_data.find("</script>", object_start) - 12
            data_json = raw_data[object_start: object_end]

            data_object = json.loads(data_json)
            try:
                rate = data_object['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPrice']['raw']
                if self.use_buffer:
                    self.buffer.add(base_curr, rate)
            except KeyError:
                logging.error("No valid conversion data found for " + base_curr + " to " + dest_curr)
        else:
            if self.use_buffer:
                self.buffer.refresh(base_curr)

        return rate
