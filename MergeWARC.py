from warcio.archiveiterator import ArchiveIterator
from warcio.warcwriter import WARCWriter
import os
import string
import random
import click
import argparse
import datetime
import time

def random_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-p','--path', help='Localization of the patching files', default= "./PATCHING2019/")
parser.add_argument('-d','--destination', help='Destination of the patching files merged', default= "./Merge/")
parser.add_argument('-n','--filename', help='Filename_template of the patching files merged', default="patching-merged-{timestamp}-{random}.warc.gz")
parser.add_argument('-e','--extension', help='Extension of originated files', default="warc.gz")
parser.add_argument('-s','--size', help='Size of the files merged (MB)', type=int, default=100)
args = vars(parser.parse_args())

##criar um git, fazer o readme, requimerent.txt(versão python)

def namePatchingMergedFile(filename_template, destination):
    string_aux = filename_template
    if "{timestamp}" in filename_template:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        string_aux = string_aux.replace("{timestamp}", str(timestamp))
    if "{random}" in filename_template:
        random_generated = random_id_generator()
        string_aux = string_aux.replace("{random}", str(random_generated))
    if "{timestamp}" not in filename_template and "{random}" not in filename_template:
        raise ValueError('Filename without unique identifiers (e.g., timestamp).')
    if destination.endswith("/"):
        return destination + string_aux
    else:
        return destination + "/" + string_aux


def script():
    click.secho("Read inputs...", fg='green')
    ##Process input
    mypath = args['path']
    destination = args['destination']
    filename_template = args['filename']
    extension = args['extension']
    sizeFile = args['size'] * 1000000

    #Check if exists Directory of destination
    if not os.path.exists(destination):
        os.makedirs(destination)
    #Create the first WARC file
    filename = namePatchingMergedFile(filename_template, destination)
    output = open(filename  , 'wb')
    writer = WARCWriter(output, gzip=True)

    click.secho("Starting merge warcs patching...", fg='green')
    #import pdb;pdb.set_trace()
    for subdir, dirs, files in os.walk(mypath):
        with click.progressbar(length=len(files), show_pos=True) as progress_bar:
            for file in files:
                progress_bar.update(1)
                if file.endswith(extension):
                    file_name = os.path.join(subdir, file)
                    with open(file_name, 'rb') as stream:
                        for record in ArchiveIterator(stream):
                            if os.path.getsize(filename) > sizeFile and record.rec_type == 'request':
                                output.close()
                                filename = namePatchingMergedFile(filename_template, destination)
                                output = open(filename, 'wb')
                                writer = WARCWriter(output, gzip=True)
                            writer.write_record(record)

if __name__ == '__main__':
    script()