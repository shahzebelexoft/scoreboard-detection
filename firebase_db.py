import pyrebase
import numpy as np
from PIL import Image
from io import BytesIO
from config import FIREBASE_CONFIG

class FirebaseClient:
    def __init__(self, config = FIREBASE_CONFIG):
        # Initialize the Firebase app with the provided configuration
        self.firebase = pyrebase.initialize_app(config)
        # Get a reference to the Firebase Storage
        self.storage = self.firebase.storage()

    def get(self, path):
        # Retrieve data from the Firebase Realtime Database at the specified path
        return self.firebase.database().child(path).get().val()

    def put(self, path, data):
        # Set data in the Firebase Realtime Database at the specified path
        return self.firebase.database().child(path).set(data)

    def delete(self, path):
        # Remove data from the Firebase Realtime Database at the specified path
        return self.firebase.database().child(path).remove()

    def upload_image(self, storage_path, image_data):
        # Convert NumPy array to PIL image
        image = Image.fromarray(image_data)

        # Convert image to bytes
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)
        
        # Upload image data to Firebase Storage at the specified path
        self.storage.child(storage_path).put(image_bytes)

    def save_image_reference(self, database_path, storage_path, time):
        # Save the image reference (download URL) in the Firebase Realtime Database at the specified path
        data = {"image_name": storage_path, 
                "image_url": self.storage.child(storage_path).get_url(None),
                "inference time taken": time}
        self.put(database_path, data)
