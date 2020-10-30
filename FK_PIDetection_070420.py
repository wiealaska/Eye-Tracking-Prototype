import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Return average intensity of a given 1D array
# Param: area = 1D-array
def build_average(area):
    sum, i = 0, 0
    for pixel in area: # what type of array is given? Preferable 1D
        sum += pixel
        i += 1
    return sum/i

# Return a cropped image with a specified size and given center coordinates
# Param: image=2D-array, startPos=tuple, size=int
# Return: image=2D-array
def crop(image, centerPos, pix):
    x = centerPos[0]
    y = centerPos[1]
    x1 = x - pix
    y1 = y - pix
    x2 = x + pix 
    y2 = y + pix 
    h, w = image.shape
    if y1 < 0:
        y1 = 0
    if x1 < 0:
        x1 = 0
    if y2 > h:
        y2 = h
    if x2 > w:
        x2 = w 
    area = image[y1:y2, x1:x2]
    return area

# check if a surrounding areas have a bigger value than the current positions area
def check_neighborhood(x, y, img):
    h, w = len(img), len(img[0])
    i,j=-1,-1
    while i <= 1:
        if y+i >= 0 and y+i < h:
            while j<=1:
                rect1 = crop(img,(x,y),1)
                av1 = build_average(rect1.ravel())
                rect2 = crop(img, (x+j, y+i), 1)
                av2 = build_average(rect2.ravel())
                if x+j >= 0 and x+j < w and  av2 > av1:
                    x = x+j
                    y = y+i
                    return x,y
                else:
                    j += 1
            j = -1
            i += 1
    return x,y

def purkinje_image(img, lth, hth):
    # check if image is already bw
    if len(img.shape) < 3:
        imgray = img
    else:
        imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #imgray = cv.blur(imgray, (3,3))
    
    pltim = plt.imshow(imgray, cmap=plt.cm.gray)
    plt.show()

    edges = cv.Canny(imgray, lth, hth) #maybe other canny function?
    pltim = plt.imshow(edges, cmap=plt.cm.gray)
    plt.show()
    contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cv.imwrite('C:\\Users\\ZVSL\\Desktop\\Franziska\\BA\\rightEye_FK_roiPI_contours.jpg', contours)
    h, w = imgray.shape
    mat = np.zeros((h, w), np.uint8)
    # check the contours
    for c in contours:
        # build an average intensity for the area around a contour coordinate
        for [[x,y]] in c:
            rect = crop(imgray, (x,y), 2)
            rect1D = rect.ravel()
            average = build_average(rect1D)
            av = average/5
            # add the average value to the corresponding field in a matrix of zeros
            i, j = -1, -1
            while i <= 1:
                if y+i >= 0 and y+i < h:
                    while j <= 1:
                        if x+j >= 0 and x+j < w:
                            mat[y+i][x+j] += av
                        j += 1
                j = -1
                i += 1
    # determine the maxVal and maxLoc in the created density matrix mat
    # check if the image has a higher value for the second highest value of mat
    while True:
        minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(mat)
        x = maxLoc[0]
        y = maxLoc[1]
        mat[y][x] = 0
        minVal2, maxVal2, minLoc2, maxLoc2 = cv.minMaxLoc(mat)
        x2 = maxLoc2[0]
        y2 = maxLoc2[1]
        if imgray[y][x] > imgray[y2][x2]:
            break
    pltim = plt.imshow(mat, cmap=plt.cm.gray)
    plt.show()
    # check for a brighter area in neighborhood
    while True:
        posPI = check_neighborhood(x,y,imgray)
        x,y = posPI
        if posPI == check_neighborhood(x,y,imgray):
            break
        
    return posPI

if __name__ == "__main__":
    pass

