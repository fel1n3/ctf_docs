<p align="center"> ### RITSEC CTF, April 2021 documentation ### </p>
<p align="center"> ### Placement: 39 / 720 ### </p>
<br/><br/>

- [FORENSICS](#forensics)
  - [Dream series](#dream-series)
  - [PleaseClickAllTheThings series](#pleaseclickallthethings-series)
  - [BIRDTHIEF FYSA](#birdthief-fysa)
  - [Parcel](#parcel)
  - [1597](#1597)
  - [Blob](#blob)
- [MISC](#misc)
  - [Revision](#revision)
  - [Corruption](#corruption)
- [WEB](#web)
  - [Robots](#robots)
  - [Sessions](#sessions)
  - [DababyWeb](#dababyweb)
  - [Revolution](#revolution)
- [REV](#rev)
  - [snek](#snek)
- [CRYPTO](#crypto)
  - [What an Enigma?](#what-an-enigma?)
  - [lorem ipsum](#lorem-ipsum)
- [INTEL](#intel)
  - [Finding Geno](#finding-geno)
  - [Data Breach](#data-breach)
  - [Music Signs](#music-signs)
  - [OSINTChallenge](#osintchallenge)
  - [APT Interference](#apt-interference)

<br/><br/>

## FORENSICS

### Dream series

The Dream challenges were a series of password protected zip files, with the flag of one level unlocking the next. Very easy.


- Dream 1: Flag is given in reverse plaintext, `RITSEC{Dreamland}`.
- Dream 2: Flag is given in hex, `RITSEC{WaterUnderTheBridge}`.
- Dream 3: Flag is given in base64 which decodes to hex which decotes to `fRITSEC{F@!!ingElev@tor}`.
- Dream 4: Given a weird windows executable that hopefully isn't malware. Opens a GUI window that just has a bunch of random garbage in it. We can scroll down, and in the end there's some morse code hidden by making the text white. This decodes to the flag `RITSEC{DIVERSION}`.
- Dream 5: Given a jpeg file. Nothing visible on different layers, stegoveritas doesn't return anything useful. Looking at it with a hex editor, there's an oddly long string that stands out, UklUU0VDezUyODQ5MX0g, which decodes to the flag, `RITSEC{528491}`.

### PleaseClickAllTheThings series

This was a series of terrible challenges. "Acquired" a legacy verion of Microsoft Outlook to open a .msg (CDFV2 Microsoft Outlook Message) file, which contained attached files.

- PleaseClick 1: The first one was an HTML file, however it was all encoded in JS `document.write(unescape('3c%68%74%6d%6c%3e%0a%3c%62... etc)).` This opens into a web page that has the base64 flag value in a tag, however the value is fully lowercase and decodes to gibberish.
  Using https://www.utilities-online.info/urlencode to decode the unescape yields the correctly capitalised base64, which decodes to `RITSEC{H3r3!t!$}`.
- PleaseClick 2: "Acquired" an older version of MS Word with macros support, opening the word file launched the macro and flag was visible in plaintext `RITSEC{M@CROS}`.
- PleaseClick 3: Same thing as PLeaseClick 2, flag visible in plaintext but in rot13. `RITSEC{R0TT1NGM@LC0D3}`.

### BIRDTHIEF: FYSA

We are given a PDF file and told to extract all information in from it. There's a black rectangle following some text, and moving it in a PDF editor reveals the flag, `RS{Make_sure_t0_read_the_briefing}`.

### Parcel

zip file that contains a Parcel.uncompressed file. Running file on it we find that it's multipart/mixed ASCII text file. It looks like some sort of an archive of an email conversation, including a lot of base64 encoded images. If we turn the base64 sections into images, we get many fragments of the flag, which can then be assembled like a puzzle in something like GIMP. Flag `RS{Im_doing_a_v1rtual_puzzl3}`

![](https://cdn.discordapp.com/attachments/534004815160934410/832236545305346059/parcel.png)

### 1597

We are given a link to a public facing git repo that displays its contents in JSON format. We can simply clone the directory, `git clone http://git.ritsec.club:7000/1597.git/`, and we get the .git directory plus a flag.txt and README.md files that were unavailable on the website.

The flag.txt file is empty though. Using GitTools extractor script on the .git directory, we can extract all commits.The flag file in one of the previous commits contains the flag. `RS{git_is_just_a_tre3_with_lots_of_branches}`.

![](https://cdn.discordapp.com/attachments/534004815160934410/832254536021835826/2021-04-10_141002.png)

### Blob

Finishing 1597 unlocks a couple of new challenges. For Blob, we are directed to another website with a git repo. Cloning this gives us an empty flag file like the last challenge, but running the extractor script only yields the one commit.

Looking around in some of the .git files, I stumble upon packed-refs, which contains a git hash / object / thingy for refs/remotes/originmaster, but also another value for refs/tags/flag. Running `git cat-file -p` on that hash prints out the flag, `RS{refs_can_b3_secret_too}`.

## MISC

### Revision

Another git challenge. Given another link and what looks like a quote: "... They aren't necessarily obvious but are helpful to know." Googling this takes us to some git documentation about revisions, as well as showing off some useful commands, like git log and git show.

Running git log in our Revision repo yields a very long commit history. Scrolling down something does catch the eye, the person cited as the creator of the challenge has made almost 40 commits. These commits were made over 2 years ago but they all have the exact same timestamp, down the the second.

Running git show on one of those commits shows that the file being worked on is called flag.txt. `git checkout 'commit' -- flag.txt` can be used to create a file flag.txt with the value it had after that commit. Every commit seems to overwrite the flag.txt file with a new character, with the final commit emptying the file altogether.

Wrote a short python script to automate this, yielding the flag `RS{I_h0p3_y0u_scr1pted_th0se_git_c0ms}`.

```
import git
import os

path = '/home/johan/ritsec/git/Revision'
os.chdir(path)
repo = git.Repo(path)

commits = list(repo.iter_commits("master"))

flag = ''

for i in commits:
    if i.author.name == 'knif3':
        repo.git.checkout(i)
        if os.path.isfile('flag.txt'):
            with open('flag.txt', 'r') as f:
                flag += f.read().strip('\n')

print(flag[::-1])
```

### Corruption

The final git challenge, this time the remote appears to have been corrupted, and we are asked to recover the data. git clone does not work, 

```
remote: aborting due to possible repository corruption on the remote side.
Unpacking objects: 100% (1/1), 69 bytes | 69.00 KiB/s, done.
fatal: early EOF
fatal: unpack-objects failed
```

however, it turns out that if we init a new repo, set the remote with `git remote add origin git://git.ritsec.club:9418/corruption.git` and then pull, ... then you still get the same error. Sometimes. Other times, the pull is successful. Not sure if this is intended or how that works, but good enough for me.

From here we do get a flag.txt and a README.md file, but there's nothing useful there, nor in the rest of the git folder structure. git log only shows the one initial commit. git fetch fails due to corruption. 

A command that comes up a lot when searching for how to repair git repos is `git fsck --full`. Running this gets us a "dangling blob" with a hexsha, running `git show` with that hexsha yields the flag, `RS{se3_that_wasnt_s0_bad_just_som3_git_plumbing}`.

## Web

### Robots

Flag is /robots.txt, base64 (They really love base64 huh) decodes to `RS{R0bots_ar3_b4d}`.

### Sessions

Babby tier, flag is base64 encoded sessiontoken cookie. `RS{0nly_One_s3ssion_tok3n}`.

### DababyWeb

Website that has two links to two php functions. One where we can input a string, and another where we can input a file. The latter is a very plain Local File Inclusion, we can grab the contents of /etc/passwd for example, but we still don't know where the flag is. There's also no way to run commands from here.

So command injection through the string function could maybe work... Semicolon is blocked, so can't do `;ls`, backticks dont work either, but `$(ls)` does! We find flag.txt in the parent directory, and then use the LFI-vulnerable function to access it. Flag `RS{J3TS0N_M4D3_4N0TH3R_0N3}`.

### Revolution

Directed to a website about robots taking over and revolotion and such. If we make the correct request, we can join the revolution. The challenge also gives multiple important hints.

"You will need a valuable piece of information from the 'robots' challenge." The last web challenge had a /robots.txt file, which explains the rules for web parsers (which subdomains are allowed and which are blocked for example). The custom user agent `User-Agent: Robot-Queto-v1.2` is an obvious grab. This can be included in the headers of a HTTP request.

"They expect a special type of request." This took me a long time, but the site has the line "Only then can we unlock your full potiential.", referring to the HTML UNLOCK method.

The challenge is called "Revolution", which directs to the /revolution subdirectory.

The actual hint for the challenge says "Use your head 2", referring to the html h2 tags with the values Friendly, Caring, Laws, Protect.

Finally the challenge says to "ONLY SEND PLAIN TEXT DATA"

I used postman to generate the request, but curl lets me demonstrate the solve in a more easy way. Note that the attribute values don't matter.

`curl -X UNLOCK "34.69.61.54:8799/revolution" -H "User-Agent: Robot-Queto-v1.2" -H "Content-Type: text/plain" --data-raw "Friendly=a,Caring=b,Laws=c,Protect=d"`

## REV

### snek

Given a python byte-compiled file, uncompyle6 do translate it back into source code. Looks like it uses a list of unicode values and user input to generate a decoded password. Just yoinking that list and decoding it into a string yields flag, `RS{all_hi$$_and_n0_bit3}`, appended to the end of the alphabet.

# CRYPTO

### What an Enigma? (Zenode)

todo

### lorem ipsum

Given text

```
Incompraehensibilis Conseruator.
Redemptor optimus
Iudex omnipotens
Sapientissimus omnipotens
Redemptor fabricator
Iudex redemptor
Optimus magnus
Aeternus iudex
Auctor omnipotens.
```

Quick google of the first line leads to the Trithemius Ave Maria cipher. Traditionally this outputs only fully uppercase, however we are given a colossal hint that the flag is case sensitive. So, a little twist on the cipher, given that one word = one letter, we assign lower or uppercase based on the word. Flag `RS{ThIsIsTrItHeMiUs}`.

# INTEL

### Finding Geno

We are simply told of a person called Geno and that he works for a firm called Bridgewater. We need to find his last name. Simple google search fings a linkedin page, and the last name in flag format is RS{ikonomov}

### Data Breach

Apparently Geno's email was involved in a data breach, and we have to find his password. The email address is found on the linkedin page, incogeno@gmail.com. Looking through actual data breach lookup services yields nothing, but simply googling the address gets us a fabricated data dump with his password. Flag `StartedFromTheBottom!`.

### Music Signs

Challenge says that Geno keeps up with his ex's music interests, and asks "What do they say about her personality". Looking up Geno on spotify doesn't work, however Geno has a twitter follower called Claire with a spotify link. She has a playlist, and the first letters of each song makes the flag, `RS{Sagittarius}`. The takeaway from this is that Spotify search is trash, and astrology is asinine.

### OSINTChallenge (Charlie)

todo

### APT Interference

Geno has disappeared! The challenge instructed us to find some incriminating evidence by looking at the social media of his ex. We are asked for a nation state though, and the data dump from Data Breach literally has `[[NATIONAL SECURITY SERVICE OF THE GOVERNMENT OF ACKARIA]] [[Super-Secret List of pwn'd Adversaries]]` in the beginning of it... Flag `RS{Ackaria}`.



