from api.blueprints.v1.model.user import User
import pytest


class TestUserModel:

    def test_user_creation(self):
        user = User('pablo', 'calvo')
        assert user.username == 'pablo'
        assert user.password == 'calvo'

    def test_fetch_by_id(self, db):
        user = User.find_by_id(1)

    def test_classname(self):
        user = User('juan', 'perez')
        assert f'{user}' == "User(username='juan')"
