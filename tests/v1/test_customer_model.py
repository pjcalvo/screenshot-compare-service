from api.blueprints.v1.model.customer import Customer
from flask_sqlalchemy import model
from api import settings
import pytest


class TestCustomerModel:

    def test_customer_creation(self, client):
        customer = Customer('54de6568-0aa1-40ad-83fd-8edbb3a08939', 'test user', 'pablo@email.com')
        assert customer.uuid == '54de6568-0aa1-40ad-83fd-8edbb3a08939'
        assert customer.display_name == 'test user'
        assert customer.email == 'pablo@email.com'

    def test_customer_creation_in_env(self, client, monkeypatch):
        settings.ENV = 'production'
        customer = Customer('54de6568-0aa1-40ad-83fd-8edbb3a08939', 'test user', 'pablo@email.com')
        assert customer.uuid == '54de6568-0aa1-40ad-83fd-8edbb3a08939'
        assert customer.display_name == 'test user'
        assert customer.email == 'pablo@email.com'

    def test_classname(self):
        customer = Customer('juan', 'perez', 'test@automation.com')
        assert f'{customer}' == "Customer(display_name='perez', email='test@automation.com')"
