import socket

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('challenges.ctfd.io', 30005))

while True:
    # Receive up to 8192 bytes, decode. If issues, += to chunk with while not endswith \n
    chunk = sock.recv(8192).decode('utf-8')

    # Look for end condition (predicted flag)
    if 'UDCTF' in chunk or 'Sorry' in chunk:
        print(chunk)
        break

    # Parse output
    lines = chunk.split('\n')
    all_bytes = lines[2].split('\\')[1:]
    low_bytes, high_bytes = [], []

    # Logic
    for i in all_bytes:
        if i in ['x00', 'x01', 'x02', 'x03', 'x04', 'x05']:
            low_bytes.append(i)
        if i in ['xff', 'xfe', 'xfd', 'xfc', 'xfb', 'xfa']:
            high_bytes.append(i)

    low, high = len(low_bytes), len(high_bytes)

    if low == 7 and high == 1 or high == 7 and low == 1:
        result = 'xor'
    elif low >= 7 and high < 2:
        result = 'and'
    elif high >= 7 and low < 2:
        result = 'or'
    else:
        result = 'xor'

    # Show script progress
    [print(i) for i in lines]
    print(f'Low bytes: {low}\nHigh bytes: {high}\nPrediction: {result}\n')

    # Encode and transfer
    data = result.encode('utf-8') + b'\n'
    sock.send(data)
