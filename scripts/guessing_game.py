import socket

hostname = 'challenges.ctfd.io'
port = 30005

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((hostname, port))

while True:
    # Set initial chunk size, make sure to keep collecting until server stops sending
    chunk = sock.recv(8192)
    while not chunk.endswith(b'\n'):
        chunk += sock.recv(1000)

    # Look for end condition (predicted flag)
    if 'UDCTF' in chunk.decode('utf-8'):
        print(chunk.decode('utf-8'))
        break

    # Parse output
    lines = [chunk.decode('ascii').split('\n')]
    flat_lines = [item for sublist in lines for item in sublist]

    # Logic
    bytes = flat_lines[2].split('\\')[1:]
    low_bytes = []
    high_bytes = []

    for i in bytes:
        if i in ['x00', 'x01', 'x02', 'x03', 'x04', 'x05']:
            low_bytes.append(i)
        if i in ['xff', 'xfe', 'xfd', 'xfc', 'xfb', 'xfa']:
            high_bytes.append(i)

    low = len(low_bytes)
    high = len(high_bytes)

    if low == 7 and high == 1 or high == 7 and low == 1:
        result = 'xor'
    elif low >= 7 and high < 2:
        result = 'and'
    elif high >= 7 and low < 2:
        result = 'or'
    else:
        result = 'xor'

    # Show script progress
    for i in flat_lines:
        print(i)
    print(f'Low bytes: {low}\nHigh bytes: {high}\nPrediction: {result}\n')

    # Encode and transfer
    data = str(result).encode('utf-8') + b'\n'
    sock.send(data)
