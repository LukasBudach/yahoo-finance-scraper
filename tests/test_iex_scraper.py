import unittest
import logging

from financescraper import scraper


class TestIEXScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = scraper.IEXScraper()
        logging.disable(logging.ERROR)

    def tearDown(self):
        self.scraper.close_connection()
        logging.disable(logging.NOTSET)

    def test_scraper_default_init(self):
        self.assertTrue(self.scraper.use_buffer)
        self.assertEqual(self.scraper.buffer.max_size, 10)
        self.assertEqual(self.scraper.buffer.max_holding_time, 15)
        self.assertEqual(self.scraper.url, 'https://api.iextrading.com/1.0/stock/')

    def test_scraper_get_data(self):
        valid_ticker = 'AMZN'
        invalid_ticker = 'TL0.F'

        response = self.scraper.get_data(valid_ticker)
        self.assertIsNotNone(response)
        self.assertEqual(response.source, 'IEX')
        self.assertTrue((type(response.price) == float) or (type(response.price) == int))

        response = self.scraper.get_data(invalid_ticker)
        self.assertIsNone(response)

    def test_scraper_get_company(self):
        valid_ticker = 'AMZN'
        invalid_ticker = 'TL0.F'

        response = self.scraper.get_company_data(valid_ticker)
        self.assertIsNotNone(response)
        self.assertNotEqual(response.name, 'No name found')
        self.assertEqual(response.symbol, valid_ticker)

        response = self.scraper.get_company_data(invalid_ticker)
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
