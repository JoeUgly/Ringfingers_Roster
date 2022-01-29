
# Desc: Extract players' names from Dark Souls 3 videos




import time
import sys
import os
import ntpath
import cv2
from PIL import Image, ImageStat, ImageOps
from pytesseract import pytesseract
import json
import threading as mt
import queue






# Benchmarking
startTime = time.time()
time_tess_l = []
time_fr_l = []
time_vcap_l = []
time_crop2_l = []
time_crop1_l = []


# Phrases to remove from player names
prefix_l = ['Phantom', 'Blue spirit', 'Blade of the Darkmoon', 'Dark spirit', 'Mad dark spirit', 'Aldrich Faithful', 'Loyal spirit, Aldrich Faithful', 'Watchdog of Farron', 'Loyal spirit, Watchdog of Farron', 'Invaded the world of', 'Invaded by dark spirit', 'Task completed.']
suffix_l = ['summoned', 'has died', 'has returned home', 'summoned through concord!', 'invaded', ', disturber of sleep', 'has returned to their world']




# Gather all files and options from args
def get_files_f(arg_l, arg_d):

    for item in arg_l:

        # Options
        if item.startswith('--'):
            if item == '--nonrecursive':
                arg_d['recursive'] = False
                print('Option set: nonrecursive')
            elif item == '--noskip':
                arg_d['noskip'] = True
                print('Option set: noskip')
            elif item.startswith('--output='):
                arg_d['output_loc'] = ''.join(item.split('--output=')[1:])
                print('Option set: output location:', arg_d['output_loc'])
            elif item == '--strict':
                arg_d['leniency'] = 0
                print('Option set: strict phrase matching')
            elif item == '--lenient':
                arg_d['leniency'] = 2
                print('Option set: lenient phrase matching')
            else:
                print('\nOption not recognized:', item)

        # Directory
        elif os.path.isdir(item):
            if arg_d['recursive'] or arg_d['first_dir'] == 'first':
                if arg_d['first_dir'] == 'first':
                    arg_d['first_dir'] = item
                child_l = [os.path.join(item, child) for child in os.listdir(item)]  # List of items in dir
                get_files_f(child_l, arg_d)  ## does this need to return a new arg_d? arg_d = get_files_f(child_l, arg_d)

        # File
        elif os.path.isfile(item):
            if os.access(item, os.R_OK):
                if ntpath.basename(item).startswith(result_filename.rsplit('.')[0]):  # Result file
                    arg_d['result_file_l'].append(item)
                    print('Result file detected:', item)
                else:
                    all_files_l.append(item)  # Video file
            else:
                print('Error: File is not readable:', item)

        else:
            print('Error: Not a file, directory, or option:', item, type(item))


    return arg_d



# Make sure Tesseract is working
def check_tess_f():

    # Running as frozen executable
    if hasattr(sys, '_MEIPASS'):
        print('Running as frozen executable')
        tess_dir = os.path.join(sys._MEIPASS, 'tess')  # Custom dir created when freezing executables

        # Path to Tesseract executable
        if 'tesseract.exe' in os.listdir(tess_dir):
            print('Trying Windows Tesseract ...')
            pytesseract.tesseract_cmd = os.path.join(tess_dir, 'tesseract.exe')
        elif 'tesseract' in os.listdir(tess_dir):
            print('Trying Linux Tesseract ...')
            os.environ['TESSDATA_PREFIX'] = tess_dir  # Needed to detect shared objects
            pytesseract.tesseract_cmd = os.path.join(tess_dir, 'tesseract')
        else:
            print('Tesseract executable cannot be found. Exiting ...')
            return False

    # Tesseract executable must be on PATH or stated explicitly
    else:
        print('Running as a script')
        # Uncomment next line and replace with your location of the Tesseract executable
        pytesseract.tesseract_cmd = r"C:\Users\jschiffler\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

    # Check if Tesseract is working
    try:
        pytesseract.get_tesseract_version()
        print('Tesseract is working')
        os.environ['OMP_THREAD_LIMIT'] = '1'  # Use only one cpu core for Tesseract
        return True
    except Exception as errex:
        print('pytesseract:', errex)
        print('\n Tesseract is not working. If you are running as a script make sure the Tesseract executable is on the PATH or explicitly stated in the RR python script.')
        print('Check the Advanced Usage document on Github for more info.')
        return False


