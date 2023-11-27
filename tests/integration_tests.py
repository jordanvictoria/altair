# integration_tests.py

import unittest
from unittest.mock import patch, mock_open, Mock
from main import fetch_and_process_country, write_to_csv

class TestIntegration(unittest.TestCase):
    @patch('main.fetch_country_data')
    @patch('main.print_country_info')
    @patch('main.write_to_csv')
    async def test_fetch_and_process_country(self, mock_write_to_csv, mock_print_country_info, mock_fetch_country_data):
        # Mock a successful API response
        mock_fetch_country_data.side_effect = [
            [
                {
                    'name': {'common': 'Country1'},
                    'currencies': {'CUR': {'name': 'Currency1'}},
                    'capital': ['Capital1'],
                    'altSpellings': ['Alt1', 'Alt2']
                }
            ],
            [
                {
                    'name': {'common': 'Country2'},
                    'currencies': {'CUR': {'name': 'Currency2'}},
                    'capital': ['Capital2'],
                    'altSpellings': ['Alt3', 'Alt4']
                }
            ]
        ]

        # Call the function
        await fetch_and_process_country(Mock(), 'Country1')
        await fetch_and_process_country(Mock(), 'Country2')

        # Assert that the fetch, print, and write functions are called correctly
        mock_fetch_country_data.assert_called_with('Country1')
        mock_print_country_info.assert_called_with(mock_fetch_country_data.return_value)
        mock_write_to_csv.assert_called_with([
            ('Country1', 'Currency1', 'Capital1', 'Alt1, Alt2')
        ])

        # Call the function again with a different country
        await fetch_and_process_country(Mock(), 'Country2')

        # Assert that the fetch, print, and write functions are called correctly for the second country
        mock_fetch_country_data.assert_called_with('Country2')
        mock_print_country_info.assert_called_with(mock_fetch_country_data.return_value)
        mock_write_to_csv.assert_called_with([
            ('Country1', 'Currency1', 'Capital1', 'Alt1, Alt2'),
            ('Country2', 'Currency2', 'Capital2', 'Alt3, Alt4')
        ])

if __name__ == '__main__':
    unittest.main()

