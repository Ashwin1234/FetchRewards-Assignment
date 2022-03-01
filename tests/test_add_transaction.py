import json
from urllib import response


def test_index(client):
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
    res = client.post('/add_transaction',data = json.dumps(data),headers = headers)
    assert res.status_code == 200
    expected = "added transactions"
    assert expected == res