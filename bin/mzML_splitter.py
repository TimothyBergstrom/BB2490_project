import xml.etree.ElementTree as ET
import os
from tkinter import filedialog, Tk
import time
import progressbar

curr_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(curr_dir)

root = Tk()
root.withdraw()
filename =  filedialog.askopenfilename(initialdir = curr_dir, title = "Select file",filetypes = (("mzML files", "*.mzML"),("all files","*.*")))
if filename == '':
    quit()
splits = input('How many files do you want to split into? : ')

"""
# C
from subprocess import Popen, PIPE
cproc = Popen("line_counter.exe", stdin=PIPE, stdout=PIPE, shell=True)  # Hide window
start_time = time.time()
out, err = cproc.communicate(str.encode(filename))
if err != None:
    print("Something went wrong.")
    print(err)
print(f"Counted {int(out.decode('utf-8'))} lines, it took {round(time.time() - start_time, 2)} seconds with C")
"""

# PYTHON
print("Counting lines")
start_time = time.time()
amount_of_lines = 0
amount_of_spectrum = 0
for line in open(filename, 'rb'):
    amount_of_lines += 1
    if b"<spectrum" in line:
        amount_of_spectrum += 1

print(f"Counted {amount_of_lines} lines and {amount_of_spectrum} spectrums, "
      f"it took {round(time.time() - start_time, 2)} seconds with Python")

print("Finding header and footer")
widgets = ['Parsing: ', progressbar.Bar('='), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]
pbar = progressbar.ProgressBar(widgets=widgets, maxval=amount_of_lines)
pbar.start()

header = []
footer = []
record_header = True
record_footer = False
file_num = 1
for i, line in enumerate(open(filename, 'rb')):
    if record_header:  # header is always the same
        header.append(line)
        if b"<run" in line:
            header_end = i
            record_header = False
    elif b"</spectrumList" in line:
        spectrum_list_line = line
    elif b"</spectrumList" in line:
        record_footer = True
        footer_start = i
    if record_footer:
        footer.append(line)
    pbar.update(i)
pbar.finish()

print("Dividing into chunks")
widgets = ['Dividing: ', progressbar.Bar('='), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]
pbar = progressbar.ProgressBar(widgets=widgets, maxval=amount_of_lines)
pbar.start()
file = 0
spectrum_in_file = amount_of_spectrum/splits
print(spectrum_in_file)
for i, line in enumerate(open(filename, 'rb')):
    if b"<spectrum" in line:
        pass
    pbar.update(i)
pbar.finish()


# JUNK

"""
tree = ET.parse(filename)
root = tree.getroot()

def unpack_tree(root):
    print(root.tag, root.attrib)
    for child in root:
        unpack_tree(child)

"""
