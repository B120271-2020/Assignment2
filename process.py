#!/bin/python3

#######
## 2 ##	Plotting conservation between protein sequences
#######

import os, subprocess, time

#for this section of script we navigat to the databse folder
#this is redundant for the final script
os.chdir("database")

#we make a database from the users query
subprocess.call('makeblastdb -in data.txt -dbtype prot -out reference', shell=True)
print("Reference database successfully created")


#use cons to get a query sequence
cmd = 'cons data.txt'
print("To verify you are not a robot, please input the following within the square brackets after the next prompt [yes]")

#we wait to make sure user has read the prompt
#this process of file naming is a bit of a cop-out
time.sleep(3)

#the user input of yes specifies the file name used in the next command
subprocess.call(cmd, shell=True)

#we blast our query prompt
subprocess.call('blastp -db reference -query yes -outfmt "6 sseqid sseq" > blastoutput.out', shell = True)

#we format the blast into a "semi-fasta"
subprocess.call("sed 's/^/>/' blastoutput.out > temp", shell = True)

#trim for the top 250 represented sequences
subprocess.call("head -n 250 temp > temp2", shell = True)

#replacing each tab with a newline to get a fasta format
text = open("temp2").read()
text2 = text.replace('\t', '\n')
f = open("trim", "w")
f.write(text2)
f.close()

#align with our file
subprocess.call('clustalo -i trim --outfmt=fasta -v -o align.fa --output-order=tree-order --iter=3', shell=True)
print("Data successfully aligned")


#plotcon is used to process a conservation plot from clustalo output
print("Proceeding with convservation plot")
print("When prompted, input size of windows. Larger windows result in smoother plots, at loss of sensitivity")

#we plot using our aligned data
subprocess.call('plotcon -sformat fasta align.fa -graph svg', shell=True)
subprocess.call('xdg-open plotcon.svg', shell=True)

#the program can now continue after the user exits
print("Conservation plot for variables here successfuly generated")
print("Scanning for motifs from the prosite database")
