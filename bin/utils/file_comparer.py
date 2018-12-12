import os
from tkinter import filedialog, Tk
curr_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(curr_dir)

root = Tk()
root.withdraw()
filename1_path =  filedialog.askopenfilename(initialdir = curr_dir, title = "Select file 1")
file_folder =  '/'.join(filename1_path.split('/')[0:-1])
filename2_path =  filedialog.askopenfilename(initialdir = file_folder, title = "Select file 2")

file1 = open(filename1_path, "rb")
file2 = open(filename2_path, "rb")

i = 0
for line1, line2 in zip(file1, file2):
    if line1 == line2:
        i += 1
    else:
        print(f"Not same in line {i+1}")
        print(line1)
        print(line2)
        quit()

print("Same contents")