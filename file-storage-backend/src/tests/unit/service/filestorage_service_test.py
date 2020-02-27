import os
import sys

def test_get_files():
    service = FileStorageService(RedisFactoryMock())
    assert service.get_files() == [{ 'filename': 'test', 'size': 112 }]

class RedisFactoryMock:
    def create_instance(self):
        print('test')
        return 

class RedisMock:
    def mget(self, keys):
        assert keys == ['K1', 'K2']
        return [{
            'requested_filename': 'test',
            'size': 112
        }]
    def keys(self, pattern):
        return ['K1', 'K2']