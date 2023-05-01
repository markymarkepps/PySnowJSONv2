import requests
import json


class ServiceNowAPI:
    def __init__(self, instance, username, password, session=None):
        """
        Initializes a new ServiceNowAPI object.

        :param instance: The ServiceNow instance name.
        :param username: The username to authenticate with.
        :param password: The password to authenticate with.
        :param session: An optional authenticated session. If provided, the session will be used instead of creating a new
                        session with the given username and password.
        """
        self.instance = instance
        self.username = username
        self.password = password
        self.base_url = f"https://{self.instance}.service-now.com"
        self.session = session or requests.Session()
        if not session:
            self.session.auth = (self.username, self.password)
        self.session.headers.update({'Content-Type': 'application/json', 'Accept': 'application/json'})

    def _get_path(self, table, sys_id=None):
        """
        Returns the API path for a given table and sys_id.

        :param table: The name of the table.
        :param sys_id: An optional sys_id. If provided, the path will be for a specific record.
        :return: The API path for the table and sys_id.
        """
        path = f"/{table}.do"
        if sys_id:
            path += f"?sys_id={sys_id}"
        return path

    def _request(self, method, path, data=None, params=None):
        """
        Sends an HTTP request to the ServiceNow API.

        :param method: The HTTP method to use.
        :param path: The API path to request.
        :param data: An optional JSON data payload for POST and PATCH requests.
        :param params: An optional dictionary of query parameters for GET requests.
        :return: The response JSON object.
        """
        url = self.base_url + path
        response = self.session.request(method, url, json=data, params=params)
        response.raise_for_status()
        try:
            return response.json()['result']
        except KeyError:
            return response.json()

    def get_record(self, table, sys_id):
        """
        Retrieves a single record from a table by sys_id.

        :param table: The name of the table.
        :param sys_id: The sys_id of the record to retrieve.
        :return: The record JSON object.
        """
        path = self._get_path(table, sys_id)
        return self._request('GET', path)

    def get_records(self, table, query=None):
        """
        Retrieves all records from a table that match the given query.

        :param table: The name of the table.
        :param query: An optional query string to filter records.
        :return: A list of record JSON objects.
        """
        params = {'JSONv2': ''}
        if query:
            params['sysparm_query'] = query
        path = self._get_path(table)
        results = []
        while True:
            response = self._request('GET', path, params=params)
            results.extend(response['records'])
            if len(response['records']) < int(response['sysparm_record_count']):
                break
            params['sysparm_offset'] = len(results)
        return results

    def create_record(self, table, data):
        """
        Creates a new record in a table.

        :param table: The name of the table.
        :param data: A dictionary containing field names and values for the new record.
        :return: The sys_id of the newly created record.
        """
        path = self._get_path(table, action='insert')
        return self._request('POST', path, data)

    def update_record(self, table, sys_id, data):
        """
        Updates a single record in a table.

        :param table: The name of the table.
        :param sys_id: The sys_id of the record to update.
        :param data: A dictionary containing field names and values to update the record.
        :return: The sys_id of the newly created record.
        """
        path = self._get_path(table, sys_id, 'update')
        return self._request('POST', path, data)

    def delete_record(self, table, sys_id):
        """
        Deletes a single record from a table.

        :param table: The name of the table.
        :param sys_id: The sys_id of the record to delete.
        :return: ???
        """
        path = self._get_path(table, sys_id, 'deleteRecord')
        return self._request('POST', path)