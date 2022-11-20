# preprocessing steps
Huge .MOV files are trimmed, split, then compressed for better data transfer and handling. Use `pymov` environment.

#### Identify trial epochs
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

#### Split and compress videos
Find all .MOV files in each session folder (currently assumes there is just 1), then save 10-min clips in a subfolder with the same name as the video.
```
$ bash split_and_compress.sh [rootdir]
```
Here, `rootdir` is the same as above, but specifically, contains <session> subfolders, each containing 1 huge .MOV that needs to be split and compressed.




