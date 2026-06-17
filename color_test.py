#finding hsv range of target object(pen)
import cv2
import numpy as np
import time
import serial
from serial.tools import list_ports
# A required callback method that goes into the trackbar function.
def nothing(x):
    pass


def open_arduino_serial():
    preferred_tokens = ("arduino", "ch340", "usb serial", "cp210", "ttyacm", "ttyusb")
    discovered_ports = []

    for port_info in list_ports.comports():
        description = f"{port_info.description} {port_info.manufacturer or ''} {port_info.hwid or ''}".lower()
        if any(token in description for token in preferred_tokens):
            discovered_ports.insert(0, port_info.device)
        else:
            discovered_ports.append(port_info.device)

    fallback_ports = ["COM3", "COM4", "COM5", "/dev/ttyACM0", "/dev/ttyUSB0"]

    for port_name in discovered_ports + fallback_ports:
        try:
            return serial.Serial(
                port=port_name,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1,
                write_timeout=1,
            )
        except serial.SerialException:
            continue

    raise RuntimeError("Could not find the Arduino serial port. Update the port list in color_test.py.")


def set_lights(ser, mode):
    if mode == "top":
        ser.write(b"Z")
        time.sleep(0.05)
        ser.write(b"D")
        time.sleep(0.05)
        ser.write(b"T")
    elif mode == "bottom":
        ser.write(b"Z")
        time.sleep(0.05)
        ser.write(b"D")
        time.sleep(0.05)
        ser.write(b"B")
    else:
        ser.write(b"Z")

# Initializing the webcam feed.
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

ser = open_arduino_serial()
light_mode = None

print("Controls: press 't' for top lights, 'b' for bottom lights, 'o' to turn lights off, ESC to quit, 's' to save HSV values.")

# Create a window named trackbars.
cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of 
# H,S and V channels. The Arguments are like this: Name of trackbar, 
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
 
while True:
    
    # Start reading the webcam feed frame by frame.
    ret, frame = cap.read()
    if not ret:
        break
    # Flip the frame horizontally (Not required)
    frame = cv2.flip( frame, 1 )
    path = '/home/pi/b_white.png'
    
    
    # Convert the BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get the new values of the trackbar in real time as the user changes 
    # them
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
 
    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])
    
    # Filter the image and get the binary mask, where white represents 
    # your target color
    mask = cv2.inRange(hsv, lower_range, upper_range)
 
    # You can also visualize the real part of the target color (Optional)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Converting the binary mask to 3 channel image, this is just so 
    # we can stack it with the others
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # stack the mask, orginal frame and the filtered result
    stacked = np.hstack((mask_3,frame,res))
    
    # Show this stacked frame at 40% of the size.
    cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))
    
    # If the user presses ESC then exit the program
    key = cv2.waitKey(1)
    if key == 27:
        break

    if key == ord('t'):
        light_mode = "top"
        set_lights(ser, light_mode)
        print("Top rings on.")
        continue

    if key == ord('b'):
        light_mode = "bottom"
        set_lights(ser, light_mode)
        print("Bottom rings on.")
        continue

    if key == ord('o'):
        light_mode = None
        set_lights(ser, "off")
        print("Lights off.")
        continue
    
    # If the user presses `s` then print this array.
    if key == ord('s'):
        
        thearray = [[l_h,l_s,l_v],[u_h, u_s, u_v]]
        print(thearray)
        
        # Also save this array as penval.npy
        np.save('hsv_value',thearray)
        break
    
# Release the camera & destroy the windows.    
cap.release()
set_lights(ser, "off")
ser.close()
cv2.destroyAllWindows()


