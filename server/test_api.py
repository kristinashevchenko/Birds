import unittest
from api import app
import json
    
class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


    def tearDown(self):
        pass

    def test_version(self):
        lResp= self.app.get('/version')
        self.assertEqual(lResp.status_code, 200)
        self.assertEqual(lResp.data, b'Birds Service. Version 0.1')

    def test_attribute_value(self):
        lResp= self.app.get('/birds?attribute=namee')
        self.assertEqual(lResp.status_code, 404)
        self.assertEqual(lResp.data, b'Invalid value for attribute param')

        lResp= self.app.get('/birds?attribute=colour')
        self.assertEqual(lResp.status_code, 404)
        self.assertEqual(lResp.data, b'Invalid value for attribute param')

        lResp= self.app.get('/birds?attribute=specis')
        self.assertEqual(lResp.status_code, 404)
        self.assertEqual(lResp.data, b'Invalid value for attribute param')

        lResp= self.app.get('/birds?attribute=body_lengt')
        self.assertEqual(lResp.status_code, 404)
        self.assertEqual(lResp.data, b'Invalid value for attribute param')

        lResp= self.app.get('/birds?attribute=winspan')
        self.assertEqual(lResp.status_code, 404)
        self.assertEqual(lResp.data, b'Invalid value for attribute param')

    def test_order_value(self):
        lResp= self.app.get('/birds?attribute=name&order=des')
        self.assertEqual(lResp.status_code, 404)
        self.assertEqual(lResp.data, b'Invalid value for order param')

        lResp= self.app.get('/birds?attribute=color&order=ascc')
        self.assertEqual(lResp.status_code, 404)
        self.assertEqual(lResp.data, b'Invalid value for order param')
    
    def test_insert_empty(self):
        payload = json.dumps({})
        response = self.app.post('/birds', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'Invalid value')


    def test_insert_invalid_bird(self):
        payload = json.dumps({
            'name': 'Henry',
            'color': 'red',
            'body_length': 20,
            'wingspan': 2
        })
        response = self.app.post('/birds', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'Invalid value')

        payload = json.dumps({
            'namee': 'Jack',
            'color': 'white',
            'body_length': 20,
            'wingspan': 2,
            'species': 'pigeon'
        })
        response = self.app.post('/birds', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b'Invalid value')


if __name__ == "__main__":
    unittest.main()