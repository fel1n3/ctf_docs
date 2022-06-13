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
...

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
As the name would suggest

### ContinuuOS (100p, Fel)
...

## OSINT
### Find Me if You Can (100p, Charlie)
...

### Lets Network (100p, Charlie)
...

### Can You Dig it? (100p, Charlie)
...

## RE
### Olden Ring (100p, Fel)
...

## STEGANOGRAPHY
### Characters of Shakespeare's Plays (200p, Charlie)
...

## MISC
### Poor Murphy (100p)
Challenge gave us a scrambled image, effectively something like a jigsaw puzzle, with each segment being 100x100px. There's probably some sort of a programmatic way of solving this, but I wasn't sure how to do that so I proceeded manually. 

I removed all the background segments, and then removed every other segment that didn't have a part of a letter in it. I missed a couple but it was good enough. Then I just put them together. It wasn't too easy, but the gradient lines behind the letters helped to align things. `flag{we_have_the_technology}`.

![Photoshop_dCTEvMFvwe](https://user-images.githubusercontent.com/8545997/173461298-a590eff5-a6c0-4991-ba70-2bc32cf52e51.png)













