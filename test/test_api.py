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

    # Testing methods
    def test_get_item_succeed(self):
        response = self.app.get('/locations/1/inventories/Milk')
        self.assertEqual('200 OK', response.status)

    def test_get_item_fail(self):
        response = self.app.get('/locations/1/inventories/lego')
        self.assertEqual('404 NOT FOUND', response.status)
    
    def test_get_all_succeed(self):
        response = self.app.get('/locations/1/inventories')
        self.assertEqual('200 OK', response.status)

    





    # Testing routing
    def test_location_fail(self):
        response = self.app.get('/locations/999/inventories')
        self.assertEqual('404 OK', response.status)


if __name__ == "__main__":
    unittest.main()
