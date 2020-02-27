from aiohttp import web

from ..service.filestorage_service import FileStorageException, FileValidationException

@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except FileValidationException as ex:
        return web.json_response({ 'error': ex.reason }, status=400)
    except FileStorageException as ex:
        return web.json_response({ 'error': ex.reason }, status=500)
    except web.HTTPException as ex:
        return web.json_response({ 'error': ex.reason }, status=ex.status_code)
    except Exception as ex:
        return web.json_response({ 'error': str(ex) }, status=500)