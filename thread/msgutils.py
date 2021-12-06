from socket import socket

default_header_size = 10
default_pack_size = 256
default_encoding = '866'


def send_msg(msg: bytes, conn: socket, header_size: int = default_header_size) -> bool:
    # определяем размер сообщения, готовим заголовок
    msg_size = f'{len(msg):{header_size}}'

    # отправляем заголовок
    if conn.send(msg_size.encode(default_encoding)) != header_size:
        print(f'ERROR: can\'t send size message')
        return False

    if conn.send(msg) != len(msg):
        print(f'ERROR: can\'t send message')
        return False

    return True


def recv_msg(conn: socket,
             header_size: int = default_header_size,
             size_pack: int = default_pack_size):
    data = conn.recv(header_size)
    # print(f'receive size:{data}')
    if not data or len(data) != header_size:
        print('ERROR: can\'t read size message')
        return False

    size_msg = int(data.decode(default_encoding))
    msg = b''

    if size_msg == 0:
        return msg

    while True:
        if size_msg <= size_pack:
            pack = conn.recv(size_msg)
            if not pack:
                return False

            msg += pack
            break

        pack = conn.recv(size_pack)
        if not pack:
            return False

        size_msg -= size_pack
        msg += pack

    return msg