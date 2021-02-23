<p align="center"> ### Tenable CTF, February 2021 documentation ### </p>
<p align="center"> ### Placement: 148 / 1762 ### </p>
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
- [VIDYA](#vidya)

<br/><br/>

## CODE

### Hello ${name} (25p, Charlie)

Very simple C/C++ script to read a string from stdin and printing out a message with that string.

### Short and Sweet (25p)

Yeah, very basic. Takes in numbers and returns a boolean list whether a number is odd or even.

https://gist.github.com/jp1995/698f773924e75d20772bacdc673abb3c

### Print N Lowest Numbers (25p)

The challenge wants us to write a C/C++ program that takes in some numbers and prints out N lowest numbers. Never did anything with C/C++ before but putting this together in an online shell was fairly simple.

https://gist.github.com/jp1995/677cf4806b67a33e7042eb46e2cb5bfc

### Parsey Mcparser (50p)

The challenge wants us to parse a string, specifically to extract certain parts based on input. Code could probably be better (in retrospect, a lot better) but hey, this works.

https://gist.github.com/jp1995/61368484c7e43ec704b3f9617d7cbd15

### Random Encryption (100p, Charlie)

They accidentally forgot the flag into the python file... oopsie. `flag{n0t_that_r4ndom}`

### Random Encryption Fixed (100p)

Given a python script and the output from the run that generated the flag. The generation is pseudorandom and reversible using the seeds from that output. I tried automating it for a while, then resorted to just manually reconstructing the flag, `flag{Oppsie_LULZ_fixed}`. Good programming exercise for later though.

## STEGANOGRAPHY

### Easy Stego (25p)

png file, different parts of the flag are hidden in different color layers of the image. Easy with stegsolve / stegoveritas. Flag is `flag{Bl4ck_liv3S_MATTER}`.

### Hackerman (25p)

Challenge provides us an svg file, examining the file reveals that there's xml inside. `strings silly_hacker.svg | grep flag` gets us our flag, `flag{microdot}`.

### Secret Images (125p)

We are given two png files. They both appear to be random noise, and none of the standard extraction methods yield any files or data. However, the fact that we are given two files suggests that perhaps we should combine them somehow. Stegsolve has that functionality, and we get the flag, `flag{otp_reuse_fail}`.

### Weird Transmission (175p)

The challenge directs us to the Tenable discord where a bot is playing some wacky space alien robot tunes. The fact that we don't have direct access to the file means that the standard stegano tools will not work, even if we record the audio. Sonic Visualiser showed nothing, but after some googling it turns out that it might be SSTV (Slow Scan Televsion) steganography. One of the tools used to decode SSTV is qsstv. We record the discord bot, which loops every 1m53s, and then pass that audio through pulseaudio to qsstv. As the audio plays the image is decoded, producing our flag, `flag{Noah_th3_s4vi0ur}`.

![output](https://cdn.discordapp.com/attachments/341454782680137728/813155476422131783/S1_20210221_184153.png)

### A3S Turtles (250p)

Challenge presents us a `turtles128.zip` file. Inside of which is a `turtles127.zip` file. Yep, it's turtles all the way down. All the zip files are password protected. Initially I just brute forced with zydra, not paying any attention to what the passwords actually were. However, this turns out to be important. All the passwords are either 0 or 1. In the order of unpacking the zips, this gives us a binary string of:

`00111101 11001001 00000110 11110110 10010010 10001110 11101000 10000010 11001100 10110001 10111000 10111101 11010001 01001010 10100010 01001100`. 

Additionally, in the final turtles zip file, there's a key.png, containing hex `ed570e22d458e25734fc08d849961da9`.

Now, a normal person would madke the AES / A3S connection instantly when there was only 9 solves on the challenge. However, I am a bit speshul. Such is life. Binary to hex, `3DC906F6928EE882CCB1B8BDD14AA24C`, then using AES decoder in ECB mode results in the flag, `flag{steg0_a3s}`.

## MISC

### Esoteric (25p)

Some brainfuck to decode, wowee. Flag turns out to be `flag{wtf_is_brainfuck}`.

### Quit messing with my flags (25p)

The challenge gives us a modified flag, `flag{161EBD7D45089B3446EE4E0D86DBCF92}`. It's not hex, and it's not base64. Hmmmmm. After applying a lot of smooth brainpower we figure out this could be a reversible md5. And so it is. `flag{P@ssw0rd}`.

### Reggie McRegex (25p)

File given is haystack.txt, a literal haystack where we have to find the flag. The text between the curly braces can only have underscores and a-z, as well as having a maximum length of 16. I have about 0 experience with regex so this took a little bit of figuring out. Command is `grep -Eo "flag{(.[a-z_]\w{14})}" haystack.txt `, which returns the 1 match, `flag{thy_flag_is_this}`.

### One Byte at a Time (50p)

We are told to netcat to a host that asks us how much of the flag we know and promises to help with the rest. So if we enter the first n chars of the flag correctly, we are told it's correct. Additionally, `XORing the next flag character with a random octet taken from some unknown IPv4 address I have... 0x76`. The host seemed to have a very unstable connection, perhaps intentionally to prohibit automatic bruteforcing. However, it was easy enough to manually brute force and completely avoid the XOR logic. Flag is `flag{f0ll0w_th3_whit3_r@bb1t}`. Gonna try to figure out the logic after the CTF.

### Find the encoding (50p)

We are given a string, `DeZmqMUkDJceycJHJPzZet`. This was quite tricky at first, since it didn't seem to be encoded in anything common. After some struggle with some more exotic encodings, it turns out to be Base58. Flag is `flag{not_base64)`.

### Forwards from Grandma (100p, Zenode)

This one is an email file, with an attached image of a comic. For a long time we looked at the image, completely oblivious to the colossal hint in the title of the challenge. FORWARDS from Grandma. The Subject of the email is:

`FWD: FWD: RE: FWD: FWD: RE: FWD: FWD: FWD: RE: RE: RE: FWD: { FWD: FWD: FWD: FWD: RE: RE: FWD: RE: RE: RE: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: FWD: RE: RE: FWD: RE: FWD: RE: RE: RE: RE: FWD: RE: FWD: FWD: } THIS IS HILARIOUS AND SO TRUE`

It's even structured in a very obvious way: data{data}. Initially tried binary, but grandma is old school and sent the message in Morse code instead. That's what the double spaces are for, they are the delimiter for the individual bits of morse code. Flag: `flag{I_MISS_AOL}`.

### Broken QR (100p)

We are given a QR code that has been drawn over with a white brush, rendering it unreadable. Re created the QR code from scratch in a Google Sheets document, managed to fill in almost all of the corrupted data. This yielded the flag, `flag{d4mn_it_w0nt_sc4n}`.

![output](https://cdn.discordapp.com/attachments/534004815160934410/812408042301423646/broken_qr.png)
![output](https://cdn.discordapp.com/attachments/534004815160934410/812408701125918800/unknown.png)

## Web

### SpringMVC 1-6 (25p each)

The challenge gave us the source code to the website, and asked us to generate precise requests to get flags. 3 Files in the source code basically told you exactly what to do in order to receive the flag. Using Postman to make these requests.

1. Generate get request to /main subdirectory, flag, `flag{flag1_517d74}`.
2. Post request to /main subdirectory, passing the parameter `magicWord` with any value. Flag `flag{flag2_de3981}`.
3. Post request to /main subdirectory, passing the parameter `magicWord` with the value `please`. Flag `flag{flag3_0d431e}`.
4. Post request to /main subdirectory. Hint is JSON, so Content-Type: `multipart/form-data` and also a header Content-Type with value `application/json`. Flag `flag{flag4_695954}`.
5. Options request to /main subdirectory, flag `flag{flag5_70102b}`.
6. Get request to /main subdirectory, with a header Magic-Word with the value `please`. Flag `flag{flag6_ca1ddf}`.

### 25p Challs targeting `http://167.71.246.232` RipperDoc site

- Stay Away Creepy Crawlers (Charlie): There's a file called robots.txt, which has our flag, `flag{mr_roboto}`.
- Source of All Evil (Charlie): Flag is in the HTML of the main page, `<!-- source flag : flag{best_implants_ever} -->`.
- Can't find it (Charlie): The 404 page has our flag, `flag{404_oh_no}`.
- Show me what you got (Charlie): An image on the site is located in the /images directory. There's also a text file, containing our flag, `flag{disable_directory_indexes}`.
- Certificate of Authenticity (Fel): Connecting to the site with HTTPS lets us see the hand crafted certificate, which frightens our browser so. Flag is in there, `flag{selfsignedcert}`.
- Headers for your inspiration: Network tab in devtools allows us to see Headers, which contain our flag, `flag{headersftw}`.

### Ripper Doc (50p, Fel)

The site has a `certified rippers` page but we cannot access it as we are not authenticated. After some searching in devtools, it turns out that authentication is done with a cookie, and after changing it's value and reloading, we get our flag, `flag{messing_with_cookies}`.

### Protected Directory (50p, Fel)

Looking for common files and subdirectories, we discover the `/admin` location and the`.htpasswd` file, which contains the admin login, as well as an encrypted password, `$apr1$1U8G15kK$tr9xPqBn68moYoH4atbg20`. This is md5 and can be cracked very fast with your faviourte tool for that. Password turns out to be `alesh16` and after logging in we get our flag, `flag{cracked_the_password}`.

## RE

### The only tool you'll ever need (25p)

It's strings. The only tool you'll ever need is strings. Given a file, a.out, flag is `flag{str1ngs_FTW}`

### Pwntown 1 (200p)

This is lidl Unity mmorpg. After character creation, we get put onto a map. A section of a map is a sort of a racing corridor. There's a start and finish and you have to run it in less than 5 seconds. The game gives you the flag, `flag{th3_amazinng_r4c3}` no matter how slow you are. Not sure if intended. The other challenges require some sort of cheat engine work.

## CRYPTO

### Classic Crypto (50p, Zenode)

The challenge provides a ciphered text. It's none of the rot ciphers, but it looks awfully like it, so it should be vigenere. This means the key has to be guessed, and has to therefore be relatively easy to guess. Anonymous works, and we get our flag, `flag{classicvigenere}`.

### Easy Peasy (50p, Zenode)

We are given a string that looks awfully like base64. Decoding that yields some hex, decoding that gives us a flag but it's ciphered. Rot13 works. Easy Peasy. Flag: `flag{congrats_you_got_me}`.

## FORENSICS

### H4ck3R_m4n exp0sed! 1 (25p, Fel)

We are given a packet capture file that is also used for the other 2 hackerman challenges. Using wireshark, following the TCP stream we find some interesting information. There's a user/pass pair of `h4ckerm4n/hunter2`, as well as files `supersecure.7z`, `compression_info.txt` and `butter.jpg`. Stream 6 contains the .7z file, we can save the data as RAW. Stream 8 tells us that the password for the compressed file is `bbqsauce`. Stream 10 contains the JPG file, which we can also save.

The butter.jpg image has the flag for the first part, `flag{u_p4ss_butt3r}`.

### H4ck3R_m4n exp0sed! 2 (25p, Fel)

The flag for the second part is inside the .7z file, in an image called ... pickle_nick.png. `flag{pickl3_)NIIICK}`.

![output](https://cdn.discordapp.com/attachments/534004815160934410/813743671534026773/pickle_nick.png)

### H4ck3R_m4n exp0sed! 3 (50p, Fel, me)

The 7z file mentioned in the previous part also contains a pure hex file called `dataz`.

Hex > text results in a very familiar JFIF header, encoded in base64. It's a jpg file. Now, because I wasn't sure how to properly convert this into an actual image, I had to go with a hack. I replaced the base64 encoded image in the Forwards from Grandma email file with this new file, also base64 encoded. Then opened the email file, which was formatted to decode a base64 encoded image, in Thunderbird and the image had changed to a rick and morty pic with the flag, `flag{20_minute_adventure}`. Scuffed, yes.

## TENABLE

### Knowledge is knowing a tomato is a fruit (25p)

These challenges were based on the product of the organizer, challenge gave a scan file which was loaded into the software. Basically it's a a report of a cybersecurity scan which lists all vulnerabilities the system it was run on had. The flags were hidden throughout this report. This particular flag, `flag{bu7 n07 putt1ng 1t 1n 4 fru17 s@l4d, th@t5 W1SD0M}`, was in the bottom of the host details file for the `172.26.48.53` machine.

### It's twice as hard (100p)

Flag file was found in the Debugging Log Report on the `.53` machine, which listed 106 log files in total. The flag was in the bottom of the get_flag.log file, not directly, but as a command, ``session.ssh_cmd_wrapper: Ran command: "cat /tmp/flag | xxd -p"`` and output: `Returned: 2e2e2e2e2e2e2e2e2e2e ... etc`. xxd -r -p on the output yields our flag, `flag{Pr0gr4mm1ng Mu57 83 7h3 Pr0c355 0f Putt1ng 7h3m 1n}`

## VIDYA

### Play me (200p)

We are given a .gb file. Quick google suggests it's a gameboy file. Installing an emulator (Visual Boy Advance) and getting the game to run is a quick 2 minute process on Windows. The game turns out to be a kind of a boshy style platformer. It might actually be playable, but hacking it seemed quicker. I was initially going to use cheat engine, but it turns out this emulator has similar functionality built right in.

We can look at the memory, live, and find values that change as we move around the map. Doesn't take long to find the memory address storing x and y coordinates. Knowing this memory address, it is now possible to create a cheat, and change the value of the x coordinate to move us further along on the map. This effectively teleports you. After about 3 increments, the character gets placed on the end screen, which displays our flag, `flag{pixels}`.

## OSINT

### We're watching you (75p)

We are given a gif of a Korean singer/personality/something doing peekaboo. Spent over an hour going through all this k-pop stuff. Nothing. Eventually find a tenable blog post about a security vulnerability they found ... titled 'Peekaboo'. Went through a bunch of related pages, eventually found the flag `flag{i_s33_y0u}` on the following page: https://www.tenable.com/security/research/tra-2018-25

## Useful Stuff

### Alternative curl commands for making requests:
```
curl "http://challenges.ctfd.io:30542/main"
curl -X POST "http://challenges.ctfd.io:30542/main"
curl -d "magicWord=please" -X POST "http://challenges.ctfd.io:30542/main"
curl -H "Content-Type: application/json" -X POST "http://challenges.ctfd.io:30542/main"
curl -X OPTIONS "http://challenges.ctfd.io:30542/main"
curl -H "Magic-Word: please" -X GET "http://challenges.ctfd.io:30542/main"
curl "http://challenges.ctfd.io:30542/?name=please"
```
