#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2022/08/15 14:43:12
@Author  :   julianarhee 
@Contact :   juliana.rhee@gmail.com
'''

import re
import os
import glob

# ---------------------------------------------------------------------
# General
# ---------------------------------------------------------------------
natsort = lambda s: [int(t) if t.isdigit() \
    else t.lower() for t in re.split('(\d+)', s)]

def flatten(t):
    return [item for sublist in t for item in sublist]


# ---------------------------------------------------------------------
# File tree 
# ---------------------------------------------------------------------
def print_and_select_session(rootdir='/Volumes/My Book/bandensis-dyad'):
    '''
    Print all sessions found in <ROOTDIR>, then allow user to select by index.

    Keyword Arguments:
        rootdir -- path to parent dir of all sessions (default: {'/Volumes/My Book/bandensis-dyad'})

    Returns:
        full path to video source dir
    '''
    src_dirs = sorted(glob.glob(os.path.join(rootdir, '2022*')), \
                key=natsort)
    for i, sdir in enumerate(src_dirs):
        print("{}: {}".format(i, os.path.split(sdir)[-1]))

    session_idx = int(input("Select IX of session to trim: "))
    src_dir = src_dirs[session_idx]

    return src_dir #session

