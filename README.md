# Dark_Souls_3_Roll_Call

# ___ UNDER CONSTRUCTION ___

## Extract other player's names from your gameplay videos


todo

email
discord
example of nameplate image
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -
use python to glob? -
config file?
optional fuzzy matching for phrases
move .py into dir then just click (make executable?)
output default to dir of code?


Phase 1:
Basic features

Beta Release

Compatibility / Bug fixes

Stable Release

Phase 2:
Quality of results

Phase 3:
Performance

args
	--nonrecursive
	--strict or --loose phrase/name detection
	--output for results file
	--noskip same filenames in diff locations?
	--multi thread count?


### Table of Contents
* [Summary](#Summary)
* [Getting Started](#Getting-Started)
* [Limitations](#Limitations)
* [FAQ](#FAQ)
* [Support](#Support)
* [Advanced Usage](/Advanced_Usage.md)





## Summary
Scans through all your gameplay videos and extracts the name of each player you encounter.\
The program outputs a list of player names, along with the name of each video which they were found in.


Use case:\
You know you fought this person before, but you don't want to manually look through hours of gameplay footage to find the right video(s).




## Getting Started
The following Python packages are required:
pytesseract

Example installation:\
pip install pytesseract


To run the program, invoke the Python script along with the folder(s) containing your videos.
Example:\
python /path/to/code/ds3_rc.py /path/to/videos/



Alternatively, if you really don't want to mess with a CLI, place the ds3_rc.py file in the same folder as your videos and double click to run.

See the "Input" section for more detail.



## Limitations and Known Bugs

#### Nameplate not caught
This program detects player names **ONLY** when the nameplate appears.
Doesn't work on arena fights.
This program assumes the entire nameplate animation (the nameplate message fading in and out multiple times) is present in the video.

For performance reasons this program does not check every frame. In fact, it checks only one frame per ~1.1 seconds of video. If any part of the nameplate animation is missing from the video, then this program might not capture that player's name.

#### Long message
Some messages can be so long that they extend past the edge of the nameplate and therefore not detected.
Some messages consist of two lines and therefore the useful text is not in the excpected location and also not detected.

#### Misinterpreted characters in player name
Computers are bad at reading text from an image. Therefore, this program will not be 100% accurate.
It's common for a player name to appear in the output multiple times with slight errors.
Example:
{
"Player_1": ["/path/to/video1.mkv"],
"PIayer__!": ["/path/to/video1.mkv"],
...
}

For this reason, video resolution of at least 720p is strongly recommended. Also, Tesseract version 5.0+.


#### Misinterpreted characters in prefix or suffix
The name extraction consists of three steps. Recognize the prefix phrase, recognize the suffix phrase, extract the leftover name.
Using the example message "Phantom XXsoandsoXX has been summoned":
Prefix: Phantom
Suffix: has been summoned
Player name: XXsoandsoXX


An exact match for both the preffix and the suffix is required. 
A single misinterpreted character in the prefix / suffix will cause the frame to be discarded.

This behavior can be changed to be more lenient by invoking the --loose?? option.
Using --loose?? will accept all nameplate text, even without a prefix or suffix match. This will cause many more entries into the output file, many of which will be false positives.
If you want to maximise the chances of detecting a player's name and you are not concerned about a somewhat bloated output file, then use this option.









## Support
Please report the following:
Bugs, errors, problems
Your PC specs and performance (the last few lines of the program's CLI output)
Any other questions, requests, suggestions, comments,  etc



























