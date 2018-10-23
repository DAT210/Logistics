import sys
sys.path.append('../')
import unittest
import json, base64

from src import create_app, db

class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'
        self.app = app.test_client()
        token = self.app.get('v1/locations/login', headers={'Authorization' : 'Basic {}'.format(base64.b64encode(b'admin:password').decode('utf8'))})
        self.headers = {'Authorization': json.loads(token.data)['token']}

   # Testing GET methods
    def test_get_item_succeed(self):
        response = self.app.get('v1/locations/1/ingredients/Milk', headers=self.headers)
        self.assertEqual('200 OK', response.status)

    def test_get_item_fail(self):
        response = self.app.get('v1/locations/1/ingredients/lego', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)
    
    def test_get_all_succeed(self):
        response = self.app.get('v1/locations/1/ingredients', headers=self.headers)
        self.assertEqual('200 OK', response.status)
    

    # Testing POST methods
    def test_add_item(self):
        data = {'itemName' : 'Tofu', 'itemAmount' : 20}
        response = self.app.post('v1/locations/1/ingredients', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('201 CREATED', response.status)

    def test_add_item_no_data(self):
        response = self.app.post('v1/locations/1/ingredients', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)
    
    def test_add_item_bad_JSON(self):
        data = {'itemName' : 'Egg'}
        response = self.app.post('v1/locations/1/ingredients', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)

    def test_add_no_json(self):
        response = self.app.post('v1/locations/1/ingredients', data='hello', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)
    

    # Testing PUT methods
    def test_update_item(self):
        data = {'itemAmount' : 20, 'action' : 'add'}
        response = self.app.put('v1/locations/1/ingredients/Milk', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('204 NO CONTENT', response.status)

    def test_update_item_bad_action(self):
        data = {'itemAmount' : 20, 'action' : 'multiply'}
        response = self.app.put('v1/locations/1/ingredients/Milk', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)

    def test_update_no_item_fail(self):
        data = {'itemAmount' : 20, 'action' : 'add'}
        response = self.app.put('v1/locations/1/ingredients/lego', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)


    # Testing DELETE methods
    def test_delete_item(self):
        response = self.app.delete('v1/locations/1/ingredients/Tofu', headers=self.headers)
        self.assertEqual('204 NO CONTENT', response.status)
    
    def test_delete_item_not_found(self):
        response = self.app.delete('v1/locations/1/ingredients/lego', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)


    # Testing routing
    def test_location_fail(self):
        response = self.app.get('v1/locations/999/ingredients', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)


if __name__ == "__main__":
    unittest.main()
