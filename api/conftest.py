import os

os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("REDIS_PASSWORD", "")

import pytest


class FakeRedis:
    def __init__(self, **kwargs):
        self._data = {}

    def ping(self):
        return True

    def rpush(self, key, value):
        return 1

    def hset(self, key, field, value):
        self._data[f"{key}:{field}"] = value
        return 1

    def hget(self, key, field):
        val = self._data.get(f"{key}:{field}")
        return val.encode() if val else None


@pytest.fixture(autouse=True)
def setup_mock():
    import main
    main.r = FakeRedis()