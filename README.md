# Dark_Souls_3_Roll_Call

# ___ UNDER CONSTRUCTION ___

## Extract other player's names from your gameplay videos

fps check
lenient and very lenient both invoked


Phase 1:
Basic features

Beta Release

Compatibility / Bug fixes

Stable Release

Phase 2:
Quality of results

Phase 3:
Performance

Phase 4:
Advanced features



<br/><br/>
### Table of Contents
* [Summary](#Summary)
* [Getting Started](#Getting-Started)
* [Limitations](#Limitations)
* [FAQ](#FAQ)
* [Support](#Support)
* [Advanced Usage](/Advanced_Usage.md)


<br/><br/>
## Summary
Scans through your gameplay videos and records the name of each player who enters or leaves the world.\
The program outputs a list of player names, along with the name of each video which they were found in.

Use case:\
You know you fought this person before, but you don't want to manually look through hours of gameplay footage to find the right video(s).



<br/><br/>
## Getting Started
#### Recommended method
The easiest way to run this program is to use one of the "frozen" executables.\
Windows 10: \
Windows 11: \
Linux Ubuntu 19.04: 

These executables will contain the Python interpreter, the Python script, and all the dependencies.\
Simply place the executable file in the same folder as your videos and double click to run it.


<br/><br/>
#### Manual method
If you are not using one the platforms listed above, then you'll have to do it manually. Follow these steps:

Prerequisites:\
Install Python version 3.6+. [Available here](https://www.python.org/downloads/)

Install the following Python packages: pytesseract, opencv-python, Pillow\
Example installation:\
`pip install pytesseract, opencv-python, Pillow`

Download my Python script located at: /releases/ds3_rc.py??

Install Tesseract-OCR (version 5.0+ is strongly reccomemended)
Windows: [Available here](https://github.com/UB-Mannheim/tesseract/wiki)
Linux: [Available here](https://tesseract-ocr.github.io/tessdoc/Home.html#binaries)

I used the following to easily install Tesseract 5.0 on Ubuntu:
` `

To run the program, invoke the Python script from a CLI along with the folder(s) containing your videos.\
Example:\
`python C:\Users\Jugly\Downloads\ds3_rc.py C:\Users\Jugly\Videos\`


<br/><br/>
Alternatively, if you really don't want to mess with a CLI, place the ds3_rc.py file in the same folder as your videos and double click to run.


<br/><br/>
## Limitations and Known Bugs

#### Nameplate not caught
This program detects player names **ONLY** when the nameplate appears.

![](https://github.com/JoeUgly/Dark_Souls_3_Roll_Call/blob/main/assets/nameplate.png)

Doesn't work on arena fights.

This program assumes the entire nameplate animation (the nameplate message fading in and out multiple times) is present in the video.

For performance reasons this program does not check every frame. In fact, it checks only one frame per ~1.1 seconds of video. If any part of the nameplate animation is missing from the video, then this program might not capture that player's name.


<br/><br/>
#### Message too long 
Some messages can be so long that they extend past the edge of the nameplate and therefore are not detected.\
Some messages consist of two lines and therefore the useful text is not in the excpected location and are also not detected.


<br/><br/>
#### Misinterpreted characters in player name
Computers are bad at reading text from an image. Therefore, this program will not be 100% accurate.\
It's common for a player name to appear in the output multiple times with slight errors.\
Example:
```
{
"Player_1": ["/path/to/video1.mkv"],
"PIayer__!": ["/path/to/video1.mkv"],
...
}
```

For this reason, video resolution of at least 720p is strongly recommended. Also, Tesseract version 5.0+.


<br/><br/>
#### Misinterpreted characters in prefix or suffix
The name extraction consists of three steps. Recognize the prefix phrase, recognize the suffix phrase, extract the leftover name.\
Using the example message "Phantom XXsoandsoXX has been summoned":\
Prefix: Phantom\
Suffix: has been summoned\
Player name: XXsoandsoXX

An exact match for both the prefix and the suffix is required. \
A single misinterpreted character in the prefix / suffix will cause the frame (and name) to be discarded.

This behavior can be changed to be more lenient by invoking the `--lenient` or `--verylenient` options.\
Using `--lenient` will extract a player name, even if a prefix or suffix is not detected. \
Using `--verylenient` will extract a player name, even if both the prefix and suffix are not detected.\
These options will cause increasingly more entries into the output file, many of which will be false positives.\
If you want to maximise the chances of detecting a player's name and you are not concerned about a somewhat bloated output file, then use these options.


<br/><br/>
## FAQ

#### What video formats are allowed?
Anything that OpenCV can read. This program uses only very basic error checking in regards to reading a file as a video.\
Unpredictable behavior will occur if you attempt to run this program on non-videos.

	
<br/><br/>
#### How can I skip some files in a folder?
Use your CLI's glob / wildcard capabilities.\
Example using Windows PowerShell to select only MP4 files:\
`python C:\Users\jhalb\Downloads\ds3_rc.py $(dir C:\Users\jhalb\Videos\*.mp4)`

Example using Bash to select only MP4 files:\
`python3 /home/jhalb/code/ds3_rc.py /home/jhalb/videos/*.mp4`



<br/><br/>
## Support
Please report the following:\
Bugs, errors, problems\
Your PC specs and performance (the last few lines of the program's CLI output)\
Any other questions, requests, suggestions, comments,  etc


<br/><br/>











import ntpath

use
pip install opencv-python-headless
if not using
cv2.imshow













