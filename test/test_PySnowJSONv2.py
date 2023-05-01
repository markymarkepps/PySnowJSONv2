import unittest
from unittest.mock import patch, Mock
from src.PySnowJSONv2 import ServiceNowJSONv2

class TestServiceNowAPI(unittest.TestCase):
    
    def setUp(self):
        self.instance = 'myinstance'
        self.username = 'myusername'
        self.password = 'mypassword'
        self.session = Mock()
        self.api = ServiceNowJSONv2(self.instance, self.username, self.password, self.session)
    
    def test_get_path_without_sys_id(self):
        path = self.api._get_path('incident')
        self.assertEqual(path, '/incident.do')
    
    def test_get_path_with_sys_id(self):
        path = self.api._get_path('incident', '123')
        self.assertEqual(path, '/incident.do?sys_id=123')
    
    def test_get_records_with_query(self):
        response = {'records': [{'number': 'INC000001', 'short_description': 'Test Incident'}]}
        self.session.request.return_value.json.return_value = {'result': response}
        records = self.api.get_records('incident', 'short_description=Test Incident')
        self.assertEqual(records, response['records'])
    
    @patch('ServiceNowJSONv2.requests.Session')
    def test_create_record(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {'result': {'sys_id': '123'}}
        mock_session.return_value.request.return_value = mock_response
        api = ServiceNowJSONv2(self.instance, self.username, self.password)
        data = {'short_description': 'Test Incident'}
        sys_id = api.create_record('incident', data)
        self.assertEqual(sys_id, '123')
    
    @patch('ServiceNowJSONv2.requests.Session')
    def test_update_record(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {'result': {'sys_id': '123'}}
        mock_session.return_value.request.return_value = mock_response
        api = ServiceNowJSONv2(self.instance, self.username, self.password)
        data = {'short_description': 'Test Incident (updated)'}
        sys_id = api.update_record('incident', '123', data)
        self.assertEqual(sys_id, '123')
    
    @patch('ServiceNowJSONv2.requests.Session')
    def test_delete_record(self, mock_session):
        mock_response = Mock()
        mock_session.return_value.request.return_value = mock_response
        api = ServiceNowJSONv2(self.instance, self.username, self.password)
        api.delete_record('incident', '123')
        mock_session.return_value.request.assert_called_once_with('POST', 'https://myinstance.service-now.com/incident.do?sys_id=123&sysparm_action=deleteRecord')
