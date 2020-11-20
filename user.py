#!/bin/python3

#######
## a ## getting data from user defined query
#######



#first lets import the modules needed
import os, subprocess, sys, re


#we make a folder for our assignment and navigate there
if not os.path.exists("database"):
        os.mkdir("database")
os.chdir("database")


#Introductory lines
print ("\nWelcome to B120271\'s  tool for protein conservation and motif ID analysis\n")


#we establish a loop for user inputs

i=1

while i == 1:
	#receive input for taxonomic group
	tax = input("Please input subset of taxonomic tree of interest:\n")


	#receive input for protein of interest
	prot = input("Please input protein family of interest:\n")


	#confirm analysis
	print("\nAnalysis will be performed on the\n",
	prot," protein family\n",
	"in the\n",
	tax, "taxonomic subset\n")

	proceed = input("Do you wish to continue? [yes/no] \n")

	if proceed == "yes":
		print ("Fetching data...")
	else:
		sys.exit()


	#lets go fetch our sequences now
	#we first copy our current environment to retain our variables
	current_env = os.environ.copy()


	#adding these to our dictionary just in case
	current_env ["wowe"] = tax
	current_env ["wow"] = prot


	#we output the fasta information using the esearch commands
	subprocess.call('esearch -db protein \
	-query "$wowe [organism] AND $wow [protein]" |\
	efetch -format fasta > data.txt', env=current_env, shell=True)


	#update the user on progress
	print("Data successfully downloaded")


	#reading through the data to let the user know what they have downloaded
	data = open("data.txt").read()
	print("\nWithin your defined dataset,")


	#we count the number of sequences as >
	seq = data.count('>')
	print("The total number of sequences is:\n", seq)


	#we count the number of non redunant species
	spec = "peepee poopoo"
	print("The total number of unique species is:\n", spec)

	#if this is not acceptable we ask user if they want to restart
	print("\nWARNING! Program will only analyse top the 250 most similar sequences")

	next = input("Would you like to redefine your query? [yes/no]\n")

	if next == "yes":
		#restart the loop 
		i = 1
	else:
		#exit the loop
		i = 2 


#Going to the next step
print("Proceeding with conservation analysis...")
