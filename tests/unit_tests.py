# unit_tests.py

import unittest
import asyncio
from unittest.mock import patch, mock_open, call
from main import fetch_country_data, print_country_info, write_to_csv

class TestCountryInfoFunctions(unittest.TestCase):
    @patch('main.aiohttp.ClientSession.get')
    @patch('main.aiohttp.ClientSession.__aenter__')
    async def test_fetch_country_data_success(self, mock_aenter, mock_get):
        # Mock a successful API response
        mock_response = mock_get.return_value
        mock_response.json.return_value = [
            {
                'name': {'common': 'Country1'},
                'currencies': {'CUR': {'name': 'Currency1'}},
                'capital': ['Capital1'],
                'altSpellings': ['Alt1', 'Alt2']
            }
        ]

        # Call the function
        result = await fetch_country_data(mock_aenter, 'Country1')

        # Assert that the function returns the expected result
        self.assertEqual(result, mock_response.json.return_value)

    @patch('main.aiohttp.ClientSession.get')
    @patch('main.aiohttp.ClientSession.__aenter__')
    async def test_fetch_country_data_error(self, mock_aenter, mock_get):
        # Mock an error in the API response
        mock_response = mock_get.return_value
        mock_response.raise_for_status.side_effect = Exception("API error")

        # Call the function
        result = await fetch_country_data(mock_aenter, 'Country1')

        # Assert that the function handles errors gracefully
        self.assertIsNone(result)

    async def test_print_country_info(self):
        # Capture printed output
        with patch('builtins.print') as mock_print:
            # Call the function with sample data
            await asyncio.run(print_country_info([
                {
                    'name': {'common': 'Country1'},
                    'currencies': {'CUR': {'name': 'Currency1'}},
                    'capital': ['Capital1'],
                    'altSpellings': ['Alt1', 'Alt2']
                }
            ]))

            # Assert that the printed output matches the expected format
            mock_print.assert_has_calls([
                call("Country Name: Country1"),
                call("Currency: Currency1"),
                call("Capital: Capital1"),
                call("Alternate Spellings: Alt1, Alt2"),
            ], any_order=False)

    async def test_write_to_csv(self):
        # Mock open function to capture file content
        with patch('builtins.open', mock_open()) as mock_file:
            # Call the function with sample data
            await asyncio.run(write_to_csv([
                ('Country1', 'Currency1', 'Capital1', 'Alt1, Alt2'),
                ('Country2', 'Currency2', 'Capital2', 'Alt3, Alt4')
            ]))

            # Assert that the file is opened and written to correctly
            mock_file.assert_called_with('country_info.csv', mode='w', newline='')
            handle = mock_file()
            handle.write.assert_called_with(
                'Country Name,Currency,Capital,Alternate Spellings\n'
                'Country1,Currency1,Capital1,Alt1, Alt2\n'
                'Country2,Currency2,Capital2,Alt3, Alt4\n'
            )

if __name__ == '__main__':
    unittest.main()
