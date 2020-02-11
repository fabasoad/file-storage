import logging
import os

from aiohttp import web
from ..service.filestorage_service import FileStorageService

class FileStorageResource:

    def __init__(self, web):
        self.log = logging.getLogger('FileStorageResource')
        self.service = FileStorageService()
        self.routes = [
            web.get('/', self.index),
            web.get('/dist/{filename}.js', self.index_js),
            web.get('/dist/{filename}.css', self.index_css),
            web.get('/files', self.get_files),
            web.post('/files/{name}', self.upload_file),
            web.delete('/files/{name}', self.delete_file)
        ]

    async def index(self, request):
        index_html = open(os.path.join('public', 'index.html'), "r")
        return web.Response(
            text=index_html.read(),
            content_type='text/html')

    async def index_js(self, request):
        return await self._index_file(request, '.js', 'application/json')

    async def index_css(self, request):
        return await self._index_file(request, '.css', 'text/css')

    async def _index_file(self, request, ext, content_type):
        filename = request.match_info['filename']
        content = open(os.path.join('public', 'dist', filename + ext), "r")
        return web.Response(
            text=content.read(),
            content_type=content_type)

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
