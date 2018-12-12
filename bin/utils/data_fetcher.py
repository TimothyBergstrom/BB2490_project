import urllib.request
import sys
import progressbar
import time

def show_progress(block_num, block_size, total_size):
    global pbar
    global i
    if pbar is None:
        widgets = ['Downloading: ', progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.AnimatedMarker()),
                   ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

amount_of_links = 0
for url in open('url_list.txt', 'r'):
    amount_of_links += 1

print(f'{amount_of_links} urls found')
for i, url in enumerate(open('url_list.txt', 'r')):
    pbar = None
    filename = url.split('/')[-1]
    filename = filename.replace('\n', '')
    print(f'Downloading {filename} from {url}')
    urllib.request.urlretrieve(url, 'mzML_data/'+filename, show_progress)
    print('')
    print(f'{i+1} out of {amount_of_links} done')
