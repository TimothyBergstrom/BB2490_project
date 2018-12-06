import os
from tkinter import filedialog, Tk
import time
try:
    import progressbar
except:
    print("Progressbar not installed, install with:")
    print("pip install progressbar2")
import re

curr_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(curr_dir)

root = Tk()
root.withdraw()
filename_path = filedialog.askopenfilename(initialdir = curr_dir, title = "Select file",filetypes = (("mzML files", "*.mzML"),("all files","*.*")))
if filename_path == '':
    quit()
filename = filename_path.split('/')[-1]
file_folder =  '/'.join(filename_path.split('/')[0:-1])
os.chdir(file_folder)

print("Counting lines")
start_time = time.time()
amount_of_lines = 0
amount_of_spectrum = 0
amount_of_chromatogram = 0
amount_of_spectrum_indices = 0
amount_of_chromatogram_indices = 0
indices_spectrum = False
indices_chromatogram = False
compiled_regex_idRef = re.compile('idRef="(.+?)"')
for line in open(filename_path, 'rb'):
    amount_of_lines += 1
    if b"<spectrum " in line:  # blankspace is important
        amount_of_spectrum += 1
    elif b"<chromatogram " in line:  # blankspace is important
        amount_of_chromatogram += 1
    if b'<index name="spectrum"' in line:
        indices_spectrum = True
    elif b"</index>" in line:
        indices_spectrum = False
    if indices_spectrum:
        if b'<offset idRef' in line:
            m = compiled_regex_idRef.search(line.decode('utf-8'))
            found = m.group(1)
            if found is not None:
                amount_of_spectrum_indices += 1
    if b'<index name="chromatogram"' in line:
        indices_chromatogram = True
    elif b"</index>" in line:
        indices_chromatogram = False
    if indices_chromatogram:
        if b'<offset idRef' in line:
            m = compiled_regex_idRef.search(line.decode('utf-8'))
            found = m.group(1)
            if found is not None:
                amount_of_chromatogram_indices += 1

print(f"Counted {amount_of_lines} lines")
print(f"{amount_of_spectrum} spectrums and {amount_of_chromatogram} chromatograms")
print(f"{amount_of_spectrum_indices} indices for spectrum")
print(f"{amount_of_chromatogram_indices} indices for chromatogram")
print(f"it took {round(time.time() - start_time, 2)} seconds with Python")