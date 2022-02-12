
'''

open vid
grab frame
grab player 1 sb region
test for orange
if true:
    grab and test p2 region? unn?
    if true: grab p3 and p4 regions and test for blue

if false:
test for blue
    repeat

do we need to determine color? only for sb determination

grab and test party symbol x4 +
    party sym pos depends on title. move target pos or not? should land in symbol either way
grab and test title. x4 +

grab sb color regions x4? x2?


Default coords must be percent
'''










from PIL import Image
import numpy as np




im = Image.open(r"C:\Users\jschiffler\Downloads\rl.bmp")

frame_na = np.array(im)

height, width = frame_na.shape[:2]



# Default name coords
x1 = int(width * 0.256)
x2 = int(width * 0.43)
y1 = int(height * 0.325)
y2 = int(height * 0.367)

name_pos_d = {
    1: [x1, x2, y1, y2],
    2: [x1, x2, y1, y2],
    3: [x1, x2, y1, y2],
    4: [x1, x2, y1, y2]
}



# SCOREBOARD DETECTION
x1_coord = int(width * 0.43)
x2_coord = int(width * 0.453)


for y1_percent in [0.335, 0.5486]:
    y1_coord = int(height * y1_percent)
    y2_coord = int(y1_coord + 1)
    sb_na = frame_na[y1_coord:y2_coord, x1_coord:x2_coord]
    sb_trans_na = sb_na[0].transpose()
    sb_color_d = {
        'red': False,
        'green': False,
        'blue': False
    }
    # Blue detection on upper scoreboard
    for i, color in enumerate(sb_color_d):
        if all(140 > xxx > 100 for xxx in sb_trans_na[i].tolist()):
            sb_color_d[color] = True
    if sum(sb_color_d.values()) == 1:
        for k, v in sb_color_d.items():
            if v:
                print('color detected:', k)
                break
    else:
        print('not 1 color within range', sb_color_d)



# lower



sb_na = frame_na[low_y1_coord:low_y2_coord, x1_coord:x2_coord]
sb_trans_na = sb_na[0].transpose()


sb_color_d = {
    'red': False,
    'green': False,
    'blue': False
}

# Orange detection on lower scoreboard
for i, color in enumerate(sb_color_d):
    if all(140 > xxx > 100 for xxx in sb_trans_na[i].tolist()):
        other_color1 = (i + 1) % 3
        other_color2 = (i + 2) % 3
        if all(60 > yyy for yyy in sb_trans_na[other_color1].tolist()) and all(60 > yyy for yyy in sb_trans_na[other_color2].tolist()):  # IF both other colors are below thresh
            sb_color_d[color] = True

if sum(sb_color_d.values()) == 1:
    for k, v in sb_color_d.items():
        if v:
            print('Bottom color detected:', k)
            break
else:
    print('not 1 color within range', sb_color_d)






# TITLE DETECTION
title_d = {
    1: False,
    2: False,
    3: False,
    4: False
}

x1_coord = int(width * 0.258)
x2_coord = int(width * 0.281)
tit_y_percents = (0.3666, 0.4194, 0.5819, 0.6347)

# Loop for each player
for player, iiii in enumerate(tit_y_percents, 1):
    y1_coord = int(height * iiii)
    y2_coord = y1_coord + 1
    tit_reg = frame_na[y1_coord:y2_coord, x1_coord:x2_coord]
    rgb_l = tit_reg.transpose()
    # If each color channel has a value over 100 then title detected
    for each_color_l in rgb_l:
        if not any(i > 100 for i in each_color_l):
            break
    else:
        print('Title detected for player:', player)
        title_d[player] = True
        tit_correction = int(0.0083 * height)
        name_pos_d[player][2] -= int(0.0083 * height)
        name_pos_d[player][3] -= int(0.0083 * height)





# PARTY SYMBOL DETECTION
party_d = {
    1: False,
    2: False,
    3: False,
    4: False
}

x_coord = int(width * 0.265)

party_y_percents = (0.347, 0.401, 0.563, 0.616)

# Loop for each player
for player, each_p in enumerate(party_y_percents, 1):
    y_coord = int(height * each_p)
    party_red, party_green, party_blue = im.getpixel((x_coord, y_coord))  # Get RGB values where party symbol might be
    # Target color values for party symbol
    party_rt = 215
    party_gt = 255
    party_bt = 152
    party_l = ((party_red, party_rt), (party_green, party_gt), (party_blue, party_bt))
    # If each color channel has a value within range then symbol detected
    for party_pair in party_l:
        current, target = party_pair
        if not target * .85 < current < target * 1.15:
            break
    else:
        print('Party symbol detected for player:', player)
        party_d[player] = True
        name_pos_d[player][0] += int(0.01875 * width)











for i in name_pos_d.items(): print(i)





















