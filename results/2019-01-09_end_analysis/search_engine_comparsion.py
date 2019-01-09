import matplotlib.pyplot as plt

file_list = ["Quantification_comet_fdr.csv",
             "Quantification_crux_fdr.csv",
             "Quantification_msfg_fdr.csv",
             "Quantification_msfg_percolator.csv"]
file_titles = ["Comet",
               "Crux",
               "MSGFPlus",
               "MSGFPlus + Percolator"]

protein_list = []
peptides_list = []

for file_name in file_list:
    proteins = 0  # n of proteins
    peptides = 0
    for line_index, line in enumerate(open(file_name, 'r')):
        if line_index > 3:  # Proteins are listed after row 4
            proteins += 1
            peptides += int(line.split('\t')[3])  # n_peptides is in column 4
    protein_list.append(proteins)
    peptides_list.append(peptides)
    print(f"{file_name} is done")

plt.bar(file_titles,
        protein_list,
        color=['black', 'red', 'green', 'blue', 'cyan'],
        edgecolor='blue')
plt.title("Comparing proteins found")
plt.ylabel("Number of proteins matched")
plt.tight_layout()  # Fixes cut off labels
plt.savefig("search_engines_proteins.png")

plt.bar(file_titles,
        peptides_list,
        color=['black', 'red', 'green', 'blue', 'cyan'],
        edgecolor='blue')
plt.title("Comparing amount of peptides matched")
plt.ylabel("Total amount of peptides matched")
plt.tight_layout()  # Fixes cut off labels
plt.savefig("search_engines_peptides.png")

