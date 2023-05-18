import cv2
import time
from utils import *
from ultralytics import YOLO
from firebase_db import FirebaseClient

class ScoreBoardDetector:
    def __init__(self, model_path, storage_path, database_path):
        self.db = FirebaseClient()
        self.model = YOLO(model_path)
        self.storage_path = storage_path
        self.database_path = database_path
        self.total_frames = 0
        self.timer_interval = 5
        self.frame_rate = 0
        self.frame_interval = 0
        self.last_detected_scoreboard = None
        self.last_detected = None
        self.scoreboard_detected = False   

    def process(self, video_path):

        cap = cv2.VideoCapture(video_path)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_rate = cap.get(cv2.CAP_PROP_FPS)
        self.frame_interval = int(self.frame_rate * self.timer_interval)
        cap.set(cv2.CAP_PROP_POS_FRAMES, self.total_frames - 1)

        start_time = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            
            start_time = time.time()
            if ret:
                # Detect objects using the YOLO model
                results = self.model(frame, conf=0.65, device='cpu')

                if len(results[0].boxes.xyxy) > 0:
                    self.last_detected = results[0].boxes.xyxy[0]
                    self.last_detected_scoreboard = crop_and_resize(frame, self.last_detected.numpy())
                    scoreboard_detected = True

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Display the annotated frame
                # cv2.imshow('Annotated Image', annotated_frame)

                if scoreboard_detected:
                    # Store in database
                    # cv2.imwrite("misc\detected_scoreboard.jpg", self.last_detected_scoreboard)
                    
                    break

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

                # Move to the previous frame based on the timer interval
                total_frames -= self.frame_interval
                cap.set(cv2.CAP_PROP_POS_FRAMES, max(total_frames - 1, 0))

            else:
                break

        cap.release()

        end_time = time.time()

        total_time = end_time - start_time

        self.db.upload_image(self.storage_path, self.last_detected_scoreboard)
        self.db.save_image_reference(self.database_path, self.storage_path, total_time)


    def access_last_detected_object(self):
        if self.self.last_detected is not None:
            print("Last detected object:", self.self.last_detected)
            cv2.imwrite("misc\Last_detected_score.jpg", self.self.last_detected_scoreboard)
        else:
            print("No object detected in the video.")