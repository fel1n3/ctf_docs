<p align="center"> ### BlueHens CTF, March 2021 documentation ### </p>
<p align="center"> ### Placement: 29 / 324 ### </p>
<br/><br/>

- [MINECRAFT](#minecraft)
  - [MineR Code](#miner-code)
  - [Modest Cipher](#modest-cipher)
  - [Mega Chickens](#mega-chickens)
  - [Morse Craft](#morse-craft)
  - [Mountain Climber](#mountain-climber)
  - [Mixed Columns](#mixed-columns)
- [MISC](#misc)
  - [Conway Presents the Falcon](#conway-presents-the-falcon)
  - [Rise and Shine](#rise-and-shine)
- [WEB](#web)
  - [ctfvc](#ctfvc)
  - [SeaEssAreEph](#seaessareeph)
  - [speedrun-1](#speedrun-1)
  - [speedrun-2](#speedrun-2)
  - [speedrun-3](#speedrun-3)
- [REV](#rev)
  - [Me, Crack](#me-crack)


<br/><br/>

## MINECRAFT

The minecraft challenges were quite creative and the setup is explained in the following video:

https://www.youtube.com/watch?v=mqOSgJ0NM_Q

The minecraft code that creates the mc86 computer:

https://gist.github.com/AndyNovo/657ff15b7614f70e34f7295cb3dd7a8f

### MineR Code

This is just a simple sanity check challenge to make sure our mc86 computer works. The given command creates a QR code in minecraft, which gives us another command, which writes out the flag in banners, `UDCTF{M1N3CR4FT_4SS3MBLY_Y0}`.

### Modest Cipher

The given command creates the following cipher, however in the image I have replaced the fences with white concrete, which has a better contrast with the dirt.
![](https://cdn.discordapp.com/attachments/534004815160934410/823257453969801246/unknown.png)

I was not familiar with this cipher and it took me a little bit of googling, but it turns out to be pigpen (and the pigs are literally in pens, ha). Decoding this yields the flag, `UDCTF{LITERALPIGPENS}`.

### Mega Chickens

This time the command creates an untold amount of chickens standing in a row.
![](https://cdn.discordapp.com/attachments/534004815160934410/823258704358932500/unknown.png)

Their eyes are a dead giveaway, with blue representing a 0 and black representing a 1. Decoding this very creative binary string from left to right yields the flag, `UDCTF{4rmy_0f_blu3_hens}`.

### Morse Craft

For this one, the computer doesn't actually build or create anything. It plays us lovely minecraft morse instead. It's actually not so lovely to listen to over and over while attempting to decode the message... Anyway, a grass(?) sound represents a dash and a bell sound represents a dot. Flag is `UDCTF{CRAFTINGMORSEFORTHEWIN}`.

### Mountain Climber

This time there's no command, only an image. The hotbar is filled with various blocks. From left to right, Gravel, Emerald, Target, Birch, Loom, Obsidian, Chest, (Dried) Kelp, Emerald, Diorite.

![](https://cdn.discordapp.com/attachments/534004815160934410/823260824503451658/unknown.png)

I overthink'd it hard with my smooth brain, but eventually I managed to figure out that it's the first character of every block. The only part that might throw you off is that the Kelp block is technically a Dried Kelp Block. Anyway, flag is `UDCTF{GETBLOCKED}`.

### Mixed Columns

For this one, the setup is a little more complicated, which might explain the lower number of solves. The given source code generates 6 new mc86 computers lined up with the first one. It also gives you seven new books. You must then place these 7 books into the 7 computers, add buttons to every computer and execute them one by one. I was initially worried about the order of books but that didn't end up mattering.

This generates a 4x7 grid of characters, note the brackets and the characters making up `UDCTF{` in the top row (which I initially missed).

![](https://cdn.discordapp.com/attachments/534004815160934410/823263365530910760/unknown.png)

After a long time of furious cipher searching I decided to actually look at the grid for a bit, and the columns were indeed out of order, as per the title of the challenge. After simple reordering the flag is revealed:

```
U D C T F { 7
R 4 N S P O S
3 _ 7 H E _ C
O L U M N S }
```

## MISC

### Conway Presents The Falcon

We are given a file called golly.rle. Looking inside, we see

```
x = 2473, y = 1630, rule = B3/S23
2$
1406bo$
1407bo3bo$
1398b2o2b2o8bo12b2o$
```

And so forth. Googling takes us to Conway's Game of Life, as well as a program called golly, which is a simulator of Game of Life and other cellular automata. Inputting this file into the program, and running it slowly generates the flag, `UDCTF{th3y_c4ll_thems3lves_the_fl4g_smash3rs}` in a rather beautiful fashion.

![](https://cdn.discordapp.com/attachments/534004815160934410/823269511850491974/unknown.png)

This was a very simple task and arguably not a challenge at all, but it's very neat and I liked it.

### Rise and Shine

Back to actual challenges, we are given a very cryptic image.

![](https://cdn.discordapp.com/attachments/534004815160934410/823267001102761994/unknown.png)

This one took me forever. I tried every possible combination, No underline, Typewriter, Slim underline, Typewriter ... Fat underline, italics etc. Looked for anagrams, went line by line, absolutely nothing. Other players were apparently equally confused, and the organizers released a hint. `it is one common english word encoded in Baconian`

In the end (and this took me way too long to figure out) I was the *confused enemy* and the *secret* was not in the text at all. The real *intent* of the challenge was to distract from the surrounding stars.

40 stars, 2 types, seemingly random distribution. This was the baconian. And unfortunately for me it was in reverse, so that took another 15 minutes.

The baconian `AAABAAABBBAAAAAABABBABBBAABAAAABBABABBAA` decoded to "CHAMPION", and thus the flag, `UDCTF{CHAMPION}`.

## Web

### ctfvc

We are linked to a page that shows 10 lines of php code.

```
<?php
  if (isset($_GET['file'])){
    $file = $_GET['file'];
    if (strpos($file, "..") === false){
      include(__DIR__ . $file);
    }
  }
  //Locked down with version control waddup 
  echo highlight_file(__FILE__, true);
?>
```

Looks like  we need to grab the flag from one of the parent directories, but they check for '..' so we have to bypass this somehow. Oooor not. After trying different encodings like `%2e%2e`, `%252e%252e` etc. I'm still not getting anywhere.

But then there's this comment, `//Locked down with version control waddup`. Quickly checking for the .git file, and it exists. Using https://github.com/internetwache/GitTools Dumper and Extractor scripts, I'm able to extract the one commit, and looking at the metadata the commit message was: *not including flag directory 1a2220dd8c13c32e in the version control system*.

So, `?file=/1a2220dd8c13c32e/flag.txt`, yields the flag, `UDCTF{h4h4_suck3rs_i_t0tally_l0ck3d_th1s_down}`.

### SeaEssAreEph

So this one was supposed to be a CSRF challenge.. but it was a little broken actually, I believe. You could create an account and then log in, which I did when exploring the site. I discovered that you can send messages to the admins, as well as transfer funds, but only if you are a site admin.

Here's where the broken part comes in though. I logged in and out of my account quite a few times and one time I logged in and .. uhmm well, as it happens, I was put into someone else's account instead of my own. So I just sat there, stunned, contemplating this mysterious turn of events. I decided to refresh the page and apparently the better educated actual owner of the account had succeeded in the CSRF attack and sent 10000 eurodollars to themselves. I then decided to graciously borrow 1337 dollaridoos by hitting the "Buy Flag" button.

All I have to say in my defense is, ... eat the rich. Flag `UDCTF{us1ng_csrf_t0_st34l_4ll_th3_m0n3y}`.

### speedrun-1

Site simply says 'hello User 2'. Nothing else, nothing in the HTML, no requests. There is a cookie though. A cookie that looks very much like md5.

Running it through a md5 reverse service, the decoded value turns out to be '2'. Simple enough, generating a new md5hash for '1' and replacing the default cookie yields our flag, `UDCTF{d0nt_r0ll_your_0wn_s3ssions}`.

### speedrun-2

Speedrun-2 takes us to another website and we are shown some of the source code, which by default prints out a sqlite response for `SELECT * FROM course WHERE credits=3`. We can do a get request with ?credits=4 which then gives a different output.

Trying a manual UNION attack at first, and while I manage to get a request that shows the whole course table, I'm unable to access the information schema or any other potential tables.

Moving to sqlmap, with which I am quickly able to find all the tables, and dump the contents of the most interesting sounding table, `flag_xor_shares`.

`sqlmap "http://challenges.ctfd.io:30026/?credits=3" --dbms sqlite -T flag_xor_shares`

The table looks like this:

```
id,hexdigest
1,7419ccad9d5949e66614cd9458cdac149c2ad981c9f3ec56d30d03e730631c23598394a6055c55ecb5bec49dd0043b9fde76
2,835db37484676a462e223024a365c91fcdfe53ff975852abfacb79e0f3aef8d5b897a36c6fbfde9ca8e63b3ee00d3a1830f1
3,9c5890b6230771372122e9352ed1f3a1f644c9d4e451b81cb2f6643a067669972dc6a06617eaf08e539ada9a92b713b09b0c
4,53e5553b467e4badfcee4d97262445b27cdad3ced69a7fc69e0a04196685a61052cdd2f8a7a9650a0d861707f51403ccebc3
5,6dbdf9003a3c710afbc92a669f248c6fbe15fc550753264477436a5093614a2efc76310bb7906c911c305a0a39f566c8fc35
```

From the table name, we can guess that the flag is spread out over these hex values. There is still the xor component. And so, `xor(xor(xor(xor (1,2),3),4),5)`, gives us another hex value, which decodes to the flag, `UDCTF{h0n3stly_we_l1k3_crypt0_a_bit_m0re_th4n_w3b}`.

### speedrun-3

Site has a simple prompt asking for username. Attempting to pass admin, the site prompts us to reload the page if we are admin. After reloading another check appears: `{"admin":false,"name":"admin"}`. Checking cookies, there does indeed appear to be an authentication cookie, with 3 fields separated by dots. 

This is JWT, JSON Web Token format of header.payload.signature. Using https://github.com/ticarpi/jwt_tool we can tamper with the token, and modify the payload. The payload in this token has two fields, name="admin" and admin=False. I Tried changing admin to true and logging in with the new token, however this caused the site to error out.

Turns out there's a signature check, and somewhat obviously `name=admin, admin=True` has a different signature from `name=admin, admin=False`. The error did leak an interesting line though:

`Stack trace: #0 /var/www/html/index.php(531): Firebase\JWT\JWT::decode('eyJ0eXAiOiJKV1Q...', '82a59879a507', Array) #1`

The first value of the decode function is part of the token, but the second value seems to be the key. We can use this value to sign our tampered token. Full command:

`python3 jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6ZmFsc2UsIm5hbWUiOiJhZG1pbiJ9.bl9vGQri8PwEV94Wcv1TVjKAuMxYWhR3eLRoz0Yhwm0 -T -S hs256 -p 82a59879a507`

Logging in with the new properly signed token yields the flag, `UDCTF{st00p1d_PHP_err0r_mess4ges}`.

## REV

### Me, Crack

Another minecraft challenge, but this is in the Rev category.

The source command given instructs us to write the flag into a new book, one character per page, and to select that book when we run the program. Looking through the command book, we see that the program iterates over 16 pages. Therefore the length of the flag is 16 chars.

To test, running the flag with 'UDCTF{' on pages 1-6 and '}' on page 16. The program reports failures for pages 7-15, which means that we have the beginning and end correct. Looking into the logic of the program further, it appears that for every page the same set of operations is made, although with different variables.

The calculations are as follows:

- ARG1 and ARG2 are given some integer values
- `ARG1 *= ARG2`
- ARG2 is given a new value
- `ARG1 += ARG2`
- ARG2 is given a new value
- `ARG1 %= ARG2`

Finally, `ARG1 -= XVAL`. If the result is not 0, the program reports an error.

We don't know the value of XVAL (or it's at least hard to understand), but there are references to the ASCII table in the code, so it makes sense that XVAL is an ASCII decimal value of the required character. Since we know ARG1, which has to be the same as XVAL, we now know the required character for this page.

Repeat for every missing page and you have your flag, `UDCTF{MC86_4EVA}`.

## Useful Stuff

https://github.com/ticarpi/jwt_tool

https://github.com/AndyNovo/speedruns to practice pwn


