import pytest
from flask import url_for
from api.blueprints.v1.resources.customer import Customer


class TestUserResource:

    def test_user_register_with_missing_user_data(self, client):
        res = client.post(url_for('v1.customer'))
        assert res.status_code == 400

    def test_user_register_with_missing_display_name(self, client):
        res = client.post(
            url_for('v1.customer',
                    uuid="54de6568-0aa1-40ad-83fd-8edbb3a08939",
                    email="pablo"))
        assert res.json.get('message').get('display_name') == 'This field cannot be blank.'
        assert res.status_code == 400

    def test_user_register_with_missing_incorrect_uuid(self, client):
        res = client.post(url_for('v1.customer', uuid="54de6568-0aa1-40ad-", username='pablo'))
        assert res.json.get('message').get('uuid') == 'Error while parsing customer UUID.'
        assert res.status_code == 400

    def test_user_register_with_missing_incorrect_email(self, client):
        res = client.post(
            url_for('v1.customer',
                    uuid="54de6568-0aa1-40ad-83fd-8edbb3a08939",
                    display_name="pablo calvo"))
        assert res.json.get('message').get('email') == 'This field cannot be blank.'
        assert res.status_code == 400

    def test_register_exisiting_customer(self, client):
        res = client.post(
            url_for('v1.customer',
                    uuid="54de6568-0aa1-40ad-83fd-8edbb3a08939",
                    display_name='Pablo Calvo',
                    email="pablo@email.com"))
        print(res.json)
        assert res.json.get('message') == 'Customer created successfully.'
        # assert res.json.get('message') == 'A user with that username already exists.'
        assert res.status_code == 201

    def test_register_duplicated_uuid_customer(self, client):
        client.post(
            url_for('v1.customer',
                    uuid="54de6568-0aa1-40ad-83fd-8edbb3a08939",
                    display_name='Pablo Calvo',
                    email="pablo@email.com"))
        res = client.post(
            url_for('v1.customer',
                    uuid="54de6568-0aa1-40ad-83fd-8edbb3a08939",
                    display_name='Pablo Calvo',
                    email="pablo@email.com"))
        print(res.json)
        assert res.json.get('message') == 'A customer with that uuid already exists.'
        assert res.status_code == 400

    def test_register_duplicated_customer(self, client):
        client.post(
            url_for('v1.customer',
                    uuid="54de6568-0aa1-40ad-83fd-8edbb3a08939",
                    display_name='Pablo Calvo',
                    email="pablo@email.com"))
        res = client.post(
            url_for('v1.customer',
                    uuid="8238f5b3-dadf-4ae7-a2d6-d1bd073a51b0",
                    display_name='Pablo Calvo',
                    email="pablo@email.com"))
        print(res.json)
        assert res.json.get('message') == 'This email is already in use.'
        assert res.status_code == 400
