# Python program to explain cv2.ellipse() method 
	
# importing cv2 
import cv2 
	
# Reading an image in default mode 
image = cv2.imread("images/lena.png") 

center_coordinates = (120, 100) 

axesLength = (100, 50) 

angle = 30

startAngle = 0

endAngle = 360

# Blue color in BGR 
color = (255, 0, 0) 

# Line thickness of -1 px 
thickness = 4

# Using cv2.ellipse() method 
# Draw a ellipse with blue line borders of thickness of -1 px 
image = cv2.ellipse(image, center_coordinates, axesLength, angle, 
						startAngle, endAngle, color, thickness) 

# Displaying the image 
cv2.imshow("win", image)
cv2.waitKey(0)
