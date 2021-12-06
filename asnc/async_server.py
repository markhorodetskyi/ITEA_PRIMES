import asyncio
import socket
from asyncio import Queue

from asnc.async_msgutils import send_msg, recv_msg, default_encoding

q = Queue()

# async def handle_client(reader, writer):
#     while True:
#         data = await recv_msg(reader)
#         if not data:
#             print(data)
#             print('not data. Disconected!')
#             continue
#         if data.decode(default_encoding) == 'quit':
#             print('quit')
#             await send_msg('ok'.encode(), writer)
#             break
#         print(data)
#         await q.put(data.decode(default_encoding))
#     writer.close()
#     await writer.wait_closed()
#     print(f'queue have {q.qsize()}')
#     print('close connection')


async def handle_client(client):
    loop = asyncio.get_event_loop()
    data = None
    while True:
        data = await recv_msg(loop, client)
        if not data:
            print(data)
            print('not data. Disconected!')
            break
        if data.decode(default_encoding) == 'quit':
            await send_msg('ok'.encode(), loop, client)
            break
        await q.put(data.decode(default_encoding))
    client.close()
    print(f'queue have {q.qsize()}')
    print('close connection')


async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 6000))
    server.listen(8)
    loop = asyncio.get_event_loop()
    print('server run')

    while True:
        client, _ = await loop.sock_accept(server)
        print('new connection')
        loop.create_task(handle_client(client))
        if q.qsize() == 148933:
            print(f'server queue: {q.qsize()}')
            new_list = [int(await q.get()) for _ in range(148933)]
            return sorted(new_list)


def start_server():
    asyncio.run(run_server())


# async def run_server():
#     server = await asyncio.start_server(handle_client, 'localhost', 6000)
#     async with server:
#         await server.wait_closed()
#         if q.qsize() == 148933:
#             server.close()