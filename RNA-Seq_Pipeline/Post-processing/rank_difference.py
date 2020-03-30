#!/usr/bin/env python

"""
Takes two ranked gene list and removes unique genes, then compares the rank of a gene 
in the first list to the rank of that same gene in the second list. If the difference 
of the rank is greater than a specified input, then output these genes to a csv file

USAGE: rank_difference.py <genelist1.csv> <genelist2.csv>
OUTPUT: genelist1.csv_rank_difference_results.csv

TODO: FINSIFH COMPARISON 

By Ronald Cutler
"""

def rank_difference(list1, list2):
	#put the gene list into arrays and remove the unique ones from each 

	#!!! - or include these and remove at the end as they will count when calculating difference between two ranked genes

	#remove the unqiue genes by finding the unique genes between the two list and extracting
	list3 = []
	list3 = list(set(list1).symmetric_difference(set(list2)))

	#remove unqiue elements from list1
	for x in list1:
		for i in list3:
			if i == x:
				list1.remove(i)
	#remove unique elements from list2
	for x in list2:
		for i in list3:
			if i == x:
				list2.remove(i)

	#compare the list - take the rank of a item in list 1 and compare it to the rank of the same item in list 2
	#make sure that the second list contains that element 
	try:
		





if __name__ == "__main__":
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    list1 = []
    list2 = []
    with open(filename1, 'rb') as file1:
        file1reader = csv.reader(file1)
        for line in file1reader:
            list1.append(str(line)[2:-2])
    with open(filename2, 'rb') as file2:
        file2reader = csv.reader(file2)
        for line in file2reader:
            list2.append(str(line)[2:-2])
    #output stream
	with open((filename1 + "_rank_difference_results.csv"), 'wt') as file3:
		filewriter = csv.writer(file3)
		results = rank_difference(list1, list2)
		filewriter.writerow(results)
