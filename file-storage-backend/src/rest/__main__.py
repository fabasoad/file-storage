import os
import sys

from aiohttp import web
from .middlewares import error_middleware
from .system_resources import SystemResource
from .filestorage_resources import FileStorageResource

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 8081

host = os.environ.get('FILESTORAGE_BACKEND_HOST', DEFAULT_HOST)
port = os.environ.get('FILESTORAGE_BACKEND_PORT', DEFAULT_PORT)

system_resources = SystemResource(web)
filestorage_resource = FileStorageResource(web)

app = web.Application(middlewares=[error_middleware])
app.add_routes(system_resources.routes + filestorage_resource.routes)
web.run_app(app, host=host, port=port)
