import json

from django.test.client import RequestFactory
from django.test.testcases import TestCase
from mock import patch

from external_api.api import entity_data_list_view


class ExternalAPITestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('os.listdir')
    def test_entity_data_list_view(self, directory_mock):

        expected_content = ['sourceUno.csv', 'source_dos.csv',
                            'source__tres.csv']

        directory_mock.return_value = expected_content

        request = self.factory.get('/entities/get_entity_list')

        response = entity_data_list_view(request)

        self.assertEqual(200, response.status_code)
        self.assertEqual(json.dumps(expected_content), response.content)
