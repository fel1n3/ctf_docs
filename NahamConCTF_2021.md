<p align="center"> ### NahamCon CTF, March 2021 documentation ### </p>
<p align="center"> ### Placement: 261 / 3418 ### </p>
<br/><br/>

- [WARMUP](#warmup)
- [MISC](#misc)
- [WEB](#web)
- [RE](#re)
- [CRYPTO](#crypto)
- [FORENSICS](#forensics)
- [MISSION](#mission)
- [RECON](#recon)

<br/><br/>

## WARMUP

### Read the rules

Given a link ot the rules, flag in HTML comment.

### Shoelaces

Given an image, running strings | grep flag on it yields our flag. Overall extremely easy and kind of disappointing stego challenges.

### Pollex (Zenode)

Looking at the given image closely, we can see writing in the thumbnail. Extracting thumbnail with `exiftool -b -Thumbnailimage pollex > pollex_thumbnail`, got flag.

### Chicken Wings

This one puzzled us for the longest time. The given file contained a bunch of emoji symbols. Eventually I just put the whole emoji string into google and the first result was ... WingDing Translator. it werkd.

### Eighth Circle

Challenge provides a text file with a long line of seemingly garbage text. Googling `Eighth Circle` leads us to Dante's Inferno, where the eighth circle of hell was named Malebolge. Incidentally, there's also an esoteric programming language called Malbolge. Using an online Malbolge interpreter, we can run the given code which returns our flag.

### esab64 (Zenode)

Filename is base64 backwards. Reversed the string inside, decoded with base64, then reversed that to get flag.

### Veebee (Zenode)

Visual Basic script. Flag could be found by just running it.

### Car Keys (Zenode)

Substitution cipher with a key. Initially tried Vigenere, then keyed Caesar cipher with QWERTY as key.

### Buzz

Challenge provides a file called buzz, of type compress'd data 16 bits. Renaming the file to buzz.z and then uncompressing it with the uncompress command yields the flag.

## MISC

### Abyss

netcat into a host that spams untold amount of garbage. Let that run for a minute and piped everything into a text file. `cat file | grep flag` yielded the flag.

## Web

### $Echo

The challenge directs us to a simple Echo website, where the site echos your input back at you. We can access the underlying debian system by passing commands surrounded by backticks, but there is still another issue. The input validation has a length check of 15 and bans most non-letter characters.

The flag is in the parent directory, but we can't change directory. Initally I tried `cat ../flag.txt` but this exceeded the lenght limit by two characters. Eventually, with some help, I got the flag with `< ..flag.txt`, however that works.

### Homeward Bound (Fel)

Upon loading the webpage i notice the notice given states something along the lines of 'you must be on the local network' or something, so I simply used Zap
to edit and add the 'X-Forwarded-For:' header and set it to 127.0.0.1. This yielded me the flag.

## RE

### Ret2Basic (Fel)

From quickly playing around with it I notice that it's obviously a buffer overflow thing, so I load the binary in gdb and first find the address of the flag to be `0x401215` and named win. Then using the pattern tool I find the offset to be 120 bytes, which I simply passed to the remote binary using inline python `python -c 'print "A"*120+"\x15\x12\x40\x00\x00\x00\x00\x00"'` and obtained the flag.

## CRYPTO

### Dice Roll (Fel)

Given a python script, after a quick glance notice that the script is using getrandbits, a pseudo rng. After a quick search I found a library named randcrack, that given enough values discovered the internal state of the generator (https://pypi.org/project/randcrack/). Using this I quickly wrote a script that queried the server a bunch of times and obtained the flag.

## FORENSICS

### Parseltongue

We are given a byte-compiled python file. From an earlier CTF I know that uncompyle6 can be used to render this file human readable and usable. Done. Now we have a python file that has a lot of obfuscation and seems to use random to generate the flag.

The script is formatted terribly, variable names are ss, sss, z, zz, zs, sz etc to overall make it as confusing as possible. Slowly working through and simplifying it I realise that random component is completely unnecessary. The flag is hard coded into the python script and easy to get after all this simplification.

### Henpeck (Zenode)

After being given the Henpeck file, I opened the file in wireshark to see have a quick look, I noticed that some of the packets had URB_INTERRUPT in which generally means that a key is being pressed or mouse is being used. I had a quick glance at the data in the "Leftover Capture Data" segment and noticed two bits changing. Comparing this to an online table you can see that these bits correspond to key presses.

So I extracted the data using `tshark -r ./henpeck.pcap -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata | sed 's/../:&/g2' > output`

Once extracted I then ran a python script found at https://github.com/TeamRocketIst/ctf-usb-keyboard-parser to parse the information into readable text using `python3 usbkeyboard.py output` which resulted in the flag.

## MISSION

### Bionic (Fel)

The initial Mission challenge. Simply checked robots.txt on constellations.page and found the flag.

### Meet the Team

robots.txt directs us to a different page, constellations.page/meet-the-team.html. Sadly we are too late, the content of the page has been redacted due to security reasons. However, when inspecting the page, we get an important clue.

`<!-- Vela, can we please stop sharing our version control software out on the public internet? -->`

There is a link to the organizations github page in the footer but there's nothing there. There is also a .git/ subdirectory but it appears to be private. After a bit of searching we find https://github.com/internetwache/GitTools. Used the dumper script to grab the contents of the constellations.page/.git and then the extractor script to turn that dump into readable files.

Now we have 6 folders, each of which is a commit with all the relevant files and metadata. One of the commits contains an older version of the page with the full list of employee names, as well as the flag for this challenge.

Orion Morra — Support

Lyra Patte — Marketing

Leo Rison — Development

Gemini Coley — Operations

Hercules Scoxland — Sales

Vela Leray — Management

Pavo Welly — HR

Gus Rodry — Accounting

Now we have a the employee names, and most of them have their own challenges.

### Gus

I noticed Gus' github account linked to the constellations organization github page. Gus has a repo called development. Going through the files, I notice that every line in the .gitignore file has a typo, ie `.sh/id_rsa` instead of `.ssh/id_rsa`. Sure enough going through the config folder there is a .ssh folder and inside we find the flag for this challenge, as well as a rsa public and private key.

### Lyra

Googling Lyra Patte gives us her twitter. Looks like she did an oopsie by sharing an internal URL (constellations.page/constellations-documents/1/) on her twitter page. Going through the numbered directories, /5/ reveals account names and passwords for the site, as well as the flag for this challenge.

### Hercules

Checking Gus' followers on github, most of them are ctf solvers following for fun, but we do see Hercules Scoxland there. In one of his repo's we find the flag for this challenge, as well as some ssh details.

### Hydraulic

We have to ssh into a machine, but we are given no credentials. There is the username / password list we got from Lyra though. Trying a couple combinations yields nothing, and this should be automated. Putting the usernames and passwords into their own files, then passing those files to hydra to brute force the solution.

And as it turns out somebody didn't change their default password and that someone was Pavo. Flag is in the home directory.

### Leo

Googling Leo Rison gets very little, there is someone with that name on Instagram though. So, time to make a fake instagram account I suppose. This process was extremely annoying. In the end, that Leo wasn't even the right guy. However searching for Leo Rison inside instagram yields another account, which is in fact the one we're looking for. One of his posts has a QR code and scanning it gets us our flag.

### Orion

Searching Orion Morra gets nothing relevant. Searching "Orion Morra" just yields a bunch of porn. Eventually I think to search that handle on various social media sites directly, and indeed twitter.com/orionmorra is legit. Flag is hand written in a picture.

## RECON

### Hackthebox

This was a recon challenge to find the flag on HackTheBox's online presence. I'm not sure if they forgot to post the flag or if it was meant to be this delayed, but with less than 2 hours left they posted the second half of the flag in one of their discord channels. I quickly found the first part on their twitter. A lot of points for very little work.

## Useful Stuff

https://github.com/TeamRocketIst/ctf-usb-keyboard-parser

https://github.com/WangYihang/UsbKeyboardDataHacker

https://aur.archlinux.org/packages/android-apktool/ and jadx and jadx-gui for decompiling .apk

https://github.com/volatilityfoundation/volatility to analyze dump files. https://github.com/ryan-cd/ctf/tree/master/2021/nahamcon/forensics/typewriter






