<p align="center"> ### Tenable CTF, February 2021 documentation ### </p>
<p align="center"> ### Placement: x / x ### </p>
<br/><br/>

- [CODE](#code)
- [STEGANOGRAPHY](#steganography)
- [MISC](#misc)
- [Web](#web)
- [RE](#re)
- [CRYPTO](#crypto)
- [FORENSICS](#forensics)
- [TENABLE](#tenable)
- [OSINT](#osint)

<br/><br/>

## CODE
============

### Hello ${name} (25p, Charlie)

### Short and Sweet (25p)

Yeah, very basic. Takes in numbers and returns a boolean list whether number is odd or even.

https://gist.github.com/jp1995/698f773924e75d20772bacdc673abb3c

### Print N Lowest Numbers (25p)

The challenge wants us to write a C/C++ program that takes in some numbers and prints out N lowest numbers. Never did anything with C/C++ before but putting this together in an online shell was fairly simple.

https://gist.github.com/jp1995/677cf4806b67a33e7042eb46e2cb5bfc

### Parsey Mcparser (50p)

The challenge wants us to parse a string, specifically to extract certain parts based on input. Code could probably be better but hey, this works.

https://gist.github.com/jp1995/61368484c7e43ec704b3f9617d7cbd15

### Random Encryption (100p, Charlie)

They accidentally forgot the flag into the python file... oopsie. `flag{n0t_that_r4ndom}`

### Random Encryption Fixed (100p)

*add detail*

Given a python script and the output from the run that generated the flag. Using the seeds from that output we can reconstruct the flag, `flag{Oppsie_LULZ_fixed}`

## STEGANOGRAPHY
============

### Easy Stego (25p)

png file, different parts of the flag are hidden in different color layers of the image. Easy with stegsolve / stegoveritas. Flag is `flag{...}`

### Hackerman (25p)

Challenge provides us a svg file, however examining the file reveals that there's xml inside. The document contains our flag, `flag{...}`.

### Weird Transmission (175p)

The challenge directs us to the Tenable discord where a bot is playing some wacky space alien robot tunes. The fact that we don't have direct access to the file suggests that the standard stegano tools will not work. After some googling it turns out that it might be SSTV (Slow Scan Televsion) steganography. One of the tools used to decode SSTV is qsstv. We record the discord bot, which loops every 1m53s, and then pass that audio through pulseaudio to qsstv. This slowly decodes the signal, producing the image with our flag, `flag{Noah_th3_s4vi0ur}`.

![output](https://cdn.discordapp.com/attachments/341454782680137728/813155476422131783/S1_20210221_184153.png)

### A3S Turtles (250p)

Challenge presents us a turtles128.zip file. Inside of which is a turtles127.zip file. Yep, it's turtles all the way down. All the zip files are password protected. Initially I just brute forced with zydra, not paying any attention to what the passwords actually were. However, this turns out to be important. All the passwords are either 0 or 1. In the order of unpacking the zips, this gives us a binary string of:

`00111101 11001001 00000110 11110110 10010010 10001110 11101000 10000010 11001100 10110001 10111000 10111101 11010001 01001010 10100010 01001100`. 

Additionally, in the final turtles zip file, there's a key.png, containing hex `ed570e22d458e25734fc08d849961da9`.

Now, a normal person would madke the AES / A3S connection instantly when there was only 9 solves on the challenge. However, I am a bit speshul. Such is life. Binary to hex, `3DC906F6928EE882CCB1B8BDD14AA24C`, then using AES decoder in ECB mode results in the flag, `flag{steg0_a3s}`.

## MISC
============

### Esoteric (25p)

Some brainfuck to decode, wowee. Flag turns out to be `flag{wtf_is_brainfuck}`.

### Quit messing with my flags (25p)

The challenge gives us a modified flag, `flag{161EBD7D45089B3446EE4E0D86DBCF92}`. It's not hex, and it's not base64. Hmmmmm. After applying a lot of smooth brainpower we figure out this could be a reversible md5. And so it is. `flag{P@ssw0rd}`.

### Reggie McRegex (25p)

File given is haystack.txt, a literal haystack where we have to find the flag. The text between the curly braces can only have underscores and a-z, as well as having a maximum length of 16. I'm have about 0 experience with regex so this took a little bit of figuring out. Command is `grep -Eo "flag{(.[a-z_]\w{14})}" haystack.txt `, which returns the 1 match, `flag{thy_flag_is_this}`.

### One Byte at a Time (50p)

todo

### Find the encoding (50p)

We are given a string, `DeZmqMUkDJceycJHJPzZet`. This was quite tricky at first, since it didn't seem to be encoded in anything common. After some struggle with some more exotic encodings, it turns out to be Base58. Flag is `flag{not_base64)`

### Forwards from Grandma (100p)

This one is an email file, with an attached image of a comic. For a long time we looked at the image, completely oblivious to the colossal hint in the title of the challenge. FORWARDS from Grandma. The Subject of the email is:

`FWD: FWD: RE: FWD: FWD: RE: FWD: FWD: FWD: RE: RE: RE: FWD: { FWD: FWD: FWD: FWD: RE: RE: FWD: RE: RE: RE: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: RE: RE: FWD: RE: FWD: RE: RE: RE: RE: FWD: RE: FWD: FWD: } THIS IS HILARIOUS AND SO TRUE`

It's even structured in a very obvious way: data{data}. Initially tried binary, but grandma is old school and sent the message in Morse code instead. That's what the double spaces are for, they are the delimiter for the individual bits of morse code. Flag: `flag{I_MISS_AOL}`.

### Broken QR (100p)

We are given a QR code that has been drawn over with a white brush, rendering it unreadable. Re created the QR code from scratch in a Google Sheets document, managed to fill in almost all of the corrupted data. This yielded the flag, `flag{d4mn_it_w0nt_sc4n}`.

![output](https://cdn.discordapp.com/attachments/534004815160934410/812408042301423646/broken_qr.png)
![output](https://cdn.discordapp.com/attachments/534004815160934410/812408701125918800/unknown.png)

## Web
============

#### Stay Away Creepy Crawlers (25p)

#### Source of All Evil (25p)

#### Can't find it (25p)

#### Show me what you got (25p)

#### Certificate of Authenticity (25p)

#### Headers for your inspiration (25p)

#### Ripper Doc (50p)

#### Protected Directory (50p)

## RE
============

### The only tool you'll ever need (25p)

It's strings. The only tool you'll ever need is strings. Given a file, a.out, flag is `flag{str1ngs_FTW}`

### Pwntown 1 (200p)

This is lidl Unity mmorpg. After character creation, we get put onto a map. A section of a map is a sort of a racing corridor. There's a start and finish and you have to run it in less than 5 seconds. The game gives you the flag, flag{*fillthisiniforgotrn*} no matter how slow you are. Not sure if intended. The other challenges require some sort of cheat engine work or reverse engineering the unity game itself.

## CRYPTO
============

### Classic Crypto (50p, Zenode)

### Easy Peasy (50p, Zenode)

## FORENSICS
============

### H4ck3R_m4n exp0sed! 1 (25p, Fel)

### H4ck3R_m4n exp0sed! 2 (25p, Fel)

### H4ck3R_m4n exp0sed! 3 (50p, Fel, me)

fel u write how u got the dataz.

So now we have this pure hex file. Hex > text results in a very familiar JFIF header, encoded in base64. It's an jpg file. Now, because I'm not sure how to properly convert this into an actual image, I had to go with a hack. I replaced the base64 encoded image in the Forwards from Grandma email file with this new file. Then opened the email file in Thunderbird and the image had changed to a rick and morty pic with the flag, `flag{20_minute_adventure}`.

## TENABLE
============

### Knowledge is knowing a tomato is a fruit (25p)

### It's twice as hard (100p)

## OSINT
============

### We're watching you (75p)

We are given a gif of a Korean singer/personality/something doing peekaboo. Spent over an hour going through all this k-pop stuff. Nothing. Eventually find a tenable blog post about a security vulnerability they found ... titled 'Peekaboo'. Went through a bunch of related pages, eventually found the flag `flag{i_s33_y0u}` on the following page: https://www.tenable.com/security/research/tra-2018-25

## Useful Stuff

