from socket import socket

default_header_size = 1
default_pack_size = 6
default_encoding = '866'


async def send_msg(msg: bytes, conn, header_size: int = default_header_size) -> bool:
    # определяем размер сообщения, готовим заголовок
    msg_size = f'{len(msg):{header_size}}'
    # print(conn.write(msg_size.encode(default_encoding)))

    #отправляем заголовок
    conn.write(msg_size.encode(default_encoding))
    await conn.drain()
    conn.write(msg)
    await conn.drain()

    # if conn.write(msg_size.encode(default_encoding)) != header_size:
    #     print(f'ERROR: can\'t send size message')
    #     return False
    # await conn.drain()
    # if conn.write(msg) != len(msg):
    #     print(f'ERROR: can\'t send message')
    #     return False
    # await conn.drain()
    return True


async def recv_msg(loop, conn,
             header_size: int = default_header_size,
             size_pack: int = default_pack_size):
    data = await loop.sock_recv(conn, header_size)
    if not data or len(data) != header_size:
        print(data)
        print('ERROR: can\'t read size message')
        return False

    size_msg = int(data.decode(default_encoding))
    msg = b''

    if size_msg == 0:
        return msg

    while True:
        if size_msg <= size_pack:
            pack = await loop.sock_recv(conn, header_size)
            if not pack:
                return False

            msg += pack
            break

        pack = await loop.sock_recv(conn, header_size)
        if not pack:
            return False

        size_msg -= size_pack
        msg += pack

    return msg