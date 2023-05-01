# PySnowJSONv2 Client

PySnowJSONv2 is a Python package for interacting with a ServiceNow instance using the JSONv2 web service. It provides a simple and intuitive interface for performing CRUD (create, read, update, delete) operations on ServiceNow records.


## Usage

```python
from servicenow_api import ServiceNowAPI

# create a new API client
api = ServiceNowAPI(instance='your-instance', username='your-username', password='your-password')

# get a single record
record = api.get_record(table='incident', sys_id='00000000000000000000000000000001')

# get all records with a specific status
records = api.get_records(table='incident', query='active=true^state=1')

# create a new record
data = {'short_description': 'New incident', 'description': 'This is a test incident'}
sys_id = api.create_record(table='incident', data=data)

# update an existing record
data = {'short_description': 'Updated incident'}
api.update_record(table='incident', sys_id=sys_id, data=data)

# delete an existing record
api.delete_record(table='incident', sys_id=sys_id)
```