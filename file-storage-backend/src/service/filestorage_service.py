import errno
import hashlib
import json
import logging
import os

from .redis_factory import RedisFactory

class FileStorageException(Exception):

    def __init__(self, reason):
        self.reason = reason

class FileValidationException(FileStorageException):

    def __init__(self, reason):
        FileStorageException.__init__(self, reason)   

class FileStorageService:

    FORM_PARAMETER = 'file'
    FILESTORAGE_PATH = os.environ.get('FILESTORAGE_PATH', '/usr/files/')

    def __init__(self):
        self.log = logging.getLogger('FileStorageService')
        self.redis_factory = RedisFactory()
    
    def get_files(self):
        redis = self.redis_factory.create_instance()
        data = redis.mget(redis.keys('file-*'))
        return [self._build_file_entity(json.loads(info)) for info in data]

    async def save_file(self, filename, reader):
        redis = self.redis_factory.create_instance()
        if redis.get(self._build_key(self._hash(filename))) is not None:
            raise FileValidationException('File with {} name already exists'.format(filename))

        field = await reader.next()
        while field is not None and field.name != self.FORM_PARAMETER:
            field = await reader.next()

        if field is None:
            raise FileValidationException('\"{}\" parameter is missing'.format(self.FORM_PARAMETER))

        info = {
            'origin_filename': field.filename,
            'hash_filename': self._hash(filename),
            'requested_filename': filename,
            'path': self.FILESTORAGE_PATH
        }

        self._try_create_folder()
        size = await self._try_save_file(field, info['hash_filename'])
        info['size'] = size
        redis.set(self._build_key(info['hash_filename']), json.dumps(info))
        return self._build_file_entity(info)

    def _try_create_folder(self):
        if not os.path.exists(self.FILESTORAGE_PATH):
            try:
                os.makedirs(self.FILESTORAGE_PATH)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise FileStorageException('Failed to access to the file storage')
    
    async def _try_save_file(self, field, filename):
        size = 0
        with open(os.path.join(self.FILESTORAGE_PATH, filename), 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
        return size

    def delete_file(self, filename):
        redis = self.redis_factory.create_instance()
        key = self._build_key(self._hash(filename))
        data = redis.get(key)
        if data is None:
            raise FileValidationException('{} file does not exist'.format(filename))
        info = json.loads(data)
        os.remove(os.path.join(info['path'], info['hash_filename']))
        redis.delete(key)
        return self._build_file_entity(info)
    
    def _build_key(self, filename):
        return 'file-{}'.format(filename)
    
    def _build_file_entity(self, data):
        return { 'filename': data['requested_filename'], 'size': data['size'] }

    def _hash(self, val):
        hasher = hashlib.sha256()
        hasher.update(val.encode('ascii'))
        return hasher.hexdigest()