# Make sure write to file is working
def check_write_f():
    test_loc = os.path.join(arg_d['output_loc'], 'rr_test_filename')
    with open(test_loc, 'w', errors='replace') as output_file:
        output_file.write('TEST_TEXT')

    with open(test_loc, 'r') as output_file:
        content = output_file.read()
    
    if content == 'TEST_TEXT':
        os.remove(test_loc) 
        return True
    else:
        print('Can not read/write at output file location. Check the path and permissions.')
        print('Output file location:', arg_d['output_loc'])
        return False



# Extract player names from text
def clean_names_f(text):
    name = text  # This is needed for lenient matching
    lenient_val = arg_d['leniency']  # Decrement this value to allow for 1 or 2 missing phrases
    try: 

        # Host detection
        if text.startswith('Invaded the world of Host of Embers'):
            name = text.split('Invaded the world of Host of Embers', maxsplit=1)[1].strip()
            return name

        # Phantom prefix detection
        for prefix in prefix_l:
            if text.startswith(prefix):
                name = text.split(prefix, maxsplit=1)[1].strip()
                break

        # No prefix detected
        else:
            print('No prefix detected:', text)
            if not lenient_val:
                return None
            lenient_val -= 1

        # Phantom suffix detection
        for suffix in suffix_l:
            if text.endswith(suffix):
                name = name.rsplit(suffix, maxsplit=1)[0].strip()
                print('Phrase match:', text)
                return name

        # No suffix detected
        else:
            print('No suffix detected:', text)
            if lenient_val:
                return name  # Return name if lenient val > 0
            else:
                return None

    except Exception as errex:
        print('__Error on name cleanup:', errex)
        text += '__Error'
        return text



# Add names to dict
def add_names_f(name, video_path, name_d):
    if name in name_d:  # Name already in dict
        if not video_path in name_d[name]:  # Prevent dups
            print('Adding video to name:', video_path, name)
            name_d[name].append(video_path)
    else:  # New entry as list
        print('Adding video to name:', video_path, name)
        name_d[name] = [video_path]


# Save results to file
def write_res_f(name_d):
    json_results = json.dumps(name_d, indent=4)
    with open(output_loc, 'w', errors='replace') as output_file:
        output_file.write(json_results)
    return json_results


# Put frames in queue
def get_frames_f(frame_queue, all_files_l):
    current_file_i = -1
    skip_tally = 0
    frame_grand_total = 0
    duration_grand_total = 0

    # Iterate all videos
    for video_path in all_files_l:
        current_file_i += 1
        consec_err = 0
        try:

            # Prevent duplicate files
            if arg_d['noskip']:
                video_name = video_path
            else:
                video_name = ntpath.basename(video_path)

            if video_name in checked_files_l:
                print('\n Skipping video:', video_path)
                continue
            else:
                checked_files_l.append(video_name)


            # Read video
            print('\n Starting video:', video_path)
            vid_frame_count = 0
            try:
                time_vcap = time.time()
                vcap = cv2.VideoCapture(video_path)
                time_vcap_l.append((time.time() - time_vcap))
                if not vcap.isOpened(): raise

            except:
                print('__Error: Unable to read file as video. Skipping:', video_path)
                continue

            # Get frame data
            try:
                vid_frame_total = vcap.get(7)  # Num of frames in video
                if vid_frame_total < 0: raise
                frame_rate = round(vcap.get(5))  # FPS
                frame_count_interval = round(frame_rate * 1.116666667)  # Select every 67th frame (on 60fps)

            except:
                print('__Error: Unable to get frame data. Skipping:', video_path)
                continue


            
            breakpoint = 3000
            if vid_frame_total > breakpoint:
                vid_frame_total = breakpoint
            

            print('fps:', frame_rate)
            video_duration = vid_frame_total / frame_rate
            print('video_duration:', video_duration)




            # Loop video until end
            while vid_frame_count + frame_count_interval <= vid_frame_total:

                # Display progress occasionally
                if skip_tally >= 50:
                    skip_tally = 0
                    progress_f(vid_frame_count, vid_frame_total, current_file_i, all_files_l)
                else:
                    skip_tally += 1

                # Check if queue is full
                while frame_queue.full():
                    print('queue full:', frame_queue.qsize())
                    time.sleep(1)



                # Read frame
                try:
                    time_frame_read = time.time()
                    vid_frame_count += frame_count_interval  # Increment to next working frame
                    vcap.set(1, vid_frame_count)  # 1 designates CAP_PROP_POS_FRAMES (which frame to read)
                    frame_na = vcap.read()[1][:, :, 0]  # Read nth frame # Remove color data
                    time_fr_l.append((time.time() - time_frame_read))
                    consec_err = 0
                except Exception as errex:
                    print('__Error trying to read frame:', errex)
                    if consec_err > 5:  # Skip to next video after too many errors
                        consec_err = 0
                        print('Skipping to next video')
                        break
                    else:
                        consec_err += 1
                        continue


                # Put frame in queue
                with q_lock:
                    frame_queue.put((video_path, frame_na), block=True)



            # End of video
            frame_grand_total += vid_frame_total
            duration_grand_total += video_duration


        except Exception as errex:
            print(errex, sys.exc_info()[2].tb_lineno)


    # End of all videos
    with q_lock:
        frame_queue.put((False, frame_grand_total, duration_grand_total), block=True)

    print('\nEnd of get_frames_f')




