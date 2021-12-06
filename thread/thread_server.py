from threading import Thread
from socket import socket
from math import floor, sqrt
from multiprocessing import Pool
import pickle

from .msgutils import recv_msg, send_msg, default_encoding


def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sq = int(floor(sqrt(n)))
    for i in range(3, sq + 1, 2):
        if n % i == 0:
            return False
    return True

class ClientHandler(Thread):
    def __init__(self, conn: socket):
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        while True:
            data = recv_msg(self.conn)
            if not data:
                print('not data. Disconected!')
                break
            if data.decode(default_encoding) == 'quit':
                send_msg('ok'.encode(default_encoding), self.conn)
                break
            return pickle.loads(data)
        print(f'queue have {len(data)}')


def start_server(workers):
    adr = ('localhost', 6000)
    with socket() as sock:
        sock.bind(adr)
        sock.listen(6)
        while True:
            conn, _ = sock.accept()
            client = ClientHandler(conn)
            data = client.run()
            if data and len(data) == 148933:
                print(f'Server have: {len(data)} cells')
                pool = Pool(workers)
                if False in pool.map(is_prime, data):
                    print('Fail')
                else:
                    with open('primes.txt', 'w') as f:
                        f.write('\n'.join(str(i) for i in data))
                return data




