#!/bin/python3


#this part of the script will get the user to specify protein family and tax group
#then it will fetch the relevant information from the user input


#######
## a ## User specifies protein family and taxonomic group
#######

#first lets import the modules needed
import os, subprocess, sys, re


#Introductory lines
print ("Welcome to B120271\'s  tool for protein conservation and motif ID analysis",
"\n")


#receive input for taxonomic group
prot = input("Please input subset of taxonomic tree of interest:\n")


#receive input for protein of interest
tax = input("Please input protein family of interest:\n")


#confirm analysis
print("Analysis will be performed on the\n", 
prot, " protein family\n"
, "in the \n", 
tax, "taxonomic subset")

print("\n")

proceed = input("Do you wish to continue? [yes/no] \n")

if proceed == "yes":
	print ("Continuing analysis...")
else:
	sys.exit()
	

#we make a folder to store our sequences and navigate there
os.mkdir("database")
os.chdir("database")


#lets go fetch our sequences now
