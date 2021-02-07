<p align="center"> ### TrollCatCTF, February 2021 documentation ### </p>
<p align="center"> ### Placement: 33 / 355 ### </p>

### Deal breaking (Zenode)

Was given a ciphertext of `cnenprgnzbysbeurnqnpur`. The challenge description mentioned '$13 million', which made me think it was a Rot13 Cipher. I put it through a rot13 decrypt and got the flag, `Trollcat{paracetamolforheadache}`.

### Lost in forest (Zenode)

Was given a ciphertext of `TWVyY3VyeVZlbnVzRWFydGhNYXJzSnVwaXRlclNhdHVyblVyYW51c05lcHR1bmU`. The challenge description mentioned 64, which made me think of Base64. I put it through a Base64 decrypt and retrieved the flag, `Trollcat{MercuryVenusEarthMarsJupiterSaturnUranusNeptune}`.

### Show your dedication (Zenode)

Was given a ciphertext of `powv wlck zs JICLQaFRNH`. The challenge description had a clue, 'KEY is RACE', so I thought a vigenere cipher would be the way to go. I put it through a decrypt and came up with `your flag is HELLOwORLD`. Final flag, `Trollcat{HELLOWORLD}`.

### Ciphers are fun

We are given QR code, which leads to a password protected pastebin. We are meant to guess this password. This is never fun. Anyway, the password turns out to be cscodershub (the organizer). The pastebin tells us to 'Check Github'. We proceed to the github page of the challenge creator, where we find a repo called Trollcat. There's a bunch of image files here, as well as a text file called 'ciphers are fun'. Inside, `uggcf://cnfgr.hohagh.pbz/c/Ot76p3z4Zt/`, a clear rot13 cipher. This url takes us to another pastebin, which gives us a base64 string. Decoding this reveals the flag, `Trollcat{C1Ph3Rs_aR3_Fun_1sint_It?}`.

### Nested exploration

We are taken to a website with a registration form, and told that we might get lucky if we register an account 69 times. Opening devtools and heading into storage we find a cookie. Change the value of that to ~~69~~, ~~68~~, 67 and we are given our flag, `Trollcat{w3b_scr1pt3rs_b3w4re}`. Definitely did not do this manually. Definitely.

### Trip to Snapistan (Charlie)

Snapchat picture of a napkin that said 'Le conche', googled that and it autocorrected to 'Le Conchour Jeddah' which had the same logo as the napkin and then found their phone number on the site. Flag `Trollcat{966126061441}`.

### Trip to Snapistan 2 (Charlie)

Snap video of a beach where you could see a tall building and a mosque, googled 'tallest building Jeddah' and found out it was the Golden Tower in Jeddah, then checked maps to find the mosque and then found the fax number for the Golden Tower on their website. Flag `Trollcat{966500771177}`. Apparently you can also find both of these videos on snapchat and use the snap map to locate them.

### Heavy driver (Charlie)

Snap video of car, copied licence plate and googled licence plates of the world to find out it was Indian, googled 'Indian licence plate lookup' and found an official site where you can look up a licence plate to find the owner in India. Name was redacted so asked an Indian friend to deduce the name Sri Arvind.
Apparently there is a second site where the name was not redacted with the same functionality. Flag `Trollcat{arvind_19012017}`.

### Life is a race (Charlie)

Followed the instagram maze/race thing and at the finish line checked the photos where the account was tagged, saw an animal instagram page and clicked the cat pictures, the flag was a comment on one of those pictures. Flag `Trollcat{f!n!$#_lin3}`.

### Change my mind (Zenode)

Was given a picture that didnt have anything wrong with it. Just chucked it into https://stylesuxx.github.io/steganography/ to see if there was anything obvious. Came up with the flag in the decrypt, `Trollcat{I_L0v3_Tr011C4t}`. Alternatively zsteg would have also revealed the flag.

### Alien message

We are given an .mp3 file and told to decode it. Using the usual stegano tools on it yields nothing, so we take a look at it with sonic-visualiser. Quick look at the waveform reveals a morse code inside the track, which decodes to the flag, `Trollcat{TROLLCATCTFBROUGHTTOYOUBYCSCODERSHUB}`.

### Trolling CAT (Zenode)

Given an image that contained the flag. Again chucked it into https://stylesuxx.github.io/steganography/ to see anything obvious. This yielded nothing so I used binwalk on the image and saw there was a zip file. Extracted flag.txt with `binwalk -e trollcat.png`, which contained the flag, `Trollcat{St3gnoGr4phy_1S_FuN}`.

*personal note: was the first to submit this flag :D

### CatBite

We are given an image, bitten.png. Exiftool, binwalk, foremost, strings etc. yield nothing. Taking a look at the individual layers with stegsolve we see a certain pattern in the top left corner, but that turns out to be a meaningless artifact. Moving on with stegoveritas, which finds 2 instances of ASCII text in the image. One of those extracted files has our flag, `Trollcat{Tr00ling_C4t}`, on the first line.

### Forbidden

We are given a file, trollcats.car, and asked to retrieve data from this file. Googling about .car files reveals thats it's some sort of an archive, Binwalk tells us that it's a bzip2 archive, however trying to unpack it does not work. We run binwalk with the extract argument, which produces a file, inside of which we find our flag, `Trollcat{M0zilla_Archive_maaaarls}`. An alternative method would have been to use bzip2recover, to repair the file, and then unpacking it.

### Rich Orphan (Zenode)

Was given a .txt file that contained the following:
```sys:$1$fUX6BPOt$Miyc3UpOzQJqz4s5wFD9l0:14742:0:99999:7:::
sys:x:3:3:sys:/dev:/bin/sh
```

the first string looked suspiciously like an MD5 hash so I put it into John The Ripper and attempted to decrypt the hash. This yielded the flag, `Trollcat{batman}`.

### Sanity check, Discord, Social challenge

For sanity check we are just given the flag, boring :(. There's a second sanity check with a flag on the Discord server. Finally, we have to do some actual searching to find a flag on the organizers social media. This ends up being in the about section of the Youtube page. Not very thrilling.


## Useful Stuff

Cracking password protected zip, rar, pdf files with zydra https://null-byte.wonderhowto.com/how-to/crack-password-protected-zip-files-pdfs-more-with-zydra-0207607/

Basic Stegano checklist https://fareedfauzi.gitbook.io/ctf-checklist-for-beginner/steganography

Hiding and extracting messages in x86 programs https://github.com/woodruffw/steg86
