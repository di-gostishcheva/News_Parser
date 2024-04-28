import unittest
from unittest.mock import patch
from your_module import LentaRuParser  # Replace 'your_module' with the actual module name

class TestLentaRuParser(unittest.TestCase):
    def setUp(self):
        self.parser = LentaRuParser()

    def test_get_url(self):
        param_dict = {
            'from': '0',
            'size': '100',
            'sort': '3',
            'title_only': '0',
            'domain': '1',
            'type': '0',
            'bloc': '0',
            'dateFrom': '2023-01-01',
            'dateTo': '2023-12-30',
            'query': 'test_query'
        }

        expected_url = ('https://lenta.ru/search/v2/process?from=0&size=100&sort=3&title_only=0&domain=1&'
                        'modified%2Cformat=yyyy-MM-dd&type=0&bloc=0&modified%2Cfrom=2023-01-01&'
                        'modified%2Cto=2023-12-30&query=test_query')

        actual_url = self.parser._get_url(param_dict)

        self.assertEqual(actual_url, expected_url)

    @patch('your_module.rq.get')
    def test_get_search_table(self, mock_get):
        mock_get.return_value.json.return_value = {'matches': [{'title': 'Test Article', 'url': 'http://test.com'}]}
        param_dict = {
            'from': '0',
            'size': '100',
            'sort': '3',
            'title_only': '0',
            'domain': '1',
            'type': '0',
            'bloc': '0',
            'dateFrom': '2023-01-01',
            'dateTo': '2023-01-01',
            'query': 'test_query'
        }

        expected_df = pd.DataFrame([{'title': 'Test Article', 'url': 'http://test.com'}])

        actual_df = self.parser._get_search_table(param_dict)

        pd.testing.assert_frame_equal(actual_df, expected_df)

if __name__ == '__main__':
    unittest.main()
