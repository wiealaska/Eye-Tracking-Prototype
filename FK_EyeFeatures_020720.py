import cv2
import os
import glob
import numpy as np
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from imutils import face_utils
import imutils
import dlib
from FK_PIDetection_070420 import *
import natsort
from helpingMethods import resized_by_scale
from matplotlib import pyplot as plt
#from pupildetection import hough_circles # somehow important for the drawing

# returns an array of all images in a directory
# Param: directory=String, 
def all_files(directory, baseName):
    data_path = os.path.join(directory, baseName) # file path
    files = glob.glob(data_path)
    #print(files)
    
    return files

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('eye_predictor.dat')

def eye_detection(image): # image: file name of an image
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = (6,12)
    (rStart, rEnd) = (0,6)
    
    img = cv2.imread(image)
    # convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # resize the image to make the detector faster
    p=0.40
    img_width = gray.shape[1]
    w = img_width * p
    scaled = imutils.resize(gray, int(w))
    # detect faces in the grayscale frame
    rects = detector(scaled, 1)
    while not rects and p <= 1:
        print('Face detection did not work for this scale')
        p += 0.10
        print('Trying ', p*100, '%')
        w = img_width * p
        print(w)
        scaled = imutils.resize(gray, int(w))
        rects = detector(scaled, 1)
    
    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(scaled, rect)
        shape = face_utils.shape_to_np(shape)
        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        # extract the ROI of the face region as a separate image
        rectLeftEye = cv2.boundingRect(leftEye)
        # rescale to orginal size
        (x, y, w, h) = [int(element / p) for element in rectLeftEye]
        roi = gray[y-15:y + h+15, x-5:x + w+5]
        
        rectRightEye = cv2.boundingRect(np.array(rightEye))
        (x1, y1, w1, h1) = [int(element / p) for element in rectRightEye]
        roi1 = gray[y1-15:y1 + h1+15, x1-5:x1 + w1+5]
        break
    
    return roi, roi1

def hough_circles(image):
    edges = canny(image, sigma=1, low_threshold=10, high_threshold=50)
    # Detect two radii ?
    hough_radii = np.arange(10, 25, 1)
    hough_res = hough_circle(edges, hough_radii)
    # Select the most prominent 1 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=1)

    return cx[0], cy[0], radii[0]

# crops pupil area
def roi_PI(image, cx, cy, r):
    h, w = image.shape
#    cx, cy, r = hough_circles(image) auskommentiert s.o.
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

def draw_features(img, pos_pi, pos_pupil):
    #img =cv2.imread(img_path)    
    img =cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    img =cv2.drawMarker(img, pos_pi, (0, 255, 0), cv2.MARKER_CROSS, 6)
    img =cv2.drawMarker(img, pos_pupil, (255, 0, 0), cv2.MARKER_CROSS, 40)    
    return img

def store_pos(posPath, searchDirectory, baseName, eye):
    header = "Pup-pos, PI-pos\n"
    header += "Data for the left eye"
    f = open(posPath, 'wb')
    np.savetxt(f, [], header=header)
    frames = glob.glob(os.path.join(searchDirectory, baseName) + '*') #Verbesserung bei all_files maybe
    frames = natsort.natsorted(frames) # frame sortieren
    print('Frames found: ', frames)
    for i in frames:
        print(i)
        roiL, roiR = eye_detection(i)
        if eye == 'left': 
            cx, cy, r = hough_circles(roiL)
            crop = roi_PI(roiL, cx, cy, r)
        else:
            cx, cy, r = hough_circles(roiR)
            crop = roi_PI(roiR, cx, cy, r)
        cx, cy, r = hough_circles(crop)
        posPupil = (cx, cy)
        posPI = purkinje_image(crop, 80, 95)
        data = np.concatenate((posPupil, posPI), axis=None).reshape(1,4)
        print('Positions: ', data)
        np.savetxt(f, data, fmt='%.18g', delimiter=' ')
        
    f.close()
       
       
if __name__ == "__main__":
    #Beispielhaft für das linke Auge
    path = 'C:/Users/ZVSL/Desktop/Franziska/Study2/Frames/FK_cal7x5_rep3/FK_cal7x5_rep3_frame_pos23.jpg'
    roiL, roiR = eye_detection(path)
    leftEye = resized_by_scale(roiR, 500)
    cv2.imshow('left eye', leftEye)
    #cv2.imwrite('C:\\Users\\ZVSL\\Desktop\\Franziska\\BA\\rightEye_FK.jpg', leftEye)
    
#     edges = canny(roiR, sigma=1, low_threshold=10, high_threshold=50)
#     edges = edges.astype(np.uint8)
#     edges*=255
#     cv2.imshow('Canny Edges Detection', edges)
    
    cx, cy, r = hough_circles(roiR)
    #roiR = cv2.cvtColor(roiR, cv2.COLOR_GRAY2BGR)
    #leftEye = cv2.circle(roiR, (cx, cy), r, (0, 0, 255), 1)
    #leftEye = resized_by_scale(leftEye, 500)
    #cv2.imshow('Pupil', leftEye)
    #cv2.imwrite('C:\\Users\\ZVSL\\Desktop\\Franziska\\BA\\rightEye_FK_pupil.jpg', leftEye)
    
    crop = roi_PI(roiR, cx, cy, r)
    #pupilRegion = resized_by_scale(crop, 500)
    #cv2.imshow('Pupil region', pupilRegion)
    #cv2.imwrite('C:\\Users\\ZVSL\\Desktop\\Franziska\\BA\\rightEye_FK_roiPI_og.jpg', crop)
    
    cx, cy, r = hough_circles(crop)
    posPupil = (cx, cy)
    print('Pupil coordinates: ', posPupil)

    posPI = purkinje_image(crop, 80, 95)
    print('PI coordinates: ', posPI)

    img = draw_features(crop, posPI, posPupil)
    markedImg = resized_by_scale(img, 1000)
    cv2.imshow('Pupil region with Pupil centre and PI centre marked', markedImg)
    
    edges = cv.Canny(crop, 80, 95)
    edges = resized_by_scale(edges, 1000)
    cv.imshow('edges', edges)
    
