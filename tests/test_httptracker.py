import asyncio

import aiohttp.test_utils
import aiohttp.web
import pytest

from ipaddress import IPv4Address

from magnet2torrent.bencode import bencode
from magnet2torrent.httptracker import retrieve_peers_http_tracker


async def tracker_response(status, body, sleep_time=0):
    app = aiohttp.web.Application()
    async def handler(request):
        await asyncio.sleep(sleep_time)
        return aiohttp.web.Response(status=status, body=body)
    app.router.add_route('get', '/', handler)

    server = aiohttp.test_utils.TestServer(app)
    async with server:
        return await retrieve_peers_http_tracker(set(), f'http://localhost:{server.port}/', 'infohash')


@pytest.mark.asyncio
async def test_success():
    payload = {
        b"complete": 10,
        b"incomplete": 20,
        b"peers": b"\x01\x02\x03\x04\x00\x10\x01\x02\x03\x05\x00\x11"
    }
    tracker, result = await tracker_response(200, bencode(payload))
    assert result == {"seeders": 10, "leechers": 20, "peers": [(IPv4Address("1.2.3.4"), 16), (IPv4Address("1.2.3.5"), 17), ]}


@pytest.mark.asyncio
async def test_error():
    tracker, result = await tracker_response(502, b'')
    assert result == {"seeders": 0, "leechers": 0, "peers": []}
