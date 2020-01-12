import pytest
from flask import url_for
from api.blueprints.v1.resources.status import Status


class TestStatus:

    def test_status(self, client):
        res = client.get(url_for('v1.status'))
        assert res.status_code == 200
        assert res.json == {'message': 'Api version: 1'}

    def test_classname(self):
        res = Status()
        assert f'{res}' == 'Status'
