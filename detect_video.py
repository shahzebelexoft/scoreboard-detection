import cv2
import numpy as np
from utils import *
import time
from ultralytics import YOLO
from firebase_db import FirebaseClient

# Provide the path to the video
video_path = r"data\videos\NFL Football\nfl_football_2.mp4"

# Provide storage and database path in the database
storage_path = "detected_score.jpg"
database_path = "Basketball"

# Provide the path to the pre-trained model
model_path = r"runs\detect\train5\weights\last.pt"

# Load the YOLO model
model = YOLO(model_path)

# Open video file
cap = cv2.VideoCapture(video_path)

# Get total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Set timer parameters
timer_interval = 5  # in seconds
frame_rate = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(frame_rate * timer_interval)

# Set the position to the last frame
cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

# Initialize the detected frames and scoreboards
last_detected = None
last_detected_scoreboard = None

# If video is not open then give error
if not cap.isOpened():
    print("Error opening video file")

# Initialize the frame counter
frame_counter = 0

# Initilalize the scoreboard detected
scoreboard_detected = False

# Instantiate the class for firebase
db = FirebaseClient()

# Start reading and processing the video
while cap.isOpened():
    ret, frame = cap.read()
    
    start_time = time.time()
    if ret:
        # Detect objects using the YOLO model
        results = model(frame, conf=0.65, device='cpu')

        if len(results[0].boxes.xyxy) > 0:
            last_detected = results[0].boxes.xyxy[0]
            last_detected_scoreboard = crop_and_resize(frame, last_detected.numpy())
            scoreboard_detected = True

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        # cv2.imshow('Annotated Image', annotated_frame)

        if scoreboard_detected:
            # Store in database
            # cv2.imwrite("misc\detected_scoreboard.jpg", last_detected_scoreboard)
            
            break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Move to the previous frame based on the timer interval
        total_frames -= frame_interval
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(total_frames - 1, 0))

    else:
        break

cap.release()

end_time = time.time()

total_time = end_time - start_time

db.upload_image(storage_path, last_detected_scoreboard)
db.save_image_reference(database_path, storage_path, total_time)

cv2.destroyAllWindows()

# Access the last detected object
if last_detected is not None:
    print("Last detected object:", last_detected)
    cv2.imwrite("misc\Last_detected_score.jpg", last_detected_scoreboard)
else:
    print("No object detected in the video.")
