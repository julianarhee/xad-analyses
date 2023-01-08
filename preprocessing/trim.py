#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   trim.py
@Time    :   2022/08/15 21:14:50
@Author  :   julianarhee 
@Contact :   juliana.rhee@gmail.com

Load timestamp param file and trim movie.

'''
#%%
import sys
import os
import re
import glob
import time
import json
import shutil
import argparse
#import cv2
import utils as util

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

#%%
def get_start_and_end_sec(start_time, end_time, time_in_sec=False):
    '''
    Get start and end time in sec.
    
    Args:
    -----
    start_time, end_time: (str or float)
        If str, must be format:  'HH:MM:SS.ms' (estimated with VLC)
        If int, assumes all the way to end (100)
       
    time_in_sec: (bool)
        If an INT is provided for either start_time or end_time, specifies whether the number is in seconds or minutes
        Set to False if in minutes (e.g., 100 minutes to get full video, a big number). 
    '''
    tstamps=[] 
    for tstamp in [start_time, end_time]:
        if isinstance(tstamp, str):
            # Get start time in sec 
            hours, minutes, secs = [float(i) for i in tstamp.split(':')]
            #print(hours, minutes, secs)
            tstamp_sec = (hours*60.*60.) + (minutes*60.) + secs
        else:
            tstamp_sec = float(tstamp) if time_in_sec else float(tstamp)*60. 
        tstamps.append(tstamp_sec) 
    print("TIME:", tstamps)

    return tstamps #tstamps[0], tstamps[1]


#%%
def create_trimmed_movie_name(input_movie, epoch='nobarrier',
                rootdir='/Users/julianarhee/Movies/grass2022/canon-bandensis'):
    '''
    _summary_

    Arguments:
        input_movie -- full path to movie to trim

    Keyword Arguments:
        epoch -- append to new movie name (default: 'nobarrier')
        rootdir -- parent dir of movies (default: '/Volumes/My Book/bandensis-dyad')

    Returns:
        new movie name (e.g., input_movie_EPOCH.MOV)
    '''
    #session = os.path.split(src_dir)[-1]
    src_dir, movname = os.path.split(input_movie)
    _, session = os.path.split(src_dir)
    mov_fn, fext = os.path.splitext(movname)
    output_movie = os.path.join(rootdir, session, '{}_{}{}'.format(mov_fn, epoch, fext))
    #print("Orig MOV: %s" % mov_fn)

    return output_movie

def trim_movie_epoch(input_movie, start_time_sec, end_time_sec, output_movie=None, overwrite=False,
                    epoch='nobarrier', verbose=True, rootdir='/Users/julianarhee/Movies/grass2022/canon-bandensis'):
    '''
    Trim movie

    Arguments:
        input_movie -- full path to movie file
        start_time -- start time in sec
        end_time -- end time in sec

    Keyword Arguments:
        epoch -- trial epoch, appended to trimmed movie name (default: 'nobarrier')
        verbose -- print lots of stuff (default: True)
    '''

    # create trimmed movie name
    if output_movie is None:
        output_movie = create_trimmed_movie_name(input_movie, epoch=epoch,
                            rootdir=rootdir)

    # Make sure movie not already cropped
    if os.path.exists(output_movie):
        print("    Movie already cropped, check: %s\n Aborting CROP." % input_movie)
        if not overwrite: 
            return

    if verbose:
        print("    Input: %s" % input_movie)
        print("    Output: %s" % output_movie)

    #%
    #start_time_sec, end_time_sec = get_start_and_end_sec(start_time, end_time)
    #if verbose:
    #    print("    Trim settings: {:.2f}-{:.2f} sec".format(start_time_sec, end_time_sec))

    #%
    # Cropy movie and save
    t = time.time()
    ffmpeg_extract_subclip(input_movie, start_time_sec, end_time_sec, 
                        targetname=output_movie)
    elapsed = time.time() - t
    print('Elapsed: {:2f}'.format(elapsed))
    print("Done trimming movie.")

#%%
#rootdir = '/Volumes/My Book/bandendsis-dyad'
#session = '20220810-0945-bandensis_L-yuna_R-valtteri'
#filenum = 0
#epoch = 'nobarrier'
#
#start_time = '33:12'
#end_time = 200
#
#trim_movie_epoch(session, filenum, start_time, end_time, 
#                epoch=epoch, verbose=True)


def process_session_movies(src_dir, epoch='nobarrier', overwrite=False,
        rootdir='/Users/julianarhee/Movies/grass2022/canon-bandensis'):
    '''
    Load params specifying trial epoch, trim movie.

    Arguments:
        src_dir -- full path to parent dir containing movies
        epoch -- key of params dict with timestamps 
    '''
    new_movies = []

    session = os.path.split(src_dir)[-1]
    # load trial epoch params
    proc_fname = '%s.json' % session
    proc_input_file = os.path.join(src_dir, proc_fname)
    assert os.path.exists(proc_input_file), \
        "No param file for trial epochs: %s" % src_dir

    with open(proc_input_file, 'r') as f:
        procparams = json.load(f)

    # load params and trim 
    movie_fnames = sorted(procparams.keys(), key=util.natsort)
    mi=0
    for movie_fname, movie_params in procparams.items():
        mi+=1
        epochs = [k for k in movie_params.keys() if k!='filepath']
        if epoch not in epochs:
            continue
        print("Processing {} of {} movies".format(mi, len(movie_fnames)))
        input_movie = movie_params['filepath']
        start_t, end_t = movie_params[epoch]

        output_movie = create_trimmed_movie_name(input_movie, epoch=epoch, 
                            rootdir=rootdir)
        print("Creating clip: {}".format(output_movie))

        # check if movie already processed 
        if start_t==0 and end_t==200: # full movie, just rename
            print("Renaming movie with epoch: {}".format(output_movie))
            os.rename(input_movie, output_movie)
        else:
            # convert to secs
            start_time, end_time = get_start_and_end_sec(
                                        start_t, end_t, time_in_sec=False)
            # trim  
            trim_movie_epoch(input_movie, float(start_time), float(end_time), 
                    epoch=epoch, verbose=True, output_movie=output_movie,
                    overwrite=overwrite, rootdir=rootdir)

        new_movies.append(output_movie)

    print("-----------------------------------------")
    print("Done processing movies. Created %i new movies:" % len(new_movies))
    for i in new_movies:
        print("  {}".format(i))
    print("Done!")

    return new_movies

#%%
def main():
    parser = argparse.ArgumentParser(description='Preprocessing steps.')
    parser.add_argument('-R', '--rootdir', type=str, default='/Volumes/My Book/bandensis-dyad',
        help='Base name for directories. Example: /Volumes/My Book/bandensis-dyad')
    parser.add_argument('-S', '--session', type=str, default='',
        help='Session name. Example: 20220810-0945-bandensis_L-yuna_R-valtteri')
    parser.add_argument('-E', '--epoch', type=str, default='nobarrier',
        help='Trial epoch to extract (default: nobarrier)')
    parser.add_argument('-O', '--overwrite', default=False, action='store_true',
        help='Overwrite clip if it exists (default: false)')

    args = parser.parse_args()
    rootdir = args.rootdir
    epoch = args.epoch
    overwrite = args.overwrite

    # select session
    if args.session == '':
        src_dir = util.print_and_select_session(rootdir=rootdir)
        session = os.path.split(src_dir)[-1]
    else:
        session = args.session
        src_dir = os.path.join(rootdir, session)
        assert os.path.exists(src_dir), "Speified src does not exist: %s" % src_dir

    try:
        new_movies = process_session_movies(src_dir, epoch=epoch, overwrite=overwrite, rootdir=rootdir)

        # move untouched movies to 'raw' dir
        rawdir = os.path.join(src_dir, 'raw')
        if not os.path.exists(rawdir):
            os.makedirs(rawdir)
        all_movs = glob.glob(os.path.join(src_dir, '*.MOV'))
        raw_movs = [f for f in all_movs if re.findall('_\d{3}.MOV', f)]    
        for fn in raw_movs:
            fname = os.path.split(fn)[-1]
            shutil.move(fn, os.path.join(rawdir, fname))    
    except Exception as e:
        print(e)


    
#%%
if __name__ == '__main__':

    main()

#%%

#rootdir = '/Users/julianarhee/Movies/grass2022/canon-bandensis'
#session = '20220806-1045-bandensis_L-esteban_R-simone'
#epoch = 'nobarrier'
#src_dir = os.path.join(rootdir, session)
#assert os.path.exists(src_dir), "Speified src does not exist: %s" % src_dir
#
##%%
#
#new_movies = []
#
#session = os.path.split(src_dir)[-1]
## load trial epoch params
#proc_fname = '%s.json' % session
#proc_input_file = os.path.join(src_dir, proc_fname)
#assert os.path.exists(proc_input_file), \
#    "No param file for trial epochs: %s" % src_dir
#
#with open(proc_input_file, 'r') as f:
#    procparams = json.load(f)
#
## load params and trim 
#movie_fnames = sorted(procparams.keys(), key=util.natsort)
#
#


