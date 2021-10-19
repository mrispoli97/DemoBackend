import redis
import json
from pprint import pprint


class Pipeline:

    def __init__(self, name):
        self._name = name
        self._redis = redis.Redis()

    def __len__(self):
        return self._redis.llen(self._name)

    def put(self, data):
        self._redis.rpush(self._name, json.dumps(data))

    def pop(self):
        json_data = self._redis.lpop(self._name)
        data = json.loads(json_data)
        return data


class RequestPipeline(Pipeline):

    def __init__(self):
        super(RequestPipeline, self).__init__(name='pipeline:request')


class Table:

    def __init__(self, name):
        self._name = name
        self._redis = redis.Redis()

    def __contains__(self, key):
        keys = [key.decode('utf-8') for key in self._redis.hkeys(self._name)]
        return key in keys

    def set(self, key, data):
        self._redis.hset(self._name, key, data)

    def get(self, key):
        data = self._redis.hget(self._name, key).decode('utf-8')
        return data

    def remove(self, key):
        self._redis.hdel(self._name, key)


class ResponseTable(Table):

    def __init__(self):
        super(ResponseTable, self).__init__(name='table:response')
