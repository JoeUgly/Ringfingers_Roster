


import numpy, cv2, PIL, pytesseract, os, sys, time

print(777777777777)


tessexe = os.path.join(sys._MEIPASS, 'tesseract.exe')

pytesseract.pytesseract.tesseract_cmd = tessexe





# Path to image dir
pics_l = os.listdir(r"C:\Users\jschiffler\Pictures\Screenshots")

# Most recent image
pic = r"C:\Users\jschiffler\Pictures\Screenshots\\" + str(pics_l[-1])


# Get text
text = pytesseract.image_to_string(pic)


print(text)






input('ffffffffff')




'''
output .json
recognize by custom file ext

calc rms before threshold
checksums

expand sampling window because transparency will get corrected by threshold
work pc perf



'''



















