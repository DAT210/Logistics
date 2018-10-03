import sys
sys.path.append('../')
import unittest
import json

from src import create_app, db

class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'
        self.app = app.test_client()

    # Testing GET methods
    def test_get_all_locations(self):
        response = self.app.get('v1/locations')
        self.assertEqual('200 OK', response.status)

    def test_get_one_locations(self):
        response = self.app.get('v1/locations/1')
        self.assertEqual('200 OK', response.status)

    def test_get_one_locations_fail(self):
        response = self.app.get('v1/locations/999')
        self.assertEqual('404 NOT FOUND', response.status)

    # Testing POST methods
    def test_create_location(self):
        data = {'locationName' : 'McDonalds'}
        response = self.app.post('v1/locations', data=json.dumps(data), content_type='application/json')
        self.assertEqual('201 CREATED', response.status)

    def test_add_item_no_data(self):
        response = self.app.post('v1/locations')
        self.assertEqual('400 BAD REQUEST', response.status)

    def test_add_no_json(self):
        response = self.app.post('v1/locations', data='hello')
        self.assertEqual('400 BAD REQUEST', response.status)

    # Testing PUT methods
    def test_update_item(self):
        data = {'locationName' : 'Big Horn'}
        response = self.app.put('v1/locations', data=json.dumps(data), content_type='application/json')
        self.assertEqual('204 NO CONTENT', response.status)

    def test_update_no_item_fail(self):
        data = {'locationName' : 'Wendy'}
        response = self.app.put('v1/locations/999', data=json.dumps(data), content_type='application/json')
        self.assertEqual('404 NOT FOUND', response.status)

    # Testing DELETE methods
    def test_delete_item(self):
        response = self.app.delete('v1/locations/3')
        self.assertEqual('204 NO CONTENT', response.status)
    
    def test_delete_item_not_found(self):
        response = self.app.delete('v1/locations/999')
        self.assertEqual('404 NOT FOUND', response.status)

if __name__ == "__main__":
    unittest.main()
