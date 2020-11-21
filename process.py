#!/bin/python3

#######
## 2 ##	Plotting conservation between protein sequences
#######

import os, subprocess, sys, re

#for this section of script we navigat to the databse folder
#this is redundant for the final script
os.chdir("database")

#we align the data using clustalo under subprocess command
subprocess.call('clustalo -i data.txt --outfmt=fasta -v -o output.fa', shell=True)


#we first 

#determine and plot conservation levels between sequenecs across taxonoic groups
#establish similarity within user sequence set chosen
#output to screen and save as file output
#limit number of sequences to no more than 250 most similar



# we can use emboss plotcon for it
# or clustalo too
# or blast

# we need to make a protein database with our previous data

