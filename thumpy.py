#! /usr/bin/env python
# -.- coding: utf-8 -.-

from __future__ import print_function
import os, os.path, sys
from PIL import Image
import click


Image.MAX_IMAGE_PIXELS = None # prevent "Decompression Bomb", Error https://stackoverflow.com/questions/25705773/image-cropping-tool-python

def make_thumb(path, fn, tgt_dir, sz, prefix):
    size = (sz, sz)
    """Make image thumbnail"""
    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)
    infile = os.path.join(path, fn)
    out_filename = 'tn_{}'.format(fn) if prefix == 'y' else fn
    outfile = os.path.join(tgt_dir, out_filename)
    print('Making thumbnail: ' + infile, '=> ', outfile)
    try:
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(outfile, "JPEG")
        return True
    except IOError:
        print('Failed: ', infile)
        return False


def check_image(fname):
    """Validate the image"""
    # check extension
    _, ext = os.path.splitext(fname)
    # only process JPEG
    if ext in ('.jpg', '.JPG', '.JPEG', '.jpeg', '.png', '.PNG'):
        return True
    else:
        return False


@click.command()
@click.option('--src_dir', '-i', prompt='source dir', default = '.',
              help='source directory to make thumbnails')
@click.option('--tgt_dir', '-o', prompt='target dir', default = 'thumbnails',
              help='target directory to save thumbnails')
@click.option('--size', '-s', prompt='size', default=650,
              help='thumbnails size')
@click.option('-k', prompt='keep struct (y/n)', type=click.Choice(['y', 'n']), default='n',
              help='To keep the directory structure')
@click.option('-x', prompt='tn_ prefix (y/n)', type=click.Choice(['y', 'n']), default='y',
              help='add tn_ prefix ?')
def main(src_dir, tgt_dir, size, k, x):
    """Batch make image thumbnails."""
    count = 0
    for path, dirs, files in os.walk(src_dir, topdown=False):
        #print(path, dirs, files)
        for name in files:
            fname = os.path.join(path, name)
            path_out = ''
            if check_image(fname):
                if k == 'y':
                    k_path = path[len(src_dir)+1:]
                    path_out = os.path.join(tgt_dir, k_path)
                else:
                    path_out = tgt_dir
                is_done = make_thumb(path, name, path_out, size, x)
                if is_done:
                    count = count + 1
            else:
                print('skip: ',fname)
    print('# thumbs: ', count)



if __name__ == '__main__':
    main()
