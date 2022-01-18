# Advanced Usage

### Table of Contents
* [Options](#Options)
* [Input](#Input)
* [Output](#Output)
* [Features](#Features)
* [Performance](#Performance)
* [Detailed Description](#Detailed-Description)



<br/><br/>
## Options
--nonrecursive&emsp;&emsp; Do not search directories recursively.\
--noskip&emsp;&emsp;&emsp;&emsp;&emsp;Do not skip files if they have the same filename.\
--lenient&emsp;&emsp;&emsp;&emsp;&emsp;Attempt name extraction if a prefix or suffix is missing.\
--verylenient&emsp;&emsp;&emsp;Attempt name extraction if both the prefix and suffix are missing.\
--output=&emsp;&emsp;&emsp;&emsp; Specify the location of the output (result) file.



<br/><br/>
## Input

This program will accept any combination of these four types of arguments:
1. Options
2. A Result file used for the [Resumption feature](#Resumption)
3. A video file
4. A directory containing videos (and result files)

All options must begin with "--".\
All result files must begin with "ds3_rc_results".

If no files or directories are given, the program will use the current working directory.

Directory searches are recursive by default. Disable this with the `--nonrecursive` option.\
Only directories given AFTER the --nonrecursive option will be nonrecursive.

Example:
`python C:\Users\jhalb\Downloads\ds3_rc.py C:\Users\jhalb\folder_1\ --nonrecursive C:\Users\jhalb\folder_2\`\
Only folder_1 will be searched recursively.


<br/><br/>
## Output
This program outputs the results in JSON / Python dictionary format. The key is the player name and the value is a list of file paths (the videos in which the player's name was found).\
Example output file:
```
{
"Motion_1": ["/path/to/video1.mkv"],

"Noob_Slayer_2": ["/path/to/video3.mp4", "/path/to/video1.mkv", "/path/to/video4.mkv"]
}
```

To specify the output file location use the `--output` option.\
Example:
`python ds3_rc.py /path/to/videos/ '--output=/path/to/documents/'`

If no location is specified, then the video directory will be used.\
If no video directory is specified (excplicitly or implicitly), then the directory containing the Python script will be used.

**This program will overwrite the output file without warning.**

<br/><br/>
## Features

#### Resumption
This program saves its progress to a file after each video is processed. This allows for a Resumption feature which serves three purposes:
1. If an error occurs, you don't need to start over from the beginning.
2. When you add new videos and run this program again, it will skip videos which have already been processed.
3. Merge the previous result file to create a single combined result file with the new additions.

To use this Resumption feature:\
Place the result file in the same directory as the videos you are processing.\

Alternatively, you can explicitly give the absolute path of the result file as an argument.\
Example:\
`python ds3_rc.py /path/to/videos/ /path/to/ds3_rc_results.txt`

The results filename must begin with "ds3_rc_results".
You can merge multiple result files.


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

**Frame extraction thread**\
This thread iterates over every video in the list. Videos are read using CV2 (OpenCV) and frames are stored as Numpy arrays.\
Every 67th frame (assuming a 60 fps video) is extracted because that is the minimum sampling rate required to guarantee nameplate recognition. The nameplate appears three times, fading to transparent in between. This program aims to select a frame containing the nameplate at least one of the three times when it is completely opaque. Choosing a less frequent sampling rate would increase performance, but decrease the quality of the results.

**Frame processing thread**\
After a frame is taken from the queue, it is cropped to a small area near the top of the nameplate. The average brightness of this small area is determined. If the brightness is too high, then it is assumed that a nameplate message is not present and the frame is discarded.

If a nameplate is determined to likely be present, then the nameplate is cropped where the text is located.

At this time the frame is converted to an image using PIL. Optical character recognition using PyTesseract (Tesseract) is performed.

If an appropriate phrase is detected (such as "Invaded the World of...", "Phantom ... has died", etc), then the player name is appended to the result (output) dictionary.

Every video name is appended to a special key in the result dictionary called "  ALL  ". This is done to save the current progress and to skip videos if this program is ran again.

Another frame is taken from the queue and the cycle repeats.

When both threads conclude, the results and stats are displayed.


<br/><br/>



















