# Advanced Usage

### Table of Contents
* [Input](#Input)
* [Output](#Output)
* [Features](#Features)
* [Optional Arguments](#Optional-Arguments)
* [Performance](#Performance)
* [Detailed Description](#Detailed-Description)


<br/><br/>
## Input
You can supply as arguments any combination of videos and directories.

This program will assume all arguments are either videos or directories containing videos, unless the argument begins with --.
If no files or directories are given, the program will use the current working directory.

Directory searches are recursive by default. Disable this with the --nonrecursive option.
Only directories given AFTER the --nonrecursive option will be nonrecursive.


<br/><br/>
### Merge
Simply place the result file in the same directory as the videos you are processing.\
Alternatively, you can explicitly give the absolute path of the result file as an argument.\
Example:\
`python ds3_rc.py /path/to/videos/ /path/to/ds3_rc_results.txt`

The filename must begin with "ds3_rc_results".
You can merge multiple result files.



What video formats are allowed?\
Anything that OpenCV can read. This program uses only very basic error checking in regards to reading a file as a video.


How can I skip some files in a folder?\
Use your CLI's glob / wildcard capabilities.\
Example using Windows PowerShell:\
`python C:\Users\jhalb\Downloads\ds3_rc.py $(dir C:\Users\jhalb\Videos\*.mp4)`

Example using Bash:\
`python3 /home/jhalb/code/ds3_rc.py /home/jhalb/videos/*.mp4`


<br/><br/>
## Output
This program outputs the results in JSON / Python dictionary format. The key is the player name and the value is a list of file paths (the names of the videos in which the player's name was found).\
Example output file:
```
{
"Motion_1": ["/path/to/video1.mkv"],

"Noob_Slayer_2": ["/path/to/video3.mp4", "/path/to/video1.mkv", "/path/to/video4.mkv"]
}
```


<br/><br/>
## Features

#### Resumption
This program saves its progress to a file after each video is processed. This allows for a resumption feature which serves three purposes:
1. If an error occurs, you don't need to start over from the beginning.
2. When you add new videos to the directory and run this program again, it will skip videos which have already been processed.
3. Merge previous results to create a single combined output file.

To use this resumption feature, supply an result file as an argument when you run the program.\
This can be done one of two ways:
1. Place the result file in one of the directories supplied in the arguments; or
2. Give the absolute path of the result file as an argument.

The results filename must start with "ds3_rc_results".


<br/><br/>
#### Skip same filename in different locations?
By default this program will skip videos with the same filename, even if they are in different folders.\
Example (the second video will be skipped):\
C:\Users\jhalb\Desktop\video_1.mkv\
C:\Users\jhalb\Videos\DS3\pvp\video_1.mkv	

This is done to allow use of symlinks.
To skip videos only when they have the same name and location invoke the `--noskip` option.


<br/><br/>
## Performance
Reading and processing video data is slow. It is mostly dependent on your CPU and the video resolution.
I have made every effort to make this program as fast as possible.


<br/><br/>
## Detailed Description

The program begins by putting all the videos to be processed into a list.

Two threads are started. One thread extracts frames from the video and puts the frames in to a queue. The other thread takes a frame from the queue and processes it.

Frame extraction thread\
This thread iterates over every video in the list. Videos are read using CV2 (OpenCV) and frames are stored as Numpy arrays.\
Every 67th frame (assuming a 60 fps video) is extracted because that is the minimum sampling rate required to guarantee nameplate recognition. The nameplate appears three times, fading to transparent in between. This program aims to select a frame containing the nameplate at least one of the three times when it is completely opaque. Choosing a less frequent sampling rate would increase performance, but decrease the quality of the results.

Frame processing thread\
After a frame is taken from the queue, it is cropped to a small area near the top of the nameplate. The average brightness of this small area is determined. If the brightness is too high, then it is assumed that a nameplate message is not present and the frame is discarded.

If a nameplate is determined to likely be present, then the nameplate is cropped where the text is located.

At this time the frame is converted to an image using PIL. Optical character recognition using PyTesseract (Tesseract) is performed.

If an appropriate phrase is detected (such as "Invaded the World of...", "Phantom ... has died", etc), then the player name is appended to the result (output) dictionary.

Every video name is appended to a special key in the result dictionary called "  ALL  ". This is done to save the current progress and to skip videos if this program is ran again.

Another frame is taken from the queue and the cycle repeats.

When both threads conclude, the results and stats are displayed.





















