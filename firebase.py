import urllib
import pyrebase

firebase_config = {
    "apiKey": "AIzaSyAC2UsfEPtz4eQohQ80fRdfv5yDuOWGbGo",
    "databaseURL": "https://scoreboard-detection-default-rtdb.asia-southeast1.firebasedatabase.app",
    "authDomain": "scoreboard-detection.firebaseapp.com",
    "projectId": "scoreboard-detection",
    "storageBucket": "scoreboard-detection.appspot.com",
    "messagingSenderId": "848958562903",
    "appId": "1:848958562903:web:0dec71f394a6d180e43912",
    "measurementId": "G-PJSXSC39MP"
}

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()
# auth = firebase.auth()
# storage = firebase.storage()

################### AUTHENTICATIOM #######################
# # Log in
# email = input("Enter your email: ")
# password = input("Enter password: ")

# try:
#     auth.sign_in_with_email_and_password(email, password)
#     print("Successfully signed in!")
# except:
#     print("Invalid username or password!")

# # Sign Up
# email = input("Enter your email: ")
# password = input("Enter password: ")

# confirmpass = input("Confirm password: ")

# if password == confirmpass:
#     try:
#         auth.create_user_with_email_and_password(email, password)
#         print("Account successfully created!")
#     except:
#         print("Email already exists!")

############################## STORAGE ###############################
# Uploading file
# file_name = input("Upload the name of filename that you want to to upload: ")
# cloudfilename = input("Rename the file name in the cloud: ")
# storage.child(cloudfilename).put(file_name)

# # Get URL
# print(storage.child(cloudfilename).get_url(None))

# # Downloading file
# cloudfilename = input("Enter the name of the file that you want to download:")
# storage.child(cloudfilename).download("", "download.jpg")

# # Reading file
# cloudfilename = input("Enter the name of the file that you want to download: ")
# url = storage.child(cloudfilename).get_url(None)
# f = urllib.request.urlopen(url).read()
# print(f)

############################## REALTIME DATABASE ###############################
# data = {"age": 37, "address": "Rawalpindi", "employed": True, "name": "Omar"}
# db.child("People").child("asdadsafa").set(data)

# Update data
# db.child("People").child("asdadsafa").update({'name': 'Jane'})

# people = db.child("People").get()
# for person in people.each():
#     if person.val()['name'] == 'Omar':
#         db.child("People").child(person.key()).update({'name' : 'Jane'})

# Delete
# db.child("People").child("Person").remove()

# people = db.child("People").get()
# for person in people.each():
#     if person.val()['name'] == 'Shah Zeb':
#         db.child("People").child(person.key()).child("age").remove()

# Read
# people =  db.child("People").child("-NVZ9LDCQl5_d7zpzOK7").get()
# print(people.val())

# people =  db.child("People").order_by_child("name").equal_to("Jane").get()
# for person in people.each():
#     print(person.val())