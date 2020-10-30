# Eye-Tracking-Prototype
Code for a video-based eye tracking prototype written in Python

The eye tracking works by extracting eye features from video frames of the user's face. The pupil and the Purkije image are determined in the image of the eye. 
Their relation vector, the pg-vector, is calculated and mapped to according screen coordinates of a calibration target's position. 
For the mapping a 2D-regression is used. 
