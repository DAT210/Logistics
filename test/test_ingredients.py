import sys
sys.path.append('../')
import unittest
import json, base64

from test_db import create_db, delete_db
from src import create_app, db

class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        create_db()
        app = create_app('test')
        self.app = app.test_client()
        token = self.app.get('v1/locations/login', headers={'Authorization' : 'Basic {}'.format(base64.b64encode(b'admin:password').decode('utf8'))})
        self.headers = {'Authorization': json.loads(token.data)['token']}

    def tearDown(self):
        delete_db()

   # Testing GET methods
    def test_get_ingredient_succeed(self):
        response = self.app.get('v1/locations/1/ingredients/Ham', headers=self.headers)
        self.assertEqual('200 OK', response.status)

    def test_get_ingredient_fail(self):
        response = self.app.get('v1/locations/1/ingredients/lego', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)
    
    def test_get_all_succeed(self):
        response = self.app.get('v1/locations/1/ingredients', headers=self.headers)
        self.assertEqual('200 OK', response.status)
    

    # Testing POST methods
    def test_add_ingredient(self):
        data = {'ingredientName' : 'Tofu', 'ingredientAmount' : 20}
        response = self.app.post('v1/locations/1/ingredients', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('201 CREATED', response.status)

    def test_add_ingredient_no_data(self):
        response = self.app.post('v1/locations/1/ingredients', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)
    
    def test_add_ingredient_bad_JSON(self):
        data = {'ingredientName' : 'Egg'}
        response = self.app.post('v1/locations/1/ingredients', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)

    def test_add_no_json(self):
        response = self.app.post('v1/locations/1/ingredients', data='hello', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)
    

    # Testing PUT methods
    def test_update_ingredient(self):
        data = {'ingredientAmount' : 20, 'action' : 'add'}
        response = self.app.put('v1/locations/1/ingredients/Ham', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('204 NO CONTENT', response.status)

    def test_update_ingredient_bad_action(self):
        data = {'ingredientAmount' : 20, 'action' : 'multiply'}
        response = self.app.put('v1/locations/1/ingredients/Ham', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('400 BAD REQUEST', response.status)

    def test_update_no_ingredient_fail(self):
        data = {'ingredientAmount' : 20, 'action' : 'add'}
        response = self.app.put('v1/locations/1/ingredients/lego', data=json.dumps(data), content_type='application/json', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)


    # Testing DELETE methods
    def test_delete_ingredient(self):
        response = self.app.delete('v1/locations/1/ingredients/Ham', headers=self.headers)
        self.assertEqual('204 NO CONTENT', response.status)
    
    def test_delete_ingredient_not_found(self):
        response = self.app.delete('v1/locations/1/ingredients/lego', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)


    # Testing routing
    def test_location_fail(self):
        response = self.app.get('v1/locations/999/ingredients', headers=self.headers)
        self.assertEqual('404 NOT FOUND', response.status)


if __name__ == "__main__":
    unittest.main()
