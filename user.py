#!/bin/python3


#this part of the script will get the user to specify protein family and tax group
#then it will fetch the relevant information from the user input


#######
## a ## User specifies protein family and taxonomic group
#######

#first lets import the modules needed
import os, subprocess, sys, re


#Introductory lines
print ("\nWelcome to B120271\'s  tool for protein conservation and motif ID analysis\n")


#receive input for taxonomic group
tax = input("Please input subset of taxonomic tree of interest:\n")


#receive input for protein of interest
prot = input("Please input protein family of interest:\n")


#confirm analysis
print("\nAnalysis will be performed on the\n", 
prot, " protein family\n"
, "in the \n", 
tax, "taxonomic subset\n")

proceed = input("Do you wish to continue? [yes/no] \n")

if proceed == "yes":
	print ("Fetching Information...")
else:
	sys.exit()
	

#we make a folder to store our sequences and navigate there
os.mkdir("database")
os.chdir("database")


#lets go fetch our sequences now
#we first copy our current environment to retain our variables
current_env = os.environ.copy()

#adding these to our dictionary just in case
current_env ["wow"] = prot
current_env ["wowe"] = tax

#we output the fasta information using the esearch commands
subprocess.call('esearch -db protein \
-query "$wowe [organism] AND $wow [protein]" |\
 efetch -format fasta > data.txt', env=current_env, shell=True)

#update the user on progress
print("Data successfully downloaded...")

#proceed options
print("Proceeding with conservation analysis...")

#look through output files and get bare data about it to present to the reader
#like number of sequences, etc
#if term too narrow, prompted to search for broader parameters
#could take the user back to the start in a loop or something

