#!/bin/python3

#######
## 2 ##	Plotting conservation between protein sequences
#######

import os, subprocess, sys, re

#for this section of script we navigat to the databse folder
#this is redundant for the final script
os.chdir("database")

#we make a database from the users query
subprocess.call('makeblastdb -in data.txt -dbtype prot -out reference', shell=True)
print("Reference database successfully created")


#use cons to get a query sequence
cmd = 'cons data.txt'
print("To verify you are not a robot, please input the following within the square brackets [yes]")
subprocess.call(cmd, shell=True)

#we blast our query prompt
subprocess.call('blastp -db reference -query yes -outfmt 7 > blastoutput.out', shell = True)
subprocess.call('blastp -db reference -query yes -outfmt "6 sseqid sseq" > blastoutput.out', shell = True)

#to format into fasta
subprocess.call("sed 's/^/>/' blastoutput.out > temp", shell = True)

#trim
subprocess.call("head -n 250 temp > temp2", shell = True)

#output now fasta
text = open("temp2").read()
text2 = text.replace('\t', '\n')
f = open("trim", "w")
f.write(text2)
f.close()

#align 
subprocess.call('clustalo -i trim --outfmt=fasta -v -o align.fa --output-order=tree-order --iter=3', shell=True)
print("Data successfully aligned")

#plot
subprocess.call('plotcon -sformat fasta align.fa -graph svg', shell=True)
subprocess.call('xdg-open plotcon.svg', shell=True)



#plotcon is used to process a conservation plot from clustalo output
print("Proceeding with convservation plot")
print("When prompted, input size of windows. Larger windows result in smoother plots")

#the program can now continue after the user exits
print("Conservation plot for variables here successfuly generated")
print("Scanning for motifs from the prosite database")
