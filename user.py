#!/bin/python3


#this part of the script will get the user to specify protein family and tax group
#then it will fetch the relevant information from the user input


#######
## a ## User specifies protein family and taxonimic group
#######

#first lets import the modules needed
import os, re


#Introductory lines
print ("Welcome to B120271\'s  tool for protein conservation and motif ID analysis")


#receive input for protein
prot = input("Please input protein family of interest:")
print(prot)


#receive input for taxonomic group
tax = input("Please input subset of taxonomic tree of interest:")
print (tax)
