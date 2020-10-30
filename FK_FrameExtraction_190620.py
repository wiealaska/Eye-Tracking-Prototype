# frame extraction script

import cv2
import os
import sys

# convert a h264 file to a mp4 file
# saves the new file in the same directory as h264 file
# if mp4 file already exists the script terminates
def convert(path):
    vid = os.path.basename(path)
    vid = vid.split('.')[0]
    directory = os.path.dirname(path)
    os.chdir(directory)
    if os.path.exists(vid + '.mp4'):
        pass
    else:
        command = "MP4Box -add %s.h264 %s.mp4"% (vid, vid)
        os.system(command)
        print("vid conv")
     
# Opens the Video file
def frame_capture(path, frames):
    # Read the video from specified path
    # Attention: cv2 needs another video container than h264, e.g. mp4, avi
    cam = cv2.VideoCapture(path) 
    file = os.path.basename(path)
    file = file.split('.')[0]
    directory = os.path.dirname(path)
    os.chdir(directory)
    
    totalframes= cam.get(7)
    framerate = cam.get(5)
    print(totalframes, framerate)
    
    try: 
          
        # creating a folder named like the file
        folder = '../Frames/' + file
        os.makedirs(folder)     
      
    # if not created then raise error 
    except OSError:
        if os.path.exists(folder):
            print('Folder already exists; Frames are already extracted')
        else: 
            print ('Error: Creating directory')
        return
      
    # frame
    # read the frame after 2 sec of focussing on the target + 3 sec of video in advance
    counter = 1
    totalframes= cam.get(7)
    print(totalframes)
    points = 35
    recTime = 3*points+3 # calibration duration
    fps = totalframes/recTime # the intern fps Anzeige by cv2 does not work correctly
    print(fps)
    currentframe = 5 * fps - int(frames/2)
    print(currentframe)
    
    cam.set(1, int(currentframe))
      
    while currentframe+int(frames/2) <= totalframes: 
        for i in range(frames): 
            # reading from frame 
            ret,frame = cam.read() 
      
            if ret: 
                # if video is still left continue creating images 
                name = '../Frames/%s/%s_frame_pos'% (file,file) + str(counter) + '.jpg'
                print ('Creating... ' + name) 
      
                # writing the extracted images 
                cv2.imwrite(name, frame) 
                cam.set(1, int(currentframe)+i)
            else:
                break
        # increasing counter so that it will 
        # show how many frames are created
        counter += 1
        # by modifying current frame you can change frame to capture
        currentframe += 3 * fps # capturing a frame every 3 seconds
        print(currentframe)
        cam.set(1, int(currentframe))        
      
    # Release all space and windows once done 
    cam.release() 
    cv2.destroyAllWindows()

# Driver Code - really nesseccary?
if __name__ == '__main__': 
  
    # Calling the function
    convert("C:/Users/ZVSL/Desktop/Franziska/Tests/Videos/fk_cal3434_rep3.h264")
    frame_capture("C:/Users/ZVSL/Desktop/Franziska/Tests/Videos/fk_cal66666_rep1.mp4", 1)
    

