import cv2
import os
import glob
#from pupildetection import hough_circles


#saving file to certain directory
# Param: path=String, directory=String, edit=String
def save_file(path, directory, edit=None):
    #to saving modification
    img = eye_detection(path)[0]
    
    #file name
    basename = os.path.basename(path)
    print(basename)
    basename_edited = edit + basename
    print(basename_edited)
    fname = os.path.join(directory, basename_edited)
    print(fname)
    cv2.imwrite(fname, img)
    
# returns an array of all images in a directory
# Param: directory=String
def all_files(directory):
    data_path = os.path.join(directory,'*g') # file path
    files = glob.glob(data_path)
    print(files)
    
    return files

# runs python script with String as argument
# Param: files=array, command=String
def run_cmd(files, command):
    for f1 in files:
        print('Run ',command,' with ',f1,' as argument')
        cmd = 'python '+command+' '+f1
        print('Command line: ',cmd)
        os.system(cmd)

# crops pupil area
def roi_PI(image):
    h, w = image.shape
    cx, cy, r = hough_circles(image)
    r = r+5
    x1=cx-r
    x2=cx+r
    y1=cy-r
    y2=cy+r
    if r>cx:
        x1 = 0
    if cx+r>w:
        x2=w
    if r>cy:
        y1=0
    if cy+r>h:
        y2=h

    crop = image[y1:y2, x1:x2]
    return crop
    
        
# resizing method 
def resized_by_scale(img, percent):
    width = int(img.shape[1] * percent / 100)
    height = int(img.shape[0] * percent / 100)
    dim = (width, height)
    print(dim)
    # resize image
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        
# count frames in a video
# Param: video=String -> path of a video file
def count_frames_manual(video):
    cam = cv2.VideoCapture(video) 
    # initialize the total number of frames read
    total = 0
    
    # loop over the frames of the video
    while True:
        # grab the current frame
        (grabbed, frame) = cam.read()
        # check to see if we have reached the end of the video
        if not grabbed:
            break
        # increment the total number of frames read
        total += 1
    # return the total number of frames in the video file
    return total