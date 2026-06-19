import cv2
import numpy as np
import time
# A required callback method that goes into the trackbar function.
def nothing(x):
    pass

# you don't have to use the trackbars. 
# you can instead choose to use the mouse click to select the pixel location.
# he selected pixel location will be printed in the console.

selected_point = None


def mouse_callback(event, x, y, flags, param):
    global selected_point
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_point = (x, y)
        print(f"Clicked pixel location: {selected_point}")

# Initializing the webcam feed.
cam = cv2.VideoCapture(0)

# Create a window named trackbars.
cv2.namedWindow("Trackbars")
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_callback)

# Now create 6 trackbars that will control the lower and upper range of 
# H,S and V channels. The Arguments are like this: Name of trackbar, 
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.createTrackbar("Coordinate 1", "Trackbars", 0, 900, nothing)
cv2.createTrackbar("Coordinate 2", "Trackbars", 0, 600, nothing)



while True:
    # Start reading the webcam feed frame by frame.
    ret, frame = cam.read()
    if not ret:
        break
        
    # Flip the frame horizontally (Not required)
    # frame = cv2.flip( frame, 1 )
    
    coord1 = cv2.getTrackbarPos("Coordinate 1", "Trackbars")
    coord2 = cv2.getTrackbarPos("Coordinate 2", "Trackbars")
    
    cv2.circle(frame, (coord1, coord2), 3, (0,0,255), -1)

    if selected_point is not None:
        cv2.circle(frame, selected_point, 3, (0, 255, 0), -1)
    
    cv2.imshow("Frame",frame)
    
    if cv2.waitKey(1)==27:
        break

cam.release()
cv2.destroyAllWindows()
    