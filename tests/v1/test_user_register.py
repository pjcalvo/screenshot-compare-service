import pytest
from flask import url_for
from api.blueprints.v1.resources.user_register import User


class TestUserResource:

    def test_user_register_with_missing_user_data(self, client):
        res = client.post(url_for('v1.userregister'))
        assert res.status_code == 400

    def test_user_register_with_missing_incorrect_username(self, client):
        res = client.post(url_for('v1.userregister', password="pablo"))
        assert res.json.get('message').get('username') == 'This field cannot be blank.'
        assert res.status_code == 400

    def test_user_register_with_missing_incorrect_password(self, client):
        res = client.post(url_for('v1.userregister', username='pablo'))
        assert res.json.get('message').get('password') == 'This field cannot be blank.'
        assert res.status_code == 400

    def test_user_register_success(self, client):
        res = client.post(url_for('v1.userregister', username="pablonew", password="pablonew"))
        assert res.json.get('message') == 'User created successfully.'
        assert res.status_code == 201

    def test_user_exisiting_user(self, client):
        client.post(url_for('v1.userregister', username="pablotest", password="pablonew"))
        res = client.post(url_for('v1.userregister', username="pablotest", password="pablonew"))
        print(res.json)
        assert res.json.get('message') == 'A user with that username already exists.'
        assert res.status_code == 400
