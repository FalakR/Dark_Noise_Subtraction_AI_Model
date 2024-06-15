"""
Python Script to first generate a dark image by meta data matching and then subtract the dark image from original
image

Main Guides:
1. Tutorial: Illumination correction -
https://clouard.users.greyc.fr/Pantheon/experiments/illumination-correction/index-en.html

2. ChatGPT : https://chatgpt.com/share/7656d1e5-9671-4ba3-a0fa-995ad238922f

"""

import exifread
import cv2
import numpy as np


# Extract Meta Data from Original Image now

def extract_metadata(image_path):
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
    metadata = {
        'ExposureTime': tags.get('EXIF ExposureTime'),
        'ISOSpeedRatings': tags.get('EXIF ISOSpeedRatings'),
        'DateTime': tags.get('EXIF DateTimeOriginal'),
        'Temperature': tags.get('EXIF Temperature', None)  # Custom field if available
    }
    return metadata


# Example implementation
original_image_metadata = extract_metadata('original_image.jpg')


# Match Meta Data now
def find_best_match(original_metadata, dark_frames_metadata):  # Will have to input a dict of dark frames.
    best_match = None
    min_difference = float('inf')

    for dark_frame_path, dark_metadata in dark_frames_metadata.items():
        # Calculate difference based on relevant metadata
        exposure_diff = abs(
            float(original_metadata['ExposureTime'].values[0]) - float(dark_metadata['ExposureTime'].values[0]))
        iso_diff = abs(
            int(original_metadata['ISOSpeedRatings'].values[0]) - int(dark_metadata['ISOSpeedRatings'].values[0]))
        # Add more comparisons as needed (e.g., temperature, date/time)

        # Simple sum of differences, could be more complex
        total_diff = exposure_diff + iso_diff

        if total_diff < min_difference:
            min_difference = total_diff
            best_match = dark_frame_path

    return best_match


# Example dictionary of dark frames metadata
dark_frames_metadata = {
    'dark_frame1.jpg': extract_metadata('dark_frame1.jpg'),
    'dark_frame2.jpg': extract_metadata('dark_frame2.jpg'),
    # Add more dark frames
}

best_dark_frame = find_best_match(original_image_metadata, dark_frames_metadata)


# Finally use the matched dark frame
# Load the matched dark frame
dark_image = cv2.imread(best_dark_frame, cv2.IMREAD_GRAYSCALE)

# Load the original image
original_image = cv2.imread('original_image.jpg', cv2.IMREAD_GRAYSCALE)

# Ensure the images have the same dimensions
if original_image.shape != dark_image.shape:
    raise ValueError("Original and dark images must have the same dimensions")

# Subtract dark image from original image
intermediate_image = original_image.astype(np.float32) - dark_image.astype(np.float32)

# Calculate mean value of the dark image
mean_dark_value = np.mean(dark_image)

# Add mean value to the intermediate image
corrected_image = intermediate_image + mean_dark_value

# Clip values to valid range [0, 255] and convert to uint8
corrected_image = np.clip(corrected_image, 0, 255).astype(np.uint8)

# Save the corrected image
cv2.imwrite('corrected_image.jpg', corrected_image)
