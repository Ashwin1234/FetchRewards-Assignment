import unittest

from app import app

import json

class AppTestCase(unittest.TestCase):
    def setUp(self):
       app.config['TESTING'] = True
       app.config['DEBUG'] = True
       self.app = app.test_client()

    def tearDown(self):
        pass
    
    # Test case 1 for adding transactions
    def test_add_transaction1(self):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = [
        { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02 14:00:00" },
        { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31 11:00:00" },
        { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31 08:00:00" },
        { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01 14:00:00" },
        { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31 12:00:00" }
        ]
        res = self.app.post('/add_transaction',data = json.dumps(data),headers = headers)
        print(res.data)
        assert res.status_code == 200
  
        
    
    # Test case 2 for adding transactions
    def test_add_transaction2(self):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02 14:00:00" }
        res = self.app.post('/add_transaction',data = json.dumps(data),headers = headers)
        print(res.data)
        assert res.status_code == 200
        

    # Test case 1 for cheking spend balances
    def test_spend_balance1(self):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = {
       "points": 5000
            }
        res = self.app.post('/spend_points',data = json.dumps(data),headers = headers)
        assert res.status_code == 200
        


    # Test case 2 for checking spend balance
    def test_spend_balance2(self):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = {
       "points": 3000
            }
        res = self.app.post('/spend_points',data = json.dumps(data),headers = headers)
        assert res.status_code == 200

    # Test case 1 for checking remaining balance
    def test_point_balances(self):
        res = self.app.get('/point_balances')
        assert res.status_code == 200

if __name__ == "__main__":
    unittest.main()