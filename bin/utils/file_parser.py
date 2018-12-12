import os
from tkinter import filedialog, Tk
curr_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(curr_dir)
root = Tk()
root.withdraw()
filename_path =  filedialog.askopenfilename(initialdir = curr_dir, title = "Select file 1")
file_folder =  '/'.join(filename_path.split('/')[0:-1])

with open(filename_path, 'r') as file:
    for line in file:
        print(line, end='\r')
        str(input(''))
