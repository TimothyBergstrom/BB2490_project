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
filename_path =  filedialog.askopenfilename(initialdir = curr_dir, title = "Select file",filetypes = (("mzML files", "*.mzML"),("all files","*.*")))
if filename_path == '':
    quit()
filename = filename_path.split('/')[-1]
file_folder =  '/'.join(filename_path.split('/')[0:-1])
os.chdir(file_folder)
if not os.path.exists(filename + "_splitted"):
    os.makedirs(filename + "_splitted")
splits = int(input('How many files do you want to split into? : '))

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
amount_of_chromatogram = 0
for line in open(filename_path, 'rb'):
    amount_of_lines += 1
    if b"<spectrum " in line:  # blankspace is important
        amount_of_spectrum += 1
    elif b"<chromatogram " in line:  # blankspace is important
        amount_of_chromatogram += 1

print(f"Counted {amount_of_lines} lines, {amount_of_spectrum} spectrums and {amount_of_chromatogram} chromatograms, "
      f"it took {round(time.time() - start_time, 2)} seconds with Python")

print("Finding header and footer")
widgets = ['Parsing: ', progressbar.Bar('='), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]
pbar = progressbar.ProgressBar(widgets=widgets, maxval=amount_of_lines)
pbar.start()

header = []
footer = []
record_header = True
record_footer = False
for i, line in enumerate(open(filename_path, 'rb')):
    if record_header:  # header is always the same
        header.append(line)
        if b"<run" in line:
            header_end = i
            record_header = False
    elif b"<spectrumList" in line:
        spectrum_list_line = line
    elif b"</spectrumList" in line:
        record_footer = True
        spectrum_list_line_end = line
        footer_start = i
    elif record_footer:
        footer.append(line)
    pbar.update(i)
pbar.finish()

def create_chunk_file(header, footer, file_contents, id_list, spectrum_in_file, file_num):
    widgets = ['Dividing: ', progressbar.Bar('='), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=amount_of_lines)
    pbar.start()
    i = 0
    compiled_regex_idRef = re.compile('idRef="(.+?)"')
    with open(f"{filename}_splitted/split{file_num}_" + filename, "wb") as file:
        for line in header:
            file.write(line)
            i += 1
            pbar.update(i)
        m = re.sub('count="(.+?)"',
                   f'count="{str(spectrum_in_file)}"',
                   spectrum_list_line.decode('utf-8'))
        file.write(m.encode())
        i += 1
        pbar.update(i)
        for line in file_contents:
            file.write(line)
            i += 1
            pbar.update(i)
        indices_spectrum = False
        for line in footer:
            if b'<index name="spectrum"' in line:
                indices_spectrum = True
            elif b"</index>" in line:
                indices_spectrum = False
            if indices_spectrum:
                if b'<offset idRef' in line:
                    m = compiled_regex_idRef.search(line.decode('utf-8'))
                    found = m.group(1)
                    if found is not None:
                        if found in id_list:
                            file.write(line)
                            i += 1
                            pbar.update(i)
                        else:
                            i += 1
                            pbar.update(i)
                            continue
                    else:
                        file.write(line)
                        i += 1
                        pbar.update(i)
                else:
                    file.write(line)
                    i += 1
                    pbar.update(i)
            else:
                file.write(line)
                i += 1
                pbar.update(i)
    pbar.finish()

print("Dividing into chunks")
spectrum_per_file = amount_of_spectrum / splits
spectrum_in_file = 0
packed_spectrum = 0
file_num = 0
file_contents = []
id_list = []
spectrum_in_file_list = []
compiled_regex_id = re.compile('id="(.+?)"')
for i, line in enumerate(open(filename_path, 'rb')):
    split_filename = filename + f"_split{file_num}"
    if line in header:
        pass
    else:
        if b"<spectrumList" in line:
            continue
        elif (b"</spectrumList" in line or spectrum_in_file >= spectrum_per_file or packed_spectrum == amount_of_spectrum):
            file_contents.append(spectrum_list_line_end)
            print(f"Creating {file_num} out of {splits}")
            create_chunk_file(header, footer, file_contents, id_list, spectrum_in_file, file_num)
            file_num += 1
            id_list = []
            file_contents = []
            spectrum_in_file_list.append(spectrum_in_file)
            spectrum_in_file = 0
            if packed_spectrum == amount_of_spectrum:
                break

        if b"<spectrum " in line:
            m = compiled_regex_id.search(line.decode('utf-8'))
            found = m.group(1)
            id_list.append(found)
        if b"</spectrum>" in line:
            spectrum_in_file += 1
            packed_spectrum += 1

        file_contents.append(line)

for i, num in enumerate(spectrum_in_file_list):
    print(f"File split{i}_{filename} has {num} spectrum")

