import socket
import re

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('178.62.70.150', 31955))
sock.settimeout(2)
iteration = 0

while True:
    iteration += 1
    print('\n')

    # Receive up to 8192 bytes, decode. Make sure server has stopped sending.
    chunk = sock.recv(8192).decode('utf-8')
    while not chunk.endswith(('> ', 'Answer: ')):
        try:
            chunk += sock.recv(1000).decode('utf-8')
        except socket.timeout:
            break

    # Look for end condition (predicted flag)
    if 'CHTB' in chunk:
        print(chunk)
        break

    # Parse output
    lines = chunk.split('\n')
    lines = [i for i in lines if i]

    # Show script progress
    [print(i) for i in lines]

    # Logic
    if iteration == 1:
        data = "1".encode('utf-8') + b'\n'
        sock.send(data)
    elif iteration == 2:
        dictionary = {}
        elements = lines[1].replace(' -> ', '->')
        elements_list = re.split(r'\s', elements)[:-1]

        for i in elements_list:
            key, value = i.split('->')[0], i.split('->')[1]
            dictionary[key] = value

        data = "2".encode('utf-8') + b'\n'
        sock.send(data)
    else:
        if iteration == 3:
            equation = lines[2].split('  = ')[0]
        else:
            equation = lines[3].split('  = ')[0]

        for key, value in dictionary.items():
            equation = equation.replace(key, value)

        result = str(eval(equation))
        print(f'{equation} = {result}')

        data = result.encode('utf-8') + b'\n'
        sock.send(data)
