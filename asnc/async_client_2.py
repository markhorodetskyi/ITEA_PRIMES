import asyncio
from socket import socket
from asyncio import Queue, Protocol
from asnc.async_msgutils import send_msg, default_encoding, recv_msg


async def primes(limit, q: Queue):
    print('im working')
    a = [True] * limit
    a[0] = a[1] = False
    for (i, is_prime) in enumerate(a):
        if is_prime:
            await q.put(str(i))
            for n in range(i*i, limit, i):     # Mark factors non-prime
                a[n] = False


async def send_worker(q):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 6000)
    while not q.empty():
        msg = await q.get()
        await send_msg(msg.encode(default_encoding), writer)
    await send_msg('quit'.encode(default_encoding), writer)
    await recv_msg(reader)
    print('Close the connection')
    writer.close()
    await writer.wait_closed()


def run():
    q = Queue()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(primes(2000000, q))
    print(f'queue have {q.qsize()} cells')
    adr = ('localhost', 6000)
    with socket() as sock:
        tasks = [
            send_worker(q),
        ]
        loop.run_until_complete(asyncio.wait(tasks))



