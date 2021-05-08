import socket
import math
import re
from time import sleep


def isPerfectSquare(x):
    s = int(math.sqrt(x))
    return s * s == x


def isFibonacci(n):
    return isPerfectSquare(5 * n * n + 4) or isPerfectSquare(5 * n * n - 4)


# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('umbccd.io', 6000))
iteration = 0

while True:
    if iteration == 0:
        chunk = sock.recv(8192).decode('utf-8')
        while not chunk.endswith(('\n', ']')):
            try:
                chunk += sock.recv(1024).decode('utf-8')
            except socket.timeout:
                break
    else:
        chunk = sock.recv(1024).decode('utf-8')

    if 'DawgCTF' in chunk:
        print(chunk)
        break

    # Parse output
    lines = chunk.split('\n')
    lines = [i for i in lines if i]

    # Show script progress
    [print(i) for i in lines]

    numbers = re.findall(r'\[(.*?)]', chunk)

    test = numbers[0].split(', ')
    int_map = map(int, test)
    int_list = list(int_map)
    for x in int_list:
        if isFibonacci(x):
            result = str(x)
            print(result)
            data = result.encode('utf-8') + b'\n'
            sock.send(data)
            print('data sent')
            sleep(0.5)

    iteration += 1