import unittest
import asyncio
from unittest.mock import patch, mock_open, call
from main import fetch_country_data, print_country_info, write_to_csv

class TestCountryInfoFunctions(unittest.TestCase):
    @patch('main.aiohttp.ClientSession.get')
    @patch('main.aiohttp.ClientSession.__aenter__')
    async def test_fetch_country_data_success(self, mock_aenter, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = [
            {
                'name': {'common': 'Country1'},
                'currencies': {'CUR': {'name': 'Currency1'}},
                'capital': ['Capital1'],
                'altSpellings': ['Alt1', 'Alt2']
            }
        ]

        result = await fetch_country_data(mock_aenter, 'Country1')

        self.assertEqual(result, mock_response.json.return_value)

    @patch('main.aiohttp.ClientSession.get')
    @patch('main.aiohttp.ClientSession.__aenter__')
    async def test_fetch_country_data_error(self, mock_aenter, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.side_effect = Exception("API error")

        result = await fetch_country_data(mock_aenter, 'Country1')

        self.assertIsNone(result)

    async def test_print_country_info(self):
        with patch('builtins.print') as mock_print:
            await asyncio.run(print_country_info([
                {
                    'name': {'common': 'Country1'},
                    'currencies': {'CUR': {'name': 'Currency1'}},
                    'capital': ['Capital1'],
                    'altSpellings': ['Alt1', 'Alt2']
                }
            ]))

            mock_print.assert_has_calls([
                call("country_name: Country1"),
                call("currency: Currency1"),
                call("capital: Capital1"),
                call("alt_spellings: Alt1, Alt2"),
            ], any_order=False)

    async def test_write_to_csv(self):
        with patch('builtins.open', mock_open()) as mock_file:
            await asyncio.run(write_to_csv([
                ('Country1', 'Currency1', 'Capital1', 'Alt1, Alt2'),
                ('Country2', 'Currency2', 'Capital2', 'Alt3, Alt4')
            ]))

            mock_file.assert_called_with('country_info.csv', mode='w', newline='')
            handle = mock_file()
            handle.write.assert_called_with(
                'country_name,currency,capital,alt_spellings\n'
                'Country1,Currency1,Capital1,Alt1, Alt2\n'
                'Country2,Currency2,Capital2,Alt3, Alt4\n'
            )

if __name__ == '__main__':
    unittest.main()
