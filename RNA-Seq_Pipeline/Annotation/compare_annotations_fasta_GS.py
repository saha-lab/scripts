file_path = (input("What is the path to the first genome annotation in FASTA format:\n>>> "))
file1 = input("What is the name you'd like to assign this file in the final output:\n>>> ")
#hardcoded
#file_path ='new/Rhodococcus_erythropolis_ria-643_genome.fasta'
#####
file = open(file_path)
genome1 = file.read()
file.close()


#####
#file_path ='new/PROKKA_06272019_GES3.fasta'
####
file_path = input("What is the path to the second genome annotation in FASTA format:\n>>> ")
file2 = input("What is the name you'd like to assign this file in the final output:\n>>> ")
file = open(file_path)

genome2 = file.read()
file.close()



annotation_list1 = genome1.split('>')
genome1_proteins= []
genome2_proteins = []

for protein in annotation_list1:
    protein = protein.split('\n')
    temp = protein[1:]
    name = protein[0]
    if ' ' in name:
        name = protein[0].split(' ',1)[1]
    sequence = ''
    genome1_proteins.append((name, sequence.join(temp).replace('\n','')))


annotation_list2 = genome2.split('>')
for protein in annotation_list2:
    protein =protein.split('\n')
    temp = protein[1:]
    name = protein[0]
    if ' ' in name:
        name = protein[0].split(' ',1)[1]
    sequence = ''
    genome2_proteins.append((name, sequence.join(temp).replace('\n','')))

identical = set() #annotation and sequence present in both genomes
difference1 = [] #present in genome 1 but not in genome 2
difference2 = [] #present in genome 2 but not in genome 1
for protein in genome1_proteins:
    if protein not in genome2_proteins:
        difference1.append(protein)
    else:
        identical.add(protein)


for protein in genome2_proteins:
    if protein not in genome1_proteins:
        difference2.append(protein)
    else:
        identical.add(protein)



different_annotation = set() #sequences with different annotations but present in both
genome1_unique = [] #sequences found in only genome 1
genome2_unique = [] #sequences found in only genome 2

for tuple1 in difference1:
    for tuple2 in difference2:
        if tuple1[1] == tuple2[1]:
            different_annotation.add((tuple1,tuple2)) 
            break
    else: #if no matching sequences are found
        genome1_unique.append(tuple1)

for tuple1 in difference2:
    for tuple2 in difference1:
        if tuple1[1] == tuple2[1]:
            different_annotation.add((tuple2,tuple1)) 
            break
    else: #if no matching sequences are found
        genome2_unique.append(tuple1)


print(len(identical),'number of identically annotated sequences')
print(len(different_annotation),'number of differently annotated sequences')
print('There are',len(genome1_unique),'number of sequences only in the first file and',len(genome2_unique), 'number of sequences found only in the second file')

out1= input('Enter output filename for identical annotations\n>>> ')
out2 = input('Enter output filename for non identical annotation \n>>> ')
file = open(out1,'w')
for prot in identical:
    file.write('>')
    file.write(prot[0])
    file.write('\n')
    file.write(prot[1])
    file.write('\n')
file.close()
file = open(out2,'w')
for prots in different_annotation:
    file.write('>' + file1 + ' ')
    file.write(prots[0][0])
    file.write('\n')
    file.write('>' + file2 + ' ')
    file.write(prots[1][0])
    file.write('\n')
    file.write(prots[0][1])
    file.write('\n')
    file.write('\n')

file.close()