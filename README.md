# Dark_Souls_3_Roll_Call

# ___ UNDER CONSTRUCTION ___

## Extract other players' names from your Dark Souls 3 gameplay videos

fps check
lenient and very lenient both invoked
use quotes in examples
ask about video organization
strip text first
tess path
exclude all .exe files? only rr file? sys.argv[0]
remind to mark run as executable

checksums
Get-FileHash input
certutil -hashfile input sha256
SHA256sum -c myfiles.md5
generate:
SHA256sum groups_list.txt  groups.csv > myfiles.SHA256sum


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
* [How can I help?](#How-can-I-help)
* [Advanced Usage](/Advanced_Usage.md)


<br/><br/>
## Summary
Scans through your DS3 gameplay videos and records the name of each player who enters or leaves the world.\
The program outputs a list of player names, along with the name of each video which they were found in.

Use case:\
You know you fought this person before, but you don't want to manually look through hours of gameplay footage to find the right video(s).



<br/><br/>
## Getting Started
### Recommended method
The easiest way to run this program is to use one of the "frozen" executables.\
Windows 10: \
Windows 11: \
Linux Ubuntu: 

These executables will contain the Python interpreter, the Python script, and all the dependencies.

Simply place the executable file in the same folder as your videos and double click to run it.


<br/><br/>
Alternatively, you can run the executable file from a CLI.\
Example:\
`C:\Users\jugly\Desktop\Downloads\rr.exe C:\Users\jugly\Desktop\DS3Videos\`

If no video folder is given, then it defaults to the folder containing the executable file.

Running from a CLI may be mandatory on some systems (Linux).

<br/><br/>
#### Manual method
If you are not using one of the platforms listed above, then you'll need to fullfill the prerequisites manually.\
See the [Manual installation method](https://github.com/JoeUgly/Dark_Souls_3_Roll_Call/edit/main/Advanced_Usage.md#Manual-installation-method) section of the Advanced Usage document.

<br/><br/>
## Limitations and Known Bugs

#### Nameplate not caught
This program detects player names **ONLY** when the nameplate appears.

![](https://github.com/JoeUgly/Dark_Souls_3_Roll_Call/blob/main/assets/nameplate.png)

This program assumes the entire nameplate animation (the nameplate message fading in and out multiple times) is present in the video.\
If any part of the nameplate animation is missing from the video, then this program might not capture that player's name.

**Does not work on arena fights.**


<br/><br/>
#### Message too long 
Some messages can be so long that they extend past the edge of the nameplate and therefore not detected.\
Some messages consist of two lines and therefore the useful text is not in the excpected location and also not detected.


<br/><br/>
#### Misinterpreted characters in player name
Having a computer read text from an image is inherently error prone.\
It's common for a player name to appear in the output multiple times with slight errors.\
Example:
```
{
"Player_1": ["/path/to/video1.mkv"],
"PIayer_!": ["/path/to/video1.mkv"],
...
}
```

A video resolution of 720p is the minimum needed for acceptable quality of results. 1080p is much better.


<br/><br/>
#### Misinterpreted characters in prefix or suffix
The name extraction consists of three steps. Recognize the prefix phrase, recognize the suffix phrase, extract the leftover name.\
Using the example message "Phantom XXsoandsoXX has been summoned":\
Prefix: Phantom\
Suffix: has been summoned\
Player name: XXsoandsoXX

An exact match for both the prefix and the suffix is required. \
A single misinterpreted character in the prefix / suffix will cause the frame (and name) to be discarded.

This behavior can be changed to be more forgiving by invoking the `--lenient` or `--verylenient` options.\
Using `--lenient` will extract a player name, even if a prefix or suffix is not detected. \
Using `--verylenient` will extract a player name, even if both the prefix and suffix are not detected.\
These options will cause increasingly more entries into the output file, many of which will be false positives.\
If you want to maximise the chances of detecting a player's name and you are not concerned about a somewhat bloated output file, then use these options.


<br/><br/>
## FAQ

#### What video formats are allowed?
Anything that OpenCV can read.

Any file which does not begin with `ds3_rr_results` will be assumed to be a video. This program should identify errors related to trying to read a non-video file and skip to the next file.

	
<br/><br/>
#### How can I skip some files in a folder?
Use your CLI's glob / wildcard capabilities.\
Example using Windows PowerShell to select only MP4 files:\
`python C:\Users\jhalb\Downloads\ds3_rc.py $(dir C:\Users\jhalb\Videos\*.mp4)`

Example using Bash to select only MP4 files:\
`python3 /home/jhalb/code/ds3_rc.py /home/jhalb/videos/*.mp4`


<br/><br/>
#### Why is it so slow?
See the [Performance section](https://github.com/JoeUgly/Dark_Souls_3_Roll_Call/blob/main/Advanced_Usage.md#Performance) in the Advanced Usage document.


<br/><br/>
#### Other questions
Check out the [Advanced Usage document](https://github.com/JoeUgly/Dark_Souls_3_Roll_Call/blob/main/Advanced_Usage.md)\
or [open an issue](https://github.com/JoeUgly/Dark_Souls_3_Roll_Call/issues)

<br/><br/>
## How can I help?
Please report the following:\
Bugs, errors, problems\
Your PC specs and performance (the last few lines of the program's CLI output)\
Any other questions, requests, suggestions, comments,  etc


<br/><br/>










add tesseract to Win path?
https://towardsdatascience.com/simple-ocr-with-tesseract-a4341e4564b6












