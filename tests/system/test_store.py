import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.client() as client:
            resp = client.post('/store/test')

            self.assertEqual(resp.status_code, 201)
            self.assertIsNotNone(StoreModel.find_by_name("test"))
            self.assertDictEqual({"name": "test", "items": []},
                                 json.loads(resp.data))

    def test_create_duplicate_store(self):
        with self.client() as client:
            client.post('/store/test')
            resp = client.post('/store/test')
            self.assertEqual(resp.status_code, 400)

    def test_delete_store(self):
        with self.app_context():
            StoreModel("test").save_to_db()

        with self.client() as client:
            resp = client.delete('/store/test')
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual({'message': 'Store deleted'},
                                 json.loads(resp.data))

    def test_find_store(self):
        with self.app_context():
            StoreModel("test").save_to_db()

        with self.client() as client:
            resp = client.get('/store/test')

            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual({"name": "test", "items": []},
                                 json.loads(resp.data))

    def test_store_not_found(self):
        with self.client() as client:
            resp = client.get('/store/test')

            self.assertEqual(resp.status_code, 404)
            self.assertDictEqual({'message': 'Store not found'},
                                 json.loads(resp.data))

    def test_store_found_with_items(self):
        with self.app_context():
            StoreModel("test").save_to_db()
            ItemModel("test_item", 19.99, 1).save_to_db()

        with self.client() as client:
            resp = client.get('/store/test')

            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual({"name": "test", "items": [{"name": "test_item", "price": 19.99}]},
                                 json.loads(resp.data))

    def test_store_list(self):
        with self.app_context():
            StoreModel("test").save_to_db()

        with self.client() as client:
            resp = client.get('/stores')

            self.assertDictEqual({'stores': [{'name': "test", 'items': []}]},
                                 json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app_context():
            StoreModel("test").save_to_db()
            ItemModel("test_item", 19.99, 1).save_to_db()


        with self.client() as client:
            resp = client.get('/stores')

            self.assertDictEqual({'stores': [{'name': "test",
                                              "items": [{"name": "test_item", "price": 19.99}]}]},
                                             json.loads(resp.data))
