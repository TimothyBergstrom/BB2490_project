import matplotlib.pyplot as plt
from csv_merger import merge_csv
import math
import numpy as np
from numpy.polynomial.polynomial import polyfit

def log2(l):
    root = l[0]  # lowest possible co2 or light level
    if root == 0:
        root = 1  # lowest possible abundance
    new_list = []
    for i in l:
        if i == 0:
            i = 1  # lowest possible abundance
        new_list.append(math.log2(i/root))
    return new_list

def mean_replicates(replicates, l):
    new_l = []
    for i in range(0, len(l), replicates):
        new_l.append(sum(l[i:i+replicates])/replicates)
    return new_l

annotated_file = "all_annotations.csv"
file_to_merge = "ProteinQuantifier_top0_sum.csv"
merged_file = "merged_file.csv"
look_for = "DNA replication"

merge_csv(annotated_file, file_to_merge, merged_file)
print("Merging csv files completed")

light_levels_files = [1000, 100, 200, 300, 60]  # ORDER
co2_levels_files = [0.15, 0.20, 0.30, 0.50, 1.00]

light_levels = []
co2_levels = []

for i, line in enumerate(open(merged_file, 'r')):
    if look_for in line:
        line = line.split(',')

        l = [int(i) for i in line[4:14]]
        l = mean_replicates(2, l)
        light_levels.append(l)

        l = [int(i) for i in line[14:24]]
        l = mean_replicates(2, l)
        co2_levels.append(l)

print(len(light_levels), "proteins found matching string:", look_for)
store_proteins = []
store_levels = []
for protein in light_levels:
    protein = [i for _,i in sorted(zip(light_levels_files, protein))]
    protein = log2(protein)  # log2 based on 60
    plt.plot(sorted(light_levels_files), protein, alpha=0.1)
    store_proteins.extend(protein)
    store_levels.extend(sorted(light_levels_files))

b, m = polyfit(store_levels, store_proteins, 1)
reg = plt.plot(light_levels_files,
               [b + m * i for i in light_levels_files],
               color="black",
               label="Linear regression of points",
               linewidth=4)
plt.legend()
plt.title(f'Light, with search string: "{look_for}", {len(light_levels)} matched proteins')
plt.ylabel("log2 ratio from lowest value (aka 60 µmol photons m-2 s-1)")
plt.xlabel("Light level")
plt.savefig("light.png")
plt.clf()

store_proteins = []
store_levels = []
for protein in co2_levels:
    protein = [i for _,i in sorted(zip(co2_levels_files, protein))]
    protein = log2(protein)  # log2 based on 0.15
    plt.plot(sorted(co2_levels_files), protein, alpha=0.1)
    store_proteins.extend(protein)
    store_levels.extend(sorted(co2_levels_files))

b, m = polyfit(store_levels, store_proteins, 1)
reg = plt.plot(co2_levels_files,
               [b + m * i for i in co2_levels_files],
               color="black",
               label="Linear regression of points",
               linewidth=4)
plt.legend()
plt.title(f'CO2, with search string: "{look_for}", {len(light_levels)} matched proteins')
plt.ylabel("log2 ratio from lowest value (aka 0.15% CO2 atmosphere)")
plt.xlabel("CO2 level")
plt.savefig("co2.png")
