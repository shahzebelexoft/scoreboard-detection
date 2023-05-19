import cv2
import time
import numpy as np
from utils import *
import datetime
from config import MODEL_PATH
from ultralytics import YOLO
from firebase_db import FirebaseClient

def predict(video_path, storage_path, database_path):
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Load the YOLO model
    model = YOLO(MODEL_PATH)

    # Open video file
    cap = cv2.VideoCapture(video_path)

    # Get total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # # Get the frame width, height, and frame rate
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set timer parameters
    timer_interval = 5  # in seconds
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(frame_rate * timer_interval)

    output = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*'MPEG'), frame_rate, (frame_width, frame_height))

    # Set the position to the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

    # Initialize the detected frames and scoreboards
    last_detected = None
    last_detected_scoreboard = None

    # If video is not open then give error
    if not cap.isOpened():
        print("Error opening video file")

    else:
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

                if scoreboard_detected:
                    break

                # writing the new frame in output
                output.write(frame)

                # Move to the previous frame based on the timer interval
                total_frames -= frame_interval
                cap.set(cv2.CAP_PROP_POS_FRAMES, max(total_frames - 1, 0))
            
            else:
                break
        
        # output.release()
        cap.release()

        end_time = time.time()

        # Upload the detected scoreboard image and reference video to Firebase
        db.upload(storage_path, last_detected_scoreboard)

        # Save the image reference and processing time in the database
        db.save_image_reference(database_path, storage_path, end_time - start_time, timestamp_str, formatted_datetime)

        # Save the image reference and processing time in the firestore database
        URL = db.store_firestore(database_path, storage_path, end_time - start_time, timestamp_str, formatted_datetime)

        return frame, last_detected_scoreboard, URL
