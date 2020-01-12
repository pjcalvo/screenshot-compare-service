import pytest
import json
from api.libs.security import identity, authenticate
from api.blueprints.v1.model.user import User


class TestSecurity:

    # custom class to be the mock return value
    test_user = User("test", "user")
    test_user.id = 1

    def test_authentication_positive(self, client, monkeypatch):
        monkeypatch.setattr(User, 'find_by_username', lambda *args: User("test", "user"))
        authenticate(self.test_user.username, self.test_user.password)

    def test_authentication_false(self, client, monkeypatch):
        monkeypatch.setattr(User, 'find_by_username', lambda *args: User("test-false", "user"))
        authenticate(self.test_user.username, self.test_user.password)

    def test_incomplete_data(self, client):
        with pytest.raises(TypeError):
            authenticate()

    def test_identity(self, client, monkeypatch):
        # mock for get all
        def mock_get(*args, **kwargs):
            mocked_user = User('', '')
            mocked_user.id = 1
            return mocked_user
        monkeypatch.setattr(User, 'find_by_id', mock_get)

        payload = {'identity': 1}
        result_user = identity(payload)
        assert result_user.id == 1

    def test_identity_false(self, client, monkeypatch):
        monkeypatch.setattr(User, 'find_by_id', lambda *args: None)
        payload = {"identity": 2}
        result_user = identity(payload)
        assert result_user is None
