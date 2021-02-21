<p align="center"> ### Tenable CTF, February 2021 documentation ### </p>
<p align="center"> ### Placement: x / x ### </p>


### The only tool you'll ever need (RE, 25p)

It's strings. The only tool you'll ever need is strings. Given a file, a.out, flag is `flag{str1ngs_FTW}`

### Pwntown 1 (RE, 200p)

This is lidl Unity mmorpg. After character creation, we get put onto a map. A section of a map is a sort of a racing corridor. There's a start and finish and you have to run it in less than 5 seconds. The game gives you the flag, flag{*fillthisiniforgotrn*} no matter how slow you are. Not sure if intended. The other challenges require some sort of cheat engine work or reverse engineering the unity game itself.

### Hello ${name} (Code, 25p, Charlie)

### Random Encryption (Code, 100p, Charlie)

They accidentally forgot the flag into the python file... oopsie. `flag{n0t_that_r4ndom}`

### Random Encryption Fixed (Code, 100p)

*add detail*

Given a python script and the output from the run that generated the flag. Using the seeds from that output we can reconstruct the flag, `flag{Oppsie_LULZ_fixed}`

### Short and Sweet (Code, 25p)

### Parsey Mcparser (Code, 50p)

### Easy Stego (Stego, 25p)

png file, different parts of the flag are hidden in different color layers of the image. Easy with stegsolve / stegoveritas. Flag is `flag{...}`

### Hackerman (Stego, 25p)

Challenge provides us a svg file, however examining the file reveals that there's xml inside. The document contains our flag, `flag{...}`.

### A3S Turtles

Challenge presents us a turtles128.zip file. Inside of which is a turtles127.zip file. Yep, it's turtles all the way down. All the zip files are password protected. Initially I just brute forced with zydra, not paying any attention to what the passwords actually were. However, this turns out to be important. All the passwords are either 0 or 1. In the order of unpacking the zips, this gives us a binary string of:

`00111101 11001001 00000110 11110110 10010010 10001110 11101000 10000010 11001100 10110001 10111000 10111101 11010001 01001010 10100010 01001100`. 

Additionally, in the final turtles zip file, there's a key.png, containing hex `ed570e22d458e25734fc08d849961da9`.

Now, a normal person would madke the AES / A3S connection instantly when there was only 9 solves on the challenge. However, I am a bit speshul. Such is life. Binary to hex, `3DC906F6928EE882CCB1B8BDD14AA24C`, then using AES decoder in ECB mode results in the flag, `flag{steg0_a3s}`.

### Esoteric (Misc, 25p)

Some brainfuck to decode, wowee. Flag turns out to be `flag{wtf_is_brainfuck}`.

### Quit messing with my flags (Misc, 25p)

The challenge gives us a modified flag, `flag{161EBD7D45089B3446EE4E0D86DBCF92}`. It's not hex, and it's not base64. Hmmmmm. After applying a lot of smooth brainpower we figure out this could be a reversible md5. And so it is. `flag{P@ssw0rd}`.

### Reggie McRegex (Misc, 25p)

File given is haystack.txt, a literal haystack where we have to find the flag. The text between the curly braces can only have underscores and a-z, as well as having a maximum length of 16. I'm have about 0 experience with regex so this took a little bit of figuring out. Command is `grep -Eo "flag{(.[a-z_]\w{14})}" haystack.txt `, which returns the 1 match, `flag{thy_flag_is_this}`.

### One Byte at a Time (Misc, 50p)

todo

### Find the encoding (Misc, 50p)

We are given a string, `DeZmqMUkDJceycJHJPzZet`. This was quite tricky at first, since it didn't seem to be encoded in anything common. After some struggle with some more exotic encodings, it turns out to be Base58. Flag is `flag{not_base64)`

### Forwards from Grandma (Misc, 100p)

This one is an email file, with an attached image of a comic. For a long time we looked at the image, completely oblivious to the colossal hint in the title of the challenge. FORWARDS from Grandma. The Subject of the email is:

`FWD: FWD: RE: FWD: FWD: RE: FWD: FWD: FWD: RE: RE: RE: FWD: { FWD: FWD: FWD: FWD: RE: RE: FWD: RE: RE: RE: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: RE: RE: FWD: RE: FWD: RE: RE: RE: RE: FWD: RE: FWD: FWD: } THIS IS HILARIOUS AND SO TRUE`

It's even structured in a very obvious way: data{data}. Initially tried binary, but grandma is old school and sent the message in Morse code instead. That's what the double spaces are for, they are the delimiter for the individual bits of morse code. Flag: `flag{I_MISS_AOL}`.

### Broken QR (Misc, 100p)

We are given a QR code that has been drawn over with a white brush, rendering it unreadable. Re created the QR code from scratch in a Google Sheets document, managed to fill in almost all of the corrupted data. This yielded the flag, `flag{d4mn_it_w0nt_sc4n}`.

![output](https://cdn.discordapp.com/attachments/534004815160934410/812408042301423646/broken_qr.png)
![output](https://cdn.discordapp.com/attachments/534004815160934410/812408701125918800/unknown.png)

### We're watching you (OSINT, 75p)

We are given a gif of a Korean singer/personality/something doing peekaboo. Spent over an hour going through all this k-pop stuff. Nothing. Eventually find a tenable blog post about a security vulnerability they found ... titled 'Peekaboo'. Went through a bunch of related pages, eventually found the flag `flag{i_s33_y0u}` on the following page: https://www.tenable.com/security/research/tra-2018-25

### 8 Web Challenges on http://167.71.246.232/ (Fel)

#### Stay Away Creepy Crawlers (25p)

#### Source of All Evil (25p)

#### Can't find it (25p)

#### Show me what you got (25p)

#### Certificate of Authenticity (25p)

#### Headers for your inspiration (25p)

#### Ripper Doc (50p)

#### Protected Directory (50p)

### Classic Crypto (Crypto, 50p, Zenode)

### Easy Peasy (Crypto, 50p, Zenode)

### H4ck3R_m4n exp0sed! 1 (Forensics, 25p, Fel)

### H4ck3R_m4n exp0sed! 2 (Forensics, 25p, Fel)

### H4ck3R_m4n exp0sed! 3 (Forensics, 50p, Fel, me)

fel u write how u got the dataz.

So now we have this pure hex file. Hex > text results in a very familiar JFIF header, encoded in base64. It's an jpg file. Now, because I'm not sure how to properly convert this into an actual image, I had to go with a hack. I replaced the base64 encoded image in the Forwards from Grandma email file with this new file. Then opened the email file in Thunderbird and the image had changed to a rick and morty pic with the flag, `flag{20_minute_adventure}`.

### Knowledge is knowing a tomato is a fruit (Tenable, 25p)

### It's twice as hard (Tenable, 100p)

## Useful Stuff

