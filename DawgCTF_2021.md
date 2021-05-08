<p align="center"> ### Dawg CTF, May 2021 documentation ### </p>
<p align="center"> ### Placement: x / x ### </p>
<br/><br/>

- [FORENSICS](#forensics)
  - [Just A Comment](#just-a-comment)
  - [These Ladies Paved Your Way](#these-ladies-paved-your-way)
  - [Photo Album](#photo-album)
- [MISC](#misc)
  - [Two Truths and a Fib](#two-truths-and-a-fib)
  - [Identifications](#identifications)
- [AUDIO RADIO](#audio-radio)
  - [Babys First Modulation](#babys-first-modulation)
  - [Third Eye](#third-eye)
  - [Tag Youre It](#tag-youre-it)
  - [Tuning In](#tuning-in)
  - [Deserted Island Toolkit](#deserted-island-toolkit)
  - [Moses](#moses)
- [CRYPTO](#crypto)
  - [cooking the ramen](#cooking-the-ramen)
- [BINARY BOMB](#binary-bomb)
  - [Phase 1](#phase-1)
  - [Phase 2](#phase-2)
  - [Bonus Phase](#bonus-phase)

<br/><br/>

## FORENSICS

### Just A Comment
 
Given a pcap file, we can see that there's a comment. We can view this by going Statistics -> Capture File Properties. 

Packet Comments 
Frame 1648: `DawgCTF{w3 h34r7 0ur 1r4d 734m}`.

### These Ladies Paved Your Way

We're given an image folder of 10 influential women in technology. Challenge says: One of them holds more than 100 issued patents and is known for writing understandable textbooks about network security protocols. What other secrets does she hold?

The images are all named, and so with some googling the person in question appears to be Radia Perlman. Tried to search more about her to find the 'secrets' but found nothing. Eventually went back to the image file, no steganography in it but exiftool reveals something nice.

Keywords : VpwtPBS{r0m5 0W t4x3IB5}

Credit   : U3Bhbm5pbmdUcmVlVmlnCg==

So we clearly have the flag in some sort of substitution cipher. Credit decodes to SpanningTreeVig, so perhaps this is the key? Vigenere Cipher, and flag decodes to `DawgCTF{l0t5 0F p4t3NT5}`.


### Photo Album

We're given a password protected zip file. "Your grandparents forgot the password to their online photo album! Lucky for you, they only ever use simple passwords and you’re a UMBC CS student. Make them proud."

There's additional hints, the password is 8 chars and "your grandparents are proud alumni of the first class at UMBC."

Given this, and after trying a lot of combinations, the files extract with 1966umbc. At first glance they all look like normal image files, except one that is 21 bytes in size. cat pic and flag is `DawgCTF{P1ctur35qu3}`.


## MISC

### Two Truths and a Fib

Netcat parsing. [Scuffed code but I went fast for time.](https://github.com/jp1995/ctf_docs/blob/main/scripts/two_truths_and_a_fib.py)

### Identifications

We're given a picture taken at night of a certain verizon office. Another picture showing nearby Wi-Fi SSID's. We need to get the CLLI of this verizon office.

Looking at the SSIDs, there's a couple interesting ones. SpaGuest, Katanasushi, Carroll Counselling, Dunkin' Donuts GUest and Carterque.

After doing some googling with these businesses, it turns out that there are only 4 Carroll Counselling offices, all in Maryland. Eventually we find one surrounded with the rest on our list, in the city of Mt Airy. After some street view action it turns out that the verizon office is also there, it just doesn't show up on the map. I assume because it's not an office at all, but some sort of general telecom equipment building.

Learning about CLLI codes, the first four characters are the city, next 2 are for the state and then further specifics. Looking up MTARMD results in a couple Verizon related CLLI codes, one of which is `MTARMDMARS1`, which is the flag.

## AUDIO RADIO

### Babys First Modulation

We are given a .iq file and told the following: This IQ file was saved in standard GNURadio format (complex, 32bit float I, 32bit float Q). Additionally, it's supposed to be a recording of someone reading the flag.

After trying to mess around with GNURadio, I found a simpler command line tool called sox, that allows us to convert the iq file into a wav file. The format is the following:

`sox -e float -t raw -r 48000 -b 32 -c 2 rf1.iq -t wav -e float -b 32 -c 2 -r 48000 rf1.wav`

At 48kHz we hear something resembling whale communication maybe, it sounds very alien. At 192kHz you can kinda start to hear something resembling human language, but it's still very slow and demonic. 640kHz seemed to be the sweet spot and the voice could be heard pretty clearly.

flag is `DawgCTF{listen_in_on_the_waves}`.

### Third Eye

given a mp3 file, opening in sonic visualiser and using the spectrogram view we can see some hex code. this decodes to `DawgCTF{syn3sth3s1acs}`.

### Tag Youre It

Another audio chall. MP3 files have tags for organization but nothing in there as the title would suggest. Running edxiftool for more info and flag is visible in the Comment. Ḑ̶a̴͈w̸͚g̸̱C̵̹T̴͍F̴͚{̴̟w̵̻h̴̭0̵̤_̷̟d̶͕0̶͎w̸͙n̷͚l̶̜0̴͓a̶͚d̷̡s̴ͅ_̶̺m̵̳u̶͎s̷̰1̸͖c̶͔_̷̧a̵̙n̵͈y̴̬m̸̩0̸͓r̴͕3̶͎?̴̩}̴̲, needs to be cleaned up a bit, challenge accepts `DawgCTF{wh0_d0wnl0ads_mus1c_anym0r3?}`.

### Tuning In

So this is another .iq file, but trying the same angle as the last time doesn't yield anything intelligible. Besides, we need to be able to quickly try different frequencies fairly precisely.

After trying to understand gnu radio some more, I give up and stumble upon gqrx, a fantastic tool for exactly this use case. We can directly feed it our .iq file, set an input rate, and run it. I randomly set the rate to 640000 Hz because that's what worked for the last challenge.

![](https://cdn.discordapp.com/attachments/534004815160934410/840619622520193074/unknown.png)

This is what the interface looks like. We can see 5 distinct "waveforms?", unsure of the correct terminology here. The slider can be dragged across them just like you would on a radio. Fourth "waveform" from the left is someone reading the flag, `DawgCTF{shifting_your_perspective}`.

### Deserted Island Toolkit

We are given a iso file with no other hints. file says it's ISO 9660 CD-ROM filesystem data. Mounting with `mount -t iso9660 dawgTunes.iso /mnt/challenge` and we find a .cdda file on the disc. Converting it to wav using an online converter, which yields some morse code.

![](https://cdn.discordapp.com/attachments/534004815160934410/840635632979804160/unknown.png)

This decodes to `S0SISNOTTHEAN5W3R`, wrapped in DawgCTF{} makes the flag.

### Moses

Another audio chall, this time there's two separate flac files. "If you can find a way to part the waves, you might find something on the seafloor."

These files seem almost identical, but one is slightly larger in size. First seemingly obvious thing to try is to find the difference between the files. This can be done with sox. `sox -m -v 1 moses1.flac -v -1 moses2.flac moses_difference.flac`. Spectrogram of the the difference contains the flag, `DawgCTF{sunk3n_tr3asur3s`.

![](https://cdn.discordapp.com/attachments/534004815160934410/840644083290341416/unknown.png)

## CRYPTO

### cooking the ramen

Challenge description has some morse code, decoding it we get `JVVE4VS2IRWGCWKYNB2FCV3UGJSUIZCHMVKEUMTENVNFOYZTLJZGG3SCK5JUONKXKZKVUWTDJBHFGZKXIZWVSM3QGFSWOPJ5`

Looks like base something so maybe cyberchef can help. From Base32, From Base64, From Base58 results in flag, `DawgCTF{0k@y_r3al_b@by's_f1r5t}`.

## BINARY BOMB

### Phase 1

Starting off easy... reversing (things) is fun! (Wrap all flags in DawgCTF{} when submitting to the scoreboard). 

Simple reverse, "Gn1r7s_3h7_Gn15Rev3R" > `DawgCTF{R3veR51nG_7h3_s7r1nG}`.


### Phase 2

Can you help me find my lost key so I can read my string?

"Dk52m6WZw@s6w0dIZh@2m5a" XOR with hex key '5' > `DawgCTF{An07h3R_rEv3r5aL_mE7h0d}`.

### Bonus Phase

Strings immediately reveals Pr3e7Y_57E4ltHy_Fl4g.

## Useful stuff




