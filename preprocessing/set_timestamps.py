#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   set_timestamps.py
@Time    :   2022/08/15 15:45:50
@Author  :   julianarhee 
@Contact :   juliana.rhee@gmail.com

Manually enter time stamps for selected movie(s) and save params to file.

'''
#%%
import sys
import os
import re
import glob
import time
import json
import argparse
import utils as util

#%%

def main():
    parser = argparse.ArgumentParser(description='Preprocessing steps.')
    parser.add_argument('-R','--rootdir', type=str, default='/Volumes/My Book/bandensis-dyad',
        help='Base name for directories. Example: /Volumes/My Book/bandensis-dyad')
    parser.add_argument('-S','--session', type=str, default='',
        help='Session name. Example: 20220810-0945-bandensis_L-yuna_R-valtteri')

    args = parser.parse_args()

    rootdir = args.rootdir

    # select session
    if args.session == '':
        src_dir = util.print_and_select_session(rootdir=rootdir)
        session = os.path.split(src_dir)[-1]
    else:
        session = args.session
        src_dir = os.path.join(rootdir, session)

    # Check for existing params
    proc_fname = '%s.json' % session
    proc_input_file = os.path.join(src_dir, proc_fname)
    if os.path.exists(proc_input_file):
        with open(proc_input_file, 'r') as f:
            procparams = json.load(f)
    else:
        procparams={}

    # get file number (if >1)
    raw_fmt=r"%s_\d{3}.MOV" % session
    movie_fpaths = sorted([i for i in 
            glob.glob(os.path.join(src_dir, '{}*.MOV'.format(session)))\
            if re.findall(raw_fmt, i)], key=util.natsort)

    #movie_fpaths = sorted(glob.glob(os.path.join(src_dir, '{}*.MOV'.format(session))), 
    #                    key=util.natsort)
    print("Found %i movies" % len(movie_fpaths))

    for fpath in movie_fpaths: 
        _, fn = os.path.split(fpath)
        movie_fname = os.path.splitext(fn)[0]
        print("-------------------------------")
        print("Movie: {}".format(movie_fname))
        
        # get start/end times
        confirmed=False
        while not confirmed:
            start_t = input("Enter start time ('00:00:00.0' HH:mm:ss.ss): ") 
            end_t = input('Enter end time (hit ENTER to go to end of movie): ')
            if end_t is None or end_t=='':
                end_t = 200
            confirm = input("Start: %s, End: %s. Press Y/n to confirm: " % (str(start_t), str(end_t)))
            confirmed = confirm=='Y'

        # get epoch name (nobarrier)
        epoch = input("Enter name of trial epoch: ")

        # create params dict
        if movie_fname not in procparams.keys():
            procparams[movie_fname] = {}

        procparams[movie_fname].update({
            'filepath': fpath,
            epoch: (start_t, end_t)
        })

    # save params
    with open(proc_input_file, 'w') as f:
        json.dump(procparams, f, indent=4)

    print("Done!")
    
if __name__ == '__main__':

    main()
