import sys
sys.path.append('../')
import unittest
import json, base64

from test_db import create_db, delete_db
from src import create_app, db

class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        create_db()
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/testDB'
        self.app = app.test_client()
        token = self.app.get('v1/locations/login', headers={'Authorization' : 'Basic {}'.format(base64.b64encode(b'admin:password').decode('utf8'))})
        self.headers = {'Authorization': json.loads(token.data)['token']}

    def tearDown(self):
        delete_db()


    # Testing GET methods
    def test_get_all_locations(self):
        response = self.app.get('v1/locations/', headers=self.headers)
        self.assertEqual('200 OK', response.status)

    def test_get_one_location(self):
        response = self.app.get('v1/locations/1', headers=self.headers)
        self.assertEqual('200 OK', response.status)

    def test_get_one_location_fail(self):
        response = self.app.get('v1/locations/999', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)

    # Testing POST methods
    def test_create_location(self):
        data = {'locationName' : 'McDonalds'}
        response = self.app.post('v1/locations/', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('201 CREATED', response.status)

    def test_add_location_no_data(self):
        response = self.app.post('v1/locations/', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)

    def test_add_no_json(self):
        response = self.app.post('v1/locations/', data='hello', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)

    # Testing PUT methods
    def test_update_location(self):
        data = {'locationName' : 'Big Horn'}
        response = self.app.put('v1/locations/1', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('204 NO CONTENT', response.status)

    def test_update_no_location_fail(self):
        data = {'locationName' : 'Wendy'}
        response = self.app.put('v1/locations/999', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)

    # Testing DELETE methods
    def test_delete_location(self):
        response = self.app.delete('v1/locations/3', headers=self.headers)
        self.assertEqual('204 NO CONTENT', response.status)
    
    def test_delete_location_not_found(self):
        response = self.app.delete('v1/locations/999', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)

if __name__ == "__main__":
    unittest.main()
