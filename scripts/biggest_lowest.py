import socket
import re

hostname = 'challs.xmas.htsp.ro'
port 6051

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(hostname, port)

while True:
    # Set initial chunk size, make sure to keep collecting until server stops sending
    chunk = sock.recv(8192)
    while not chunk.endswith(b'\n'):
        chunk += sock.recv(1000)
    
    # Look for end condition (predicted flag)
    if 'X-MAS' in chunk.decode('utf-8'):    
        print(chunk.decode('utf-8'))
        break
    
    # Parse output
    lines = [chunk.decode('ascii').split('\n')]
    flat_lines = [item for sublist in lines for item in sublist]
    
    # Show scripts progress
    for i in flat_lines:
        print(i)
        
    # Get our variables
    re_array = re.search('\\[(.*?)]', chunk.decode('utf-8')
    expression_array = re_array.group(0)
    re_k1 = re.search('(?<=k1\\s=)(.*)', chunk.decode('utf-8')
    expression_k1 = re_k1.group(1)
    re_k2 = re.search('(?<=k2\\s=)(.*)', chunk.decode('utf-8')
    expression_k2 = re_k2.group(1)
    
    array = eval(expression_array)
    k1 = eval(expression_k1)
    k2 = eval(expression_k2)
    
    # Do the math
    array_sorted = sorted(array)
    array_sorted_reverse = sorted(array, reverse=True)
    yeet = str(array_sorted[:int(k1)]) + "; " + str(array_sorted_reverse[:int(k2)])
    result = yeet.replace('[', '').replace(']', '')
    
    # Encode and transfer
    data = str(result).encode('utf-8') + b'\n'
    sock.send(data)
