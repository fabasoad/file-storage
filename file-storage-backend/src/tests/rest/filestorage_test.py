import aiohttp
import os
import pytest

import settings

from aiohttp import FormData

async def call_get(url, handler):
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.base_url + url) as resp:
            assert resp.status == 200
            await handler(await resp.json())

async def call_delete(url, handler):
    async with aiohttp.ClientSession() as session:
        async with session.delete(settings.base_url + url) as resp:
            assert resp.status == 200
            await handler(await resp.json())

async def call_upload_file(url, filename, handler):
    filepath = os.path.join(os.getcwd(), 'src', 'tests', 'rest', filename)
    async with aiohttp.ClientSession() as session:
        data = FormData()
        data.add_field('file',
            open(filepath, 'rb'),
            filename=filename)
        async with session.post(settings.base_url + url, data=data) as resp:
            assert resp.status == 201
            await handler(await resp.json())

@pytest.mark.asyncio    
async def test_full_lifecycle():
    async def files_handler1(res1):
        assert res1 == []
        test_name = 'another_test_file.txt'

        async def upload_file_handler(res2):
            async def files_handler2(res3):
                assert len(res3) == 1
                assert res3[0]['filename'] == test_name
                assert res3[0]['size'] == 6

                async def delete_file_handler(res4):
                    assert res4 == res3[0]

                    async def files_handler3(res5):
                        assert res5 == []

                    await call_get('/files', files_handler3)

                await call_delete('/files/' + test_name, delete_file_handler)

            await call_get('/files', files_handler2)

        await call_upload_file('/files/' + test_name, 'test_file.txt', upload_file_handler)

    await call_get('/files', files_handler1)