# Get frames from queue and process
def process_frames_f(frame_queue, name_d):
    prev_video_path = None
    

    # Threshold for converting pixel to black or white
    thresh = 60  # Higher values will give "thinner" text
    temp_fn = lambda x : 255 if x > thresh else 0


    while True:

        # Wait for a frame to be available
        while True:
            try:
                with q_lock:
                    q_ret_t = frame_queue.get_nowait()
                    break
            except queue.Empty:
                time.sleep(.01)
            except Exception as errex:
                print('__Error: queue:', errex)



        video_path = q_ret_t[0]
        frame_na = q_ret_t[1]


        # Detect start of new video
        if video_path != prev_video_path:

            # Append completed video name to name_d
            if prev_video_path:  # Skip first video
                name_d["  ALL  "].append(prev_video_path)  # Add video to ALL key
                json_results = write_res_f(name_d)  # Save new results file

            prev_video_path = video_path

            # No more videos
            if video_path == False:
                frame_queue.put((q_ret_t[1], q_ret_t[2]))
                break



        try:

            # Select area above nameplate text
            # Crop as percent so unaffected by resolution
            height, width = frame_na.shape[:2]
            x1_coord = int(width * .29)
            x2_coord = int(width * .71)
            y1_coord = int(height * .681)
            y2_coord = int(height * .695)

            crop_arr = frame_na[y1_coord:y2_coord, x1_coord:x2_coord]  # Crop Numpy array with index operator because it's faster

            crop_img = Image.fromarray(crop_arr)  # Convert to PIL image


            # Calculate root mean square of brightness
            stat = ImageStat.Stat(crop_img)
            rms = stat.mean[0]
            #print('rms:', rms)

            # Skip if too dark or too bright, ie: nameplate not detected
            if rms < 11 or rms > 14:
                continue


            # Reuse x coords for text crop
            time_crop2 = time.time()
            y1_coord = int(height * .69)
            y2_coord = int(height * .73)
            crop_arr = frame_na[y1_coord:y2_coord, x1_coord:x2_coord]

            #crop_img = Image.fromarray(crop_arr)

            # Reduce noise by converting to only black or white
            time_crop1 = time.time()
            #crop_img = crop_img.convert('L').point(temp_fn, mode='1')
            #crop_img = crop_img.convert('L').point(temp_fn, mode='L')
            time_crop1_l.append(time.time() - time_crop1)
            
            #crop_img = ImageOps.invert(crop_img)  # Tesseract expects dark text on light background. Slightly faster than tesseract inverting

            time_crop2_l.append((time.time() - time_crop2))

            #crop_img.show()  # will need? pip install opencv-python


            # Get text from image, don't invert, whitelist ASCII chars, expect one line of text
            t4 = time.time()
            text = pytesseract.image_to_string(crop_arr, timeout=5, config='''-c tessedit_do_invert=1 -c tessedit_char_whitelist="!\\"#$%&\\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ " --psm 7 --oem 1''').strip()

            time_tess_l.append((time.time() - t4))


            # Check for phrases and extract player names
            if text:
                print(text)  ##
                name = clean_names_f(text)

                # Add names to dict
                if name:
                    add_names_f(name, video_path, name_d)



        except Exception as errex:
            print(errex, sys.exc_info()[2].tb_lineno)


    print('\nEnd of process_frames_f')


