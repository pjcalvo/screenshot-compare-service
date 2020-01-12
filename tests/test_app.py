import pytest
from flask import url_for


class TestApp:

    def test_home(self, client):
        res = client.get(url_for('index'))
        assert res.status_code == 200

    def test_status(self, client):
        res = client.get(url_for('status'))
        assert res.json == {'message': 'Healthy app is healthy and secure!'}
        assert res.status_code == 200
