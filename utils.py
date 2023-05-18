import re
import cv2
import numpy as np
from skimage.filters import sobel
from skimage.segmentation import watershed


def preprocess(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    otsu_blur = sobel(thresh)

    markers = np.zeros_like(thresh)

    markers[thresh < 15] = 1

    markers[thresh > 75] = 2

    segmentation_otsu_blur = watershed(otsu_blur, markers)

    segmentation_normalized = cv2.normalize(src=segmentation_otsu_blur, dst = None, alpha = 0, beta = 255,
                                        norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)
    
    return thresh

def crop_image(input, image):

    contours, hierarchy = cv2.findContours(input, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

    contours_poly = [None] * len(contours)

    boundRect = []

    for i, c in enumerate(contours):
        if hierarchy[0][i][3] == -1:
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect.append(cv2.boundingRect(contours_poly[i]))

    for i in range(len(boundRect)):
        color = (0, 255, 0)
        cv2.rectangle(image, (int(boundRect[i][0]), int(boundRect[i][1])), \
                    (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
        
    # cropped_list = []

    # for i in range(len(boundRect)):

    #     dimension_offset = 5
    #     position_offset = 2

    #     x, y, w, h = boundRect[i]
    #     h = h + dimension_offset
    #     w = w + dimension_offset
    #     x = x - position_offset
    #     y = y - position_offset

    #     cropped = input[y: y + h, x : x + w]

    #     cropped_list.append(cropped)

    return boundRect


def load_and_resize(img):
    """
    Load an image and resize it to a fixed size.

    Args:
        img (str): Path to the image file.

    Returns:
        numpy.ndarray: Resized image.
    """
    img = cv2.imread(img)
    img = cv2.resize(img, (640, 640))
    return img


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
