# Tec_Crack
A small utility for cracking the captured login hash from a Technicolour TG582n ADSL Router

=======
Usage
=======

	Tec_Crack.py -u <USER> -n <NONCE> -h <HASH> -w <FILE>

=======
Options
=======

	-u,  --user=<USER>	Username
	-n,  --nonce=<NONCE>	Random nonce, unique to each login attempt
	-h,  --hash=<HASH>	MD5 Hash to be cracked
	-w,  --wordlist=<FILE>	Address of Wordlist file
