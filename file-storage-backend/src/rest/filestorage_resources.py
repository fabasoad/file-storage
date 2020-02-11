import logging
import os

from aiohttp import web
from ..service.filestorage_service import FileStorageService

class FileStorageResource:

    def __init__(self, web):
        self.log = logging.getLogger('FileStorageResource')
        self.service = FileStorageService()
        self.routes = [
            web.get('/{folder}/{filename}.{ext}', self.index_file),
            web.get('/files', self.get_files),
            web.get('/', self.index),
            web.post('/files/{name}', self.upload_file),
            web.delete('/files/{name}', self.delete_file)
        ]

    async def index(self, request):
        index_html = open(os.path.join('public', 'index.html'), "r")
        return web.Response(
            text=index_html.read(),
            content_type='text/html')

    async def index_file(self, request):
        ext_dict = {
            'css': 'text/css',
            'js': 'application/javascript',
            'png': 'image/png',
            'map': 'text/plain'
        }
        filename = request.match_info['filename']
        ext = request.match_info['ext']
        folder = request.match_info['folder']
        content = open(os.path.join('public', folder, '{}.{}'.format(filename, ext)), "r", encoding="utf-8")
        return web.Response(
            text=content.read(),
            content_type=ext_dict[ext])

    async def index_img(self, request):
        filename = request.match_info['filename']
        ext = request.match_info['ext']
        content = open(os.path.join('public', 'images', '{}.{}'.format(filename, ext)), "r")
        return web.Response(
            text=content.read(),
            content_type='image/' + ext)

    async def get_files(self, request):
        result = self.service.get_files()
        return web.json_response(result)

    async def upload_file(self, request):
        filename = request.match_info['name']
        result = await self.service.save_file(filename, await request.multipart())
        return web.json_response(result, status=201)
    
    async def delete_file(self, request):
        filename = request.match_info['name']
        result = self.service.delete_file(filename)
        return web.json_response(result)
