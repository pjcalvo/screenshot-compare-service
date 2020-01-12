import pytest
from api.libs.custom_types import type_uuid


class TestCustomType:

    def test_uuid_validation_positive(self, client):
        type_uuid('b7f978cc-0235-4371-bb3e-d809c46c34b3')

    def test_uuid_validation_error(self, client):
        with pytest.raises(ValueError):
            type_uuid('thisisnotanuuid')
