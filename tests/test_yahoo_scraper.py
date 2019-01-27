import unittest
import logging

from financescraper import scraper


class TestYahooScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper.YahooScraper()
        logging.disable(logging.ERROR)

    def tearDown(self):
        self.scraper.close_connection()
        logging.disable(logging.NOTSET)

    def test_scraper_default_init(self):
        self.assertTrue(self.scraper.use_buffer)
        self.assertEqual(self.scraper.buffer.max_size, 10)
        self.assertEqual(self.scraper.buffer.max_holding_time, 15)
        self.assertEqual(self.scraper.url, 'https://finance.yahoo.com/quote/')

    def test_scraper_set_buffer_size(self):
        self.scraper.set_buffer_size(5)
        self.assertEqual(self.scraper.buffer.max_size, 5)

    def test_scraper_set_holding_time(self):
        self.scraper.set_holding_time(10)
        self.assertEqual(self.scraper.buffer.max_holding_time, 10)

    def test_scraper_get_data(self):
        valid_ticker = 'AMZN'
        invalid_ticker = 'AAAA'

        response = self.scraper.get_data(valid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response['Source'], 'Yahoo')
        self.assertEqual(type(response['Price']), float)

        response = self.scraper.get_data(invalid_ticker)
        self.assertIsNone(response)

    def test_scraper_get_company(self):
        valid_ticker = 'AMZN'
        invalid_ticker = 'AAAA'

        response = self.scraper.get_company_data(valid_ticker)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['Company Name'])
        self.assertEqual(response['Symbol'], valid_ticker)

        response = self.scraper.get_company_data(invalid_ticker)
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
