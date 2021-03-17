from pwn import *
from randcrack import RandCrack
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("challenge.nahamcon.com", 32535))

answer = s.recv(1024)
print answer


rc = RandCrack()
s.send("2\r\n")
num = s.recv(128)
split = num.split()

for i in range(624):
    s.send("2\r\n")
    num = s.recv(128)
    split = num.split()
    print '['+str(i)+'] ' + split[6]
    rc.submit(int(split[6]))

#str(rc.predict_getrandbits(32))

s.send("3\r\n")
print s.recv(128)
s.send(str(rc.predict_getrandbits(32))+'\r\n')
resp = s.recv(1024)
print resp

s.close