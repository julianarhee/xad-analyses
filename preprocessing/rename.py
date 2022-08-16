#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   rename.py
@Time    :   2021/11/30 14:52:55
@Author  :   julianarhee 
@Contact :   juliana.rhee@gmail.com
 
'''
#%%
import os
import glob
import re
import argparse
import utils as util

#%%
def rename_raw_files(src_dirs, 
                    raw_fmt=r"NINJAV\_S\d{3}_S\d{3}_T\d{3}.MOV",
                    verbose=False):
    '''
    Rename transferred NINJAV files to match datestr format.

    Keyword Arguments:
        raw_fmt -- _description_ (default: {r"NINJAV\_S\d{3}_S\d{3}_T\d{3}.MOV"})
    '''
    for src in src_dirs:
        _, session = os.path.split(src)
        raw_movies = sorted([i for i in glob.glob(os.path.join(src, 'NINJA*.MOV'))\
            if re.findall(raw_fmt, i)], key=util.natsort)
        for fi, fpath in enumerate(raw_movies):
            matchstr = re.findall(raw_fmt, fpath)[0]
            date_name = fpath.replace(matchstr, session)
            new_name = '{}_{:0>3d}.MOV'.format(os.path.splitext(date_name)[0], fi)
            if verbose:
                print(new_name) 
            assert not os.path.exists(new_name), "Name exists: %s" % new_name
            os.rename(fpath, new_name)


def main():
    parser = argparse.ArgumentParser(description='Preprocessing steps.')
    parser.add_argument('-R','--rootdir', type=str, default='/Volumes/My Book/bandensis-dyad',
        help='Base name for directories. Example: /Volumes/My Book/bandensis-dyad')

    args = parser.parse_args()

    rootdir = args.rootdir
    src_dirs = sorted(glob.glob(os.path.join(rootdir, '2022*')), \
                    key=util.natsort)

    rename_raw_files(src_dirs)

    print("Done!")
    
if __name__ == '__main__':

    main()
