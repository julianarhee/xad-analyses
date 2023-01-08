# Preprocess raw videos for analysis
Takes huge vidoes (100s GB) and splits and compresses them into manageable chunks. 

## setup
Runs on Mac M1 (also Ubuntu 20 LTS). Uses ffmpeg with libx265 compression. 

Start miniforge env (is using Apple M1) called `pymov`
```
source ~/miniforge3/bin/activate 
conda activate pymov
```

## preprocessing steps
Huge .MOV files are trimmed, split, then compressed for better data transfer and handling. Use `pymov` environment.

#### identify trial epochs
1. Manually define timestamps to mark trial epochs, e.g., barrier, nobarrier, etc. 
```
$ python set_timestamps.py -R [rootdir] -S [session]
``` 
Specify `rootdir` as base directory with all session or trial data. Provie full trial or session name for `session` (format `YYYYMMdd-HHmm-bandensis_L-foo_R-bar`)

2. Trim videos into epochs.
```
$ python trim.py -R [rootdir] -S [session] -E [epoch]
```
Trim out specific trial epoch. Currently, only tested with `nobarrier` epoch. TODO: aggregate pre/barrier epochs into 1 vid. Moves all the raw videos into a `raw` dir in the src folder.

#### split and compress videos
Find all .MOV files in each session folder (creates a subdir for each .MOV file found), then save 10-min clips in a subfolder with the same name as the video.
```
# First, split and save movie chunks
$ bash split_movies.sh [moviedir]

# Then, compress movie chunks into a subsubdir
$ sh compress_clips.sh [moviedir]
```
- Here, `moviedir` is the same as above, but specifically, contains <session> subfolders, each containing 1 huge .MOV that needs to be split and compressed. For example, `/Users/julianarhee/Movies/grass2022/canon-bandensis/20220817-1415-bandensis_L-max_R-esteban`. Does this for each clip subfolder found in the main session dir.





