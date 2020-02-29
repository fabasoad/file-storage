import hashlib
import json
import os
import pytest
import sys

from ..filestorage_service import FileStorageService, FileValidationException
from ..redis_factory import RedisFactory

from redis import Redis
from unittest.mock import mock_open, patch, MagicMock

def test_get_files():
    mget_result = ['{"requested_filename": "abc123", "size": 123}']
    keys_result = 'def321'
    with patch.object(Redis, 'keys', return_value=keys_result) as mock_keys:
        with patch.object(Redis, 'mget', return_value=mget_result) as mock_mget:
            redis = Redis()
            redis_factory = RedisFactory()
            redis_factory.create_instance = MagicMock(return_value = redis)
            service = FileStorageService(redis_factory)
            assert service.get_files() == [{ 'filename': 'abc123', 'size': 123 }]
            mock_mget.assert_called_once_with(keys_result)
            mock_keys.assert_called_once_with(_build_key('*'))

@patch('os.path.exists')
@patch('os.makedirs')
@patch("builtins.open", new_callable=mock_open, read_data="data")
@pytest.mark.asyncio
async def test_save_file_when_exist(mock_os_path_exists, mock_os_makedirs, mock_open):
    with patch.object(Redis, 'get', return_value='NotNone') as mock_get:
        with patch.object(Redis, 'set') as mock_set:
            filename = 'abc123'
            expected_key = _build_key(_hash(filename))
            redis = Redis()
            redis_factory = RedisFactory()
            redis_factory.create_instance = MagicMock(return_value = redis)
            service = FileStorageService(redis_factory)
            try:
                await service.save_file(filename, None)
                assert False
            except FileValidationException:
                mock_get.assert_called_once_with(expected_key)
                mock_set.assert_not_called()
                mock_os_path_exists.assert_not_called()
                mock_os_makedirs.assert_not_called()
                mock_open.assert_not_called()

@patch('os.path.exists')
@patch('os.makedirs')
@patch("builtins.open", new_callable=mock_open, read_data="data")
@pytest.mark.asyncio
async def test_save_file_with_empty_reader_result(mock_os_path_exists, mock_os_makedirs, mock_open):
    await _save_file_with_invalid_reader(mock_os_path_exists, mock_os_makedirs, mock_open, lambda: ReaderMock(0))

@patch('os.path.exists')
@patch('os.makedirs')
@patch("builtins.open", new_callable=mock_open, read_data="data")
@pytest.mark.asyncio
async def test_save_file_with_invalid_reader_result(mock_os_path_exists, mock_os_makedirs, mock_open):
    await _save_file_with_invalid_reader(mock_os_path_exists, mock_os_makedirs, mock_open, lambda: ReaderMock(3))

async def _save_file_with_invalid_reader(mock_os_path_exists, mock_os_makedirs, mock_open, reader_factory):
    with patch.object(Redis, 'get', return_value=None) as mock_get:
        with patch.object(Redis, 'set') as mock_set:
            filename = 'abc123'
            expected_key = _build_key(_hash(filename))
            redis = Redis()
            redis_factory = RedisFactory()
            redis_factory.create_instance = MagicMock(return_value = redis)
            service = FileStorageService(redis_factory)
            try:
                await service.save_file(filename, reader_factory())
                assert False
            except FileValidationException:
                mock_get.assert_called_once_with(expected_key)
                mock_set.assert_not_called()
                mock_os_path_exists.assert_not_called()
                mock_os_makedirs.assert_not_called()
                mock_open.assert_not_called()

@patch("builtins.open", new_callable=mock_open, read_data="data")
@patch.dict('os.environ', {'FILESTORAGE_PATH': os.getcwd()})
@pytest.mark.asyncio
async def test_save_file(mock_open):
    mock_open.return_value = 'NotNone'
    with patch.object(Redis, 'get', return_value=None) as mock_get:
        with patch.object(Redis, 'set') as mock_set:
            filename = 'abc123'
            field_filename = 'abc456'
            expected_key = _build_key(_hash(filename))
            redis = Redis()
            redis_factory = RedisFactory()
            redis_factory.create_instance = MagicMock(return_value = redis)
            service = FileStorageService(redis_factory)
            expected = {
                'origin_filename': field_filename,
                'hash_filename': _hash(filename),
                'requested_filename': filename,
                'path': service.FILESTORAGE_PATH,
                'size': 0
            }
            actual = await service.save_file(filename, ReaderMock(1, service.FORM_PARAMETER, field_filename))
            assert actual == {
                'filename': expected['requested_filename'],
                'size': expected['size']
            }
            mock_get.assert_called_once_with(expected_key)
            mock_set.assert_called_once_with(_build_key(expected['hash_filename']), json.dumps(expected))

@patch('os.remove')
def test_delete_file_positive(mock_os_remove):
    get_result = {
        'path': "/test/",
        'hash_filename': "abcdef",
        'requested_filename': "ghi",
        'size': 456
    }
    with patch.object(Redis, 'get', return_value=json.dumps(get_result)) as mock_get:
        with patch.object(Redis, 'delete') as mock_delete:
            filename = 'abc123'
            expected_key = _build_key(_hash(filename))
            redis = Redis()
            redis_factory = RedisFactory()
            redis_factory.create_instance = MagicMock(return_value = redis)
            service = FileStorageService(redis_factory)
            assert service.delete_file(filename) == {
                'filename': get_result['requested_filename'],
                'size': get_result['size']
            }
            mock_get.assert_called_once_with(expected_key)
            mock_delete.assert_called_once_with(expected_key)
            mock_os_remove.assert_called_once_with(
                os.path.join(get_result['path'], get_result['hash_filename']))

@patch('os.remove')
def test_delete_file_negative(mock_os_remove):
    with patch.object(Redis, 'get', return_value=None) as mock_get:
        with patch.object(Redis, 'delete') as mock_delete:
            filename = 'abc123'
            expected_key = _build_key(_hash(filename))
            redis = Redis()
            redis_factory = RedisFactory()
            redis_factory.create_instance = MagicMock(return_value = redis)
            service = FileStorageService(redis_factory)
            try:
                service.delete_file(filename)
            except FileValidationException:                
                mock_get.assert_called_once_with(expected_key)
                mock_delete.assert_not_called()
                mock_os_remove.assert_not_called()
                return
            assert False

def _build_key(filename):
    return 'file-{}'.format(filename)

def _hash(val):
    hasher = hashlib.sha256()
    hasher.update(val.encode('ascii'))
    return hasher.hexdigest()

class ReaderMock:
    def __init__(self, limit, name='abc123', filename=None):
        self.counter = 0
        self.limit = limit
        self.name = name
        self.filename = filename

    async def next(self):
        if self.counter == self.limit:
            return None
        else:
            self.counter += 1
            return ReaderFieldMock(self.name, self.filename)

class ReaderFieldMock:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    async def read_chunk(self):
        return False