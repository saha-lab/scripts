import csv, os
from itertools import combinations

"""
This script takes in a .csv file output from CLC's RNA-Seq Analysis tool,
and converts it into the format of count table needed by DESeq2. This
output may then be treated as if it was HTSeq-Count output.
Some parts of this code borrow from Sam Clamons' csvannotation.py

Note: The filenames of the input files MUST be in the format of:
condition_replicate#_otherInformation.tsv
in order to correctly group files of the same conditions.

By Caroline Golino (Edited 170424)
"""

def makeCountTablesForSubfolders(parentFolderName, subfolderList):
	for sub in subfolderList:
		makeCountTable(parentFolderName+sub, parentFolderName+sub+"//"+sub+"_Count_Table.tsv")

def make_all_count_tables(folderName):
	"""Makes one count table containing all of the reads for each sample."""
	allSamples = get_all_files(folderName)
	
	allCountDicts = []
	for fileName in allSamples:
		sampleDict = makeCountDict(fileName, folderName)
		if sampleDict == None:
			print ("Warning: "+fileName+" doesn't have read counts. Ignored.")
		else:
			allCountDicts.append(sampleDict)

	conditions = get_conditions(allSamples)
	#combos = get_file_combinations(conditions)

	allCountDicts = check_count_dicts(allCountDicts)

	make_count_table(allCountDicts, folderName+"All_Counts.tsv")

	for s in allCountDicts:
		make_count_table([s], folderName+s["name"])

	#for c in combos:
	#	make_count_table(get_dicts_for_comparison(c,allCountDicts), folderName+make_output_name(c))

def make_count_table(countDicts, outName):
	"""Takes in a list of count dicts to combine into one count table."""
	with open(outName, 'w') as outfile:
		for sample in countDicts:
			outfile.write("\t"+sample["name"])
		outfile.write("\n")
		for gene in countDicts[0].keys():
			if (gene == "name"):
				continue
			outfile.write(gene)
			for sample in countDicts: #sample is the dict w/ key of gene name
				if gene in sample.keys():
					outfile.write("\t"+sample[gene])
				else:
					print ("File " +sample["name"]+" is missing gene " + gene)
			outfile.write("\n")
	print("Finished writing file: "+outName)

def check_count_dicts(allCountDicts):
	"""Check that all count dicts have the same number of genes."""
	allFirstGenes = allCountDicts[0].keys()
	for sampleDict in allCountDicts:
		if sampleDict.keys() != allFirstGenes:
			print ("Warning: " + sampleDict["name"] + " does not contain" + \
				" the correct number of genes. It is being removed.")
			allCountDicts.remove(sampleDict)
	return allCountDicts

def get_all_files(folderName):
	"""Get all of the files with read counts."""
	allSamples=[]
	[root, folders, files] = next(os.walk(folderName))
	for filename in files:
		if filename.endswith('.csv'):#Just taking .csv for now
			dataFilename = folderName + os.sep + filename
			allSamples.append(dataFilename)
	return allSamples

def make_output_name(combo):
	"""Creates a name for the output file comparing the files in countDicts"""
	fileName = ""
	for cond in combo:
		fileName = fileName + cond +"_"
	return fileName.replace("/", "")+"Count_Table.tsv"

#def get_file_combinations(files):
#	combos = combinations(files, 2)
#	return combos

def get_conditions(files):
	"""Get all of the conditions to be compared."""
	condList = []
	for f in files:
		f = f.split("/")[-1]
		if f.split("_")[0] not in condList:
			condList.append(f.split("_")[0])
	print("All conditions found:" + str(condList))
	return condList

def get_dicts_for_comparison(combo, countDicts):
	"""Select the dictionaries relevant to the given comparisons."""
	selectDicts = []
	for cond in combo:
		for cd in countDicts:
			if cond in cd["name"]:
				selectDicts.append(cd)
	return selectDicts

def makeCountDict(inTableName, folderName, countColName = 'Total gene reads'):
	"""Returns a dictionary of count values for genes in a single sample."""
	
	myFile = open(inTableName, 'rU')
	reader = csv.reader(myFile)
	headerLine = next(reader)
	if countColName in headerLine:
		colNumber = headerLine.index(countColName)
	else:
		print("Error: the input file does not contain read counts. If " + \
			"you're sure it does, try specifying the name of the column containing read counts.")
		return
	geneCounts= {} #keys will be the gene name, and the vals the counts
	geneCounts["name"]= inTableName[len(folderName):]
	for line in reader:
		geneCounts[line[0]] =line[colNumber] #Assuming the first col=gene name
	myFile.close()

	return geneCounts

make_all_count_tables('/Volumes/cachannel/RNA_SEQ/Analysis/WC1/Quantification/T0/rep1')