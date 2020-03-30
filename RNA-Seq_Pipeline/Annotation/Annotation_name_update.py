"""
Fixing names in annotation to match the more meaningful names in cDNA file
Using gene IDs to search for gene IDs in 

updated 170717 by Ronald Cutler 
"""
import sys

def main( annotation, cDNA):
	cDNA_names = []
	cDNA_IDs = []
	
	with open( cDNA, 'r') as reader1:
			for line in reader1:
				if '>' in line:
					cDNA_names.append(line[1:].rstrip('\n'))
					cDNA_IDs.append(line.split('|')[1].rstrip('\n'))

	with open( annotation, 'r' ) as annotReader:
		with open( annotation + "_new.gff3", 'w' ) as annotWriter:
			rewrite = False
			for line in annotReader:
				if "#" in line:
					annotWriter.write(line)
					continue

				split_line = line.split('\t')

				if split_line[2] == "gene":
					field_8 = split_line[8].split(';')
					name = field_8[1].rstrip('\n')
					ID = name.split('|')[1]
					if ID in cDNA_IDs:
						rewrite = True
						index = cDNA_IDs.index(ID)
						new_name = "Name=" + cDNA_names[index]
						split_line[8] = field_8[0] + ';' + new_name + '\n'
						new_line = '\t'.join(split_line)
						annotWriter.write(new_line)
					else:
						rewrite = False
						annotWriter.write(line)

				elif ((rewrite == True) and ((split_line[2] == "CDS") or (split_line[2] == "exon") or (split_line[2] == "mRNA"))):
					field_8 = split_line[8].split(';')
					field_8[1] = new_name
					split_line[8] = ';'.join(field_8)
					new_line = '\t'.join(split_line)
					annotWriter.write(new_line)

				else:
					rewrite = False
					annotWriter.write(line)

if __name__ == "__main__":
	main( sys.argv[1], sys.argv[2] )