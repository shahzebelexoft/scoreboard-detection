import pyrebase
from PIL import Image
from io import BytesIO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from scoreboard.config import FIREBASE_CONFIG, CRED


class FirebaseClient:
    def __init__(self, config=FIREBASE_CONFIG, cred=CRED):
        # Initialize the Firebase app with the provided configuration
        self.firebase = pyrebase.initialize_app(config)
        # Get a reference to the Firebase Storage
        self.storage = self.firebase.storage()
        if not firebase_admin._apps:
            self.cred = credentials.Certificate(cred)
            firebase_admin.initialize_app(self.cred)
        self.db_s = firestore.client()

    def get(self, path):
        # Retrieve data from the Firebase Realtime Database at the specified path
        return self.firebase.database().child(path).get().val()

    def put(self, path_1, path_2, data):
        # Set data in the Firebase Realtime Database at the specified path
        return self.firebase.database().child(path_1).child(path_2).set(data)

    def delete(self, path):
        # Remove data from the Firebase Realtime Database at the specified path
        return self.firebase.database().child(path).remove()

    def upload(self, storage_path, image_data):
        # Convert NumPy array to PIL image
        image = Image.fromarray(image_data)

        # Convert image to bytes
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG', quality=95, subsampling=0)
        image_bytes.seek(0)

        # Upload image data to Firebase Storage at the specified path
        self.storage.child(f'{storage_path[:-4]}.jpg').put(image_bytes)

    def save_image_reference(self, database_path, storage_path, time, time_stamp, date_time):
        # Save the image reference (download URL) in the Firebase Realtime Database at the specified path
        data = {"file name": storage_path,
                "image name": f'{storage_path[:-4]}.jpg',
                "image url": self.storage.child(f'{storage_path[:-4]}.jpg').get_url(None),
                "inference time taken": time,
                "time stamp": time_stamp,
                "updated at": date_time}
        self.put(database_path, storage_path[:-4], data)

    def store_firestore(self, database_path, storage_path, time, time_stamp, date_time):
        data = {"file name": storage_path,
                "image name": f'{storage_path[:-4]}.jpg',
                "image url": self.storage.child(f'{storage_path[:-4]}.jpg').get_url(None),
                "inference time taken": time,
                "time stamp": time_stamp,
                "updated at": date_time}

        ref = self.db_s.collection(database_path).document(f'{storage_path[:-4]}')

        ref.set(data)

        return data["file name"]