# Display progress
def progress_f(vid_frame_count, vid_frame_total, current_file_i, all_files_l):

    file_prog = vid_frame_count / vid_frame_total

    tot_prog_inc = 1 / len(all_files_l) * 100
    additional_inc = round(tot_prog_inc * file_prog)

    total_prog_simple = round(current_file_i / len(all_files_l) * 100)
    total_prog_adv = additional_inc + total_prog_simple

    print('\nFile progress:', str(round(file_prog * 100)) + '%')
    print('Total progress:', str(total_prog_adv) + '%')
    print('Frames in queue:', frame_queue.qsize(), '\n')









if __name__ == '__main__':

    print('Arguments:', sys.argv[1:])

    # Set default input and output directory
    default_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    print(os.path.abspath(sys.argv[0]))
    print(os.path.abspath(__file__))

    # Default options
    arg_d = {
    'recursive': True,
    'first_dir': 'first',
    'noskip': False,
    'output_loc': False,
    'result_file_l': [],
    'leniency': 1
    }

    result_filename = 'ds3_rr_results.txt'
    all_files_l = []  # All the videos to work on


    # Get user-supplied option values
    arg_d = get_files_f(sys.argv[1:], arg_d)

    # If no files as input, default to all files in script/exe dir
    if not all_files_l:
        arg_d = get_files_f([default_path], arg_d)


    checked_files_l = []  # Used only by get_frames_f to not start working on same video
    name_d = {"  ALL  ": []}  # Used by process_frames_f to mark a video as complete

    # Merge all input files
    if arg_d['result_file_l']:
        for input_file in arg_d['result_file_l']:
            with open(input_file, 'r') as res_file:
                new_d = json.loads(res_file.read())

            for key, value in new_d.items(): 
                if key in name_d:  # Player name already exists
                    for each_vid in value:  # Append all videos to the key
                        if not each_vid in name_d[key]:  # Prevent dups
                            name_d[key].append(each_vid)
                else:
                    name_d[key] = value

        # Append every video from ALL key to checked_files_l
        for value in name_d["  ALL  "]:
            if not arg_d['noskip']:  # Use only filename if noskip is invoked
                value = ntpath.basename(value)
            if not value in checked_files_l:
                checked_files_l.append(value)


    # Set output location if not specified
    if not arg_d['output_loc']:
        if arg_d['first_dir'] != 'first':  # Use first specified dir
            arg_d['output_loc'] = arg_d['first_dir']
        else:
            arg_d['output_loc'] = default_path  # Use script or exe dir

    output_loc = os.path.join(arg_d['output_loc'], result_filename)


    print(json.dumps(arg_d, indent=4))


    # Make sure Tesseract is working
    tess_working = check_tess_f()
    if not tess_working: sys.exit()

    # Make sure you can write to output file
    write_working = check_write_f()
    if not write_working: sys.exit()


    q_lock = mt.Lock()
    frame_queue = queue.Queue(200)  # Queue max size

    p1 = mt.Thread(target=get_frames_f, args=(frame_queue, all_files_l))
    p1.start()
    p2 = mt.Thread(target=process_frames_f, args=(frame_queue, name_d))
    p2.start()

    p1.join()
    p2.join()





    # Write and display results
    print(json.dumps(name_d, indent=4))
    print('\n\n\n\t-------- Complete. --------\n\nOutput file saved at:', output_loc, '\n\n')


    # Prevent divide by zero error
    for each_l in [time_crop1_l, time_vcap_l, time_fr_l, time_tess_l]:
        if not each_l:
            each_l.append(0)

    # Display stats
    frame_grand_total, duration_grand_total = frame_queue.get()
    duration = time.time() - startTime

    print(duration)  ##
    print('\n\nRun time duration:', round(duration / 60), 'minutes')
    print('Footage processed:', round(duration_grand_total / 60), 'minutes')
    print('\nAve processing speed:', str(round(duration_grand_total / duration, 1)) + 'x')
    print('Ave frames / sec:', round(frame_grand_total / duration))
    print('video capture ave:', sum(time_vcap_l) / len(time_vcap_l))
    print('frame read ave:', sum(time_fr_l) / len(time_fr_l))
    print('img convert ave:', sum(time_crop1_l) / len(time_crop1_l))
    print('OCR read ave:', sum(time_tess_l) / len(time_tess_l))
    print('\nVersion: 0.1.0-beta')

    input('END')










