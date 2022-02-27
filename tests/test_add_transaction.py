import json


def test_index(app, client):
    res = client.get('/add_transaction')
    assert res.status_code == 200
    expected = "added transactions"
    assert expected == json.loads(res.get_data(as_text=True))