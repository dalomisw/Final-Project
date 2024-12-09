"""
Create tests for the code in the final_project.py file.
Wiktoria Dalomis
"""
import unittest
from unittest.mock import patch, MagicMock
from final_project import (
    get_available_currencies,
    get_current_rates,
    get_historical_rates,
    convert_usd_to_currency,
    predict_trend,
    convert_between_currencies,
    get_exchange_rate_for_many_days
)

class TestCurrencyExchangeRateTracker(unittest.TestCase):

    @patch('final_project.requests.get')
    def test_get_available_currencies(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"USD": "United States Dollar", "EUR": "Euro"}
        mock_get.return_value = mock_response

        currencies = get_available_currencies()
        self.assertIn("USD", currencies)
        self.assertIn("EUR", currencies)

    @patch('final_project.requests.get')
    def test_get_current_rates(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"USD": 1, "EUR": 0.85}}
        mock_get.return_value = mock_response

        rates = get_current_rates()
        self.assertIn("rates", rates)
        self.assertEqual(rates["rates"]["USD"], 1)
        self.assertEqual(rates["rates"]["EUR"], 0.85)

    @patch('final_project.requests.get')
    def test_get_historical_rates(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"USD": 1, "EUR": 0.85}}
        mock_get.return_value = mock_response

        date = "2023-01-01"
        rates = get_historical_rates(date)
        self.assertIn("USD", rates)
        self.assertIn("EUR", rates)

    @patch('final_project.requests.get')
    def test_convert_usd_to_currency(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"EUR": 0.85}}
        mock_get.return_value = mock_response

        amount = 100
        currency = "EUR"
        converted_amount = convert_usd_to_currency(amount, currency)
        self.assertEqual(converted_amount, 85)

    def test_predict_trend(self):
        exchange_rates = [1.0, 1.1, 1.2, 1.3, 1.4]
        slope, intercept, trend = predict_trend(exchange_rates)
        self.assertGreater(slope, 0)
        self.assertEqual(trend, "upward")

    @patch('final_project.requests.get')
    def test_convert_between_currencies(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"USD": 1, "EUR": 0.85, "GBP": 0.75}}
        mock_get.return_value = mock_response

        amount = 100
        original_currency = "EUR"
        new_currency = "GBP"
        converted_amount = convert_between_currencies(amount, original_currency, new_currency)
        self.assertAlmostEqual(converted_amount, 88.24, places=2)

    @patch('final_project.requests.get')
    def test_get_exchange_rate_for_many_days(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"USD": 1, "EUR": 0.85}}
        mock_get.return_value = mock_response

        currency = "EUR"
        number_of_days = 5
        rates = get_exchange_rate_for_many_days(currency, number_of_days)
        self.assertEqual(len(rates), number_of_days)
        self.assertTrue(all(rate == 0.85 for rate in rates))

if __name__ == '__main__':
    unittest.main()

