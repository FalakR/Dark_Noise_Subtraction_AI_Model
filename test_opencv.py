"""testing an import"""
import cv2
import numpy as np

# Create an image with a black background
image = np.zeros((500, 500, 3), dtype="uint8")

# Draw a white rectangle
cv2.rectangle(image, (50, 50), (450, 450), (255, 255, 255), -1)

# Display the image
cv2.imshow('Test Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""Run this script. If a window displaying a white rectangle on a black background pops up, OpenCV is installed 
correctly"""
