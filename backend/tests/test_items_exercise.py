import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_items_all():
    r = client.get('/items')
    assert r.status_code == 200
    data = r.json()
    names = {d['name'] for d in data}
    assert {'Alpha', 'Beta'}.issubset(names)

def test_list_items_filter_match():
    r = client.get('/items?q=alp')
    assert r.status_code == 200
    data = r.json()
    assert any(d['name'] == 'Alpha' for d in data)

def test_list_items_filter_no_match_returns_empty():
    r = client.get('/items?q=ZZZ_DOES_NOT_MATCH')
    assert r.status_code == 200
    assert r.json() == []