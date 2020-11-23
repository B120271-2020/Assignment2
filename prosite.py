#!/bin/python3

#######
## 3 ## 	scan for motifs from prosite database
#######

#redunant

import os, re, subprocess

os.chdir("database")


#we read the file with all our sequences
seq = open("align.fa").read()

#split it into individual strings of each fasta
seq = re.split(r'\n>', seq[1:])

#then format it so all items have the > at the start
seq = ['>{0}'.format (i) for i in seq]

#we pull out each string and write it into a new file
if not os.path.exists("proteins"):
        os.mkdir("proteins")
os.chdir("proteins")

n=1

for i in seq:
	if n < 250:
		n=str(n)
		s = open (n, "w")
		s.write(i)
		s.close()
		n=int(n)
		n+=1

print("File inputs for PROSITE generated")


#we use a loop in unix to go through each file and process through the patmatmotifs
cmd = 'for file in *\n do\n patmatmotifs $file out\n cat out >> summary\n done'
subprocess.call(cmd, shell=True )


#looking through the summary file we can see
#how many sequenecs have a motif
#the different motifs by name
#the number of sequences associated with each motif
