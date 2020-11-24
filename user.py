#!/bin/python3

#######
## 1 ## getting data from user defined query
#######


#first lets import the modules needed
import os, subprocess, sys, re, time

#Introductory lines
print ("\nWelcome to B120271\'s  tool for protein conservation and motif ID analysis\n")
print("Program will write outputs to the \'database\' folder in the current directory.")

#we make a folder for our assignment and navigate there
#the folder is made writable by the user and guests

if not os.path.exists("database"):
        os.mkdir("database")
subprocess.call('chmod u+rwx database', shell=True)
subprocess.call('chmod g+rwx database', shell=True)
os.chdir("database")

#we establish a big loop for user inputs

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

	proceed = input("Do you wish to continue? [yes/no/exit] \n")

	if proceed == "yes":
		print ("Please be patient, fetching data...")

		#lets go fetch our sequences now
		#we first copy our current environment to retain our variables
		current_env = os.environ.copy()


		#adding these to our dictionary just in case
		current_env ["sub"] = tax
		current_env ["pro"] = prot


		#we output the fasta information using the esearch commands
		#specifying the subset as an 
		subprocess.call('esearch -db protein \
		-query "$sub [organism] AND $pro [protein]" |\
		efetch -format fasta > data.txt', env=current_env, shell=True)


		#update the user on progress
		print("Data acquired")


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
	
	elif proceed == "no":
		print("Redefining query")
		i = 1
	else:
		sys.exit() 


#Going to the next step
print("Proceeding with conservation analysis...")


#######
## 2 ##
#######

#we make a database from the users query
subprocess.call('makeblastdb -in data.txt -dbtype prot -out reference', shell=True)
print("Reference database successfully created")

#we align our data
#align with our file
subprocess.call('clustalo -i data.txt --outfmt=fasta -v -o clust.fa --output-order=tree-order --iter=1', shell=True)
print("Data successfully aligned")

#we keep the top 250 sequences
#as aligned fastas all have the same length, 
#the total number of lines divided by the total number of sequences gives the number of lines per sequence
#so 250 multiplied by (lines/sequences) is the 250 top sequences assigned by clustalo
align = open("clust.fa").read()
lines = align.count('\n')
sequences = align.count('>')
keep=int(250*(lines/sequences))


aligns=align.splitlines()
aligns= str(aligns[0:keep])
aligns=aligns.replace("', '", "\n")
aligns=aligns[2:-3]
aligns = aligns + "\n"

#write out 250 top to file
f = open("trim.fa", "w")
f.write(aligns)
f.close()


#use cons to get a query sequence
cmd = 'cons trim.fa'
print("To verify you are not a robot, please input the following within the square brackets after the next prompt [yes]")

#we wait to make sure user has read the prompt
#this process of file naming is a bit of a cop-out
time.sleep(5)

#the user input of yes specifies the file name used in the next command
subprocess.call(cmd, shell=True)

#we blast our query prompt
subprocess.call('blastp -db reference -query yes -outfmt "6 sseqid sseq" > blastoutput.out', shell=True)

#we format the blast into a "semi-fasta"
subprocess.call("sed 's/^/>/' blastoutput.out > temp", shell = True)

#replacing each tab with a newline to get a fasta format
text = open("temp").read()
text = text.replace('\t', '\n')
f = open("align.fa", "w")
f.write(text)
f.close()

#plotcon is used to process a conservation plot from clustalo output
print("Proceeding with convservation plot")
print("When prompted, input size of windows. Larger windows result in smoother plots, at loss of sensitivity")

#we plot using our aligned data
subprocess.call('plotcon -sformat fasta align.fa -graph svg', shell=True)
print("Opening plot...")
subprocess.call('xdg-open plotcon.svg', shell=True)

#the program can now continue after the user exits
print("Conservation plot for ", prot, " in ", tax, "successfuly generated")
print("Scanning for motifs from the prosite database")



#######
## 3 ## 	scan for motifs from prosite database
#######

#align.fa contains top 250 aligned protein sequences
#we'll have to process this so it writes out a separate file for each of the 250
#and then use each one as an input 

#we read the file
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

#give the user time to read
time.sleep(5)

#now we process each file into patmatmotifs
cmd = 'for file in *\n do\n patmatmotifs $file out\n cat out >> all.txt\n done'
subprocess.call(cmd, shell=True)

#now lets look for elements in the summary file
all = open("all.txt").read()

sequences = len(seq)
print("From the ", sequences, " sequences:")


#sequences with motifs
nmotifs = re.findall(r'Motif = .+', all)
lenmotifs=len(nmotifs)
print("A motif has been identified: ", lenmotifs, "times")

#different motifs by name
dmotifs=set(nmotifs)
print("The different motifs present in the sequences are: ", dmotifs)

#number of sequences for each motif 
for i in dmotifs:
	n=nmotifs.count(i)
	print("There are ", n, "occurences of ", i, "in all sequences")

#we write these to a file so the user can look at them later if interested 
os.chdir('..')

sys.stdout = open("summary.txt", "w")
print("From the ", sequences, " sequences:")
print("A motif has been identified: ", lenmotifs, "times")
print("The different motifs present in the sequences are: ", dmotifs)
print("There are ", n, "occurences of ", i, "in all sequences")
sys.stdout.close()
