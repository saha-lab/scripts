
file_path = input("What is the path to the .txt file you wish to process:\n>>> ")
file = open(file_path)

DE_genes = file.read()
file.close()

gene_list = DE_genes.split('\n')
final_list = []

for line in gene_list:
    line = line.split('_')
    temp = line[0:2]
    gene_name = ''
    gene_name = gene_name.join(temp)
    final_list.append(gene_name)

output= input('Enter output filename\n>>> ')

file = open(output,'w')
for gene in final_list:
    file.write(gene)
    file.write('\n')

file.close()