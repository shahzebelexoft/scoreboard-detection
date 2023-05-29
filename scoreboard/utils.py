import re
import os
from flask import request


def process_file():
    file_path = request.form.get('file_path')  # Retrieve the file path from the request

    if not file_path:
        return "File path not provided", 400

    # Check if the file exists
    if not os.path.isfile(file_path):
        return "File not found", 404

    # Process the file
    # Perform your desired operations on the file using the provided file_path
    # For example:
    with open(file_path, 'r') as file:
        content = file.read()
        # Process the file content here

    # Return the response or perform further actions
    return "File processed successfully"


def crop_and_resize(img, box):
    """
    Crop a region of interest (ROI) from an image based on the given bounding box coordinates and resize it.

    Args:
        img (numpy.ndarray): Input image.
        box (numpy.ndarray): Bounding box coordinates in the format [x1, y1, x2, y2].

    Returns:
        numpy.ndarray: Cropped and resized region of interest.
    """
    # Get the bounding box coordinates
    x1, y1, x2, y2 = box

    # Round the values
    x1 = round(x1)
    y1 = round(y1)
    x2 = round(x2)
    y2 = round(y2)

    # Crop the region of interest
    roi = img[y1:y2, x1:x2]

    if len(roi) == 0:
        pass
    else:
        return roi


def bbox(results):
    """
    Extract the bounding box coordinates from YOLO model results.

    Args:
        results (list): List of YOLO model results.

    Returns:
        numpy.ndarray: Bounding box coordinates in the format [x1, y1, x2, y2].
    """
    if len(results[0].boxes.xyxy) == 1:
        for result in results:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            probs = result.probs  # Class probabilities for classification outputs

        box = boxes[0].xyxy
        return box
    else:
        pass


def extract_filename(filename):
    # Remove the file extension
    filename = filename.rsplit('.', 1)[0]

    # Remove numbers and symbols
    cleaned_filename = re.sub('[^a-zA-Z\s]', '', filename)

    # Remove extra whitespace
    cleaned_filename = ' '.join(cleaned_filename.split())

    return cleaned_filename
