import json

from aiohttp import web

class SystemResource:

    def __init__(self, web):
        self.routes = [
            web.get('/system/pulse', self.pulse)
        ]
    
    async def pulse(self, request):
        return web.json_response({ "alive": True })