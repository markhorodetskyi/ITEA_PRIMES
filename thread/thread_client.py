from queue import Queue
from socket import socket
from time import time
from .msgutils import recv_msg, send_msg, default_encoding
import concurrent.futures as cf
import pickle
from threading import Thread


#  ________QUEUE__________________
# def primes(limit, q: Queue):
#     a = [True] * limit
#     a[0] = a[1] = False
#     for (i, is_prime) in enumerate(a):
#         if is_prime:
#             q.put(str(i))
#             for n in range(i * i, limit, i):
#                 a[n] = False
#
#
# def send_worker(adr: tuple, q):
#     with socket() as sock:
#         sock.connect(adr)
#         while not q.empty():
#             msg = q.get()
#             send_msg(msg.encode(default_encoding), sock)
#
#         send_msg('quit'.encode(), sock)
#         recv_msg(sock)
#         sock.close()
#  _______QUEUE__________________

#  _______HARD DIVIDE RANGE__________________
# def primes(limit):
#     primes_list = []
#     a = [True] * limit
#     a[0] = a[1] = False
#     for (i, is_prime) in enumerate(a):
#         if is_prime:
#             # q.put(str(i))
#             primes_list.append(str(i))
#             for n in range(i * i, limit, i):
#                 a[n] = False
#     return primes_list
#
#
# def send_worker(adr: tuple, q):
#
#     with socket() as sock:
#         sock.connect(adr)
#         for i in q:
#             send_msg(i.encode(default_encoding), sock)
#
#         send_msg('quit'.encode(), sock)
#         recv_msg(sock)
#         sock.close()
#
#
# def divade_to_thread(workers_count: int, primes_list: list):
#     adr = ('localhost', 6000)
#     worker_range = [i for i in range(1, 6+1)]
#     remainder = 148933 % workers_count
#     divade_range = int((148933-remainder)/workers_count)
#     start_index = 0
#     print(divade_range)
#     for worker_number in worker_range:
#         if worker_number != 1:
#             start_index += divade_range
#         end_index = divade_range*worker_number
#         if worker_number == workers_count:
#             end_index = (divade_range * worker_number)+remainder
#             print(end_index)
#         q = primes_list[start_index:end_index]
#         Thread(target=send_worker, args=(adr, q)).start()
#  _______HARD DIVIDE RANGE__________________

def primes(limit):
    primes_list = []
    a = [True] * limit
    a[0] = a[1] = False
    for (i, is_prime) in enumerate(a):
        if is_prime:
            # q.put(str(i))
            primes_list.append(i)
            for n in range(i * i, limit, i):
                a[n] = False
    return primes_list


def send_worker(adr: tuple, q):

    with socket() as sock:
        sock.connect(adr)
        msg = pickle.dumps(q)
        send_msg(msg, sock)
        send_msg('quit'.encode(), sock)
        sock.close()


def run():
    start = time()
    primes_list = primes(2000000)
    # divade_to_thread(6, primes_list)
    adr = ('localhost', 6000)
    print(f'Client have {len(primes_list)} cells')
    send_worker(adr, primes_list)
    print(f'Client time = {time() - start} sec.')
