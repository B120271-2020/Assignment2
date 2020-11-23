#!/bin/python3

#######
## a ## getting data from user defined query
#######


#first lets import the modules needed
import os, subprocess, sys, re, time


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
		print ("Please be patient, fetching data...")
	else:
		sys.exit()


	#lets go fetch our sequences now
	#we first copy our current environment to retain our variables
	current_env = os.environ.copy()


	#adding these to our dictionary just in case
	current_env ["tax"] = tax
	current_env ["prot"] = prot


	#we output the fasta information using the esearch commands
	subprocess.call('esearch -db protein \
	-query "$tax [organism] AND $prot [protein]" |\
	efetch -format fasta > data.txt', env=current_env, shell=True)


	#update the user on progress
	print("Data successfully downloaded")


	#if this is not acceptable we ask user if they want to restart
	print("\nWARNING! Program will only analyse the top 250 most similar sequences")
	

	#reading through the data to let the user know what they have downloaded
	data = open("data.txt").read()
	print("\nWithin your defined dataset,")


	#we count the number of sequences as >
	nseq = data.count('>')
	print("The total number of sequences is:\n", nseq)


	#we count the number of non redunant species
	nspec = set(re.findall('\[(.*?)\]', data))
	print("The total number of unique species represented:\n", len(nspec))

	#option to redefine query
	next = input("\nWould you like to redefine your query? [yes/no]\n")

	if next == "yes":
		#restart the loop 
		i = 1
	else:
		#exit the loop
		i = 2 


#Going to the next step
print("Proceeding with conservation analysis...")


#######
## 2 ##
#######

#we make a database from the users query
subprocess.call('makeblastdb -in data.txt -dbtype prot -out reference', shell=True)
print("Reference database successfully created")


#use cons to get a query sequence
cmd = 'cons data.txt'
print("To verify you are not a robot, please input the following within the square brackets [yes]")

#we wait to make sure user has read the prompt
#this process of file naming is a bit of a cop-out
time.sleep(3)

#the user input of yes specifies the file name used in the next command
subprocess.call(cmd, shell=True)

#we blast our query prompt
subprocess.call('blastp -db reference -query yes -outfmt "6 sseqid sseq" > blastoutput.out', shell=True)

#we format the blast into a "semi-fasta"
subprocess.call("sed 's/^/>/' blastoutput.out > temp", shell = True)

#trim for the top 250 represented sequences
subprocess.call("head -n 250 temp > temp2", shell = True)

#trim for the top 250 represented sequences
subprocess.call("head -n 250 temp > temp2", shell = True)

#replacing each tab with a newline to get a fasta format
text = open("temp2").read()
text2 = text.replace('\t', '\n')
f = open("trim", "w")
f.write(text2)
f.close()

#align with our file
subprocess.call('clustalo -i trim --outfmt=fasta -v -o align.fa --output-order=tree-order --iter=2', shell=True)
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
