import cv2
import time
import numpy as np
from utils import *
import datetime
from config import MODEL_PATH
from ultralytics import YOLO
from firebase_db import FirebaseClient

def predict(video_path, storage_path, database_path):
    # Load the YOLO model
    model = YOLO(MODEL_PATH)

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

    # Initialize the scoreboard detected flag
    scoreboard_detected = False

    # Instantiate the class for firebase
    db = FirebaseClient()

    start_time = time.time()

    # Start reading and processing the video
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:

            # Get the timestamp of the current frame
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)

            # Convert the timestamp to a datetime object
            timestamp = datetime.timedelta(milliseconds=timestamp)

            # Format the timestamp as hours:minutes:seconds
            timestamp_str = str(timestamp).split('.', 2)[0]

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

    # Upload the detected scoreboard image to Firebase
    db.upload_image(storage_path, last_detected_scoreboard)

    # Save the image reference and processing time in the database
    db.save_image_reference(database_path, storage_path, end_time - start_time, timestamp_str)

    # Save the image reference and processing time in the firestore database
    db.store_firestore(database_path, storage_path, end_time - start_time, timestamp_str)

    return frame, last_detected_scoreboard
