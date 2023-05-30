import io
import cv2
import time
import base64
import datetime
import numpy as np
from PIL import Image
from ultralytics import YOLO
from scoreboard.utils import *
from scoreboard.config import MODEL_PATH
from scoreboard.database import FirebaseClient
import torch


def score_board(video_path, storage_path, database_path):
    
    #Set the device to gpu or cpu
    if torch.cuda.is_available():
        torch.cuda.set_device(0)  # Set the device index if multiple GPUs are available
        DEVICE = torch.device("cuda")
    else:
        DEVICE = torch.device("cpu")
        
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
                results = model(frame, conf=0.65, device=DEVICE)

                if len(results[0].boxes.xyxy) > 0:
                    last_detected = results[0].boxes.xyxy[0]
                    last_detected_scoreboard = crop_and_resize(frame, last_detected.numpy())
                    scoreboard_detected = True

                if scoreboard_detected:
                    break

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
        file_name = db.store_firestore(database_path, storage_path, end_time - start_time, timestamp_str,
                                    formatted_datetime)

        return frame, last_detected_scoreboard, file_name


def process_video(video_path, storage_path, database_path):
    processed_image, detected_image, file_name = score_board(video_path, storage_path=storage_path,
                                                        database_path=database_path)  # type: ignore

    # Convert the NumPy arrays to PIL images
    processed_pil_image = Image.fromarray(np.uint8(processed_image))
    detected_pil_image = Image.fromarray(np.uint8(detected_image))

    # Swap color channels if necessary (from RGB to BGR)
    if processed_pil_image.mode == 'RGB':
        processed_pil_image = processed_pil_image.convert('RGB')
        processed_pil_image = processed_pil_image.split()
        processed_pil_image = Image.merge('RGB', (processed_pil_image[2], processed_pil_image[1], processed_pil_image[0]))

    if detected_pil_image.mode == 'RGB':
        detected_pil_image = detected_pil_image.convert('RGB')
        detected_pil_image = detected_pil_image.split()
        detected_pil_image = Image.merge('RGB', (detected_pil_image[2], detected_pil_image[1], detected_pil_image[0]))

    # Save the PIL images to bytes
    processed_bytes = io.BytesIO()
    processed_pil_image.save(processed_bytes, format='PNG')

    detected_bytes = io.BytesIO()
    detected_pil_image.save(detected_bytes, format='PNG')

    # Convert the bytes to base64 strings
    processed_base64 = base64.b64encode(processed_bytes.getvalue()).decode('utf-8')
    detected_base64 = base64.b64encode(detected_bytes.getvalue()).decode('utf-8')

    return processed_base64, detected_base64, file_name
