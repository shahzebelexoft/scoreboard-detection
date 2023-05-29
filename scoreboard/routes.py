import os
from urllib.parse import quote
from werkzeug.utils import secure_filename
from flask import render_template, redirect

from scoreboard import app, upload_folder, video_directory
from scoreboard.forms import UploadFileForm, DirectoryForm
from scoreboard.utils import extract_filename
from scoreboard.models import process_video


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    upload_form = UploadFileForm()
    # directory_form = DirectoryForm()

    if upload_form.validate_on_submit():
        file = upload_form.file.data

        try:
            # Create the 'upload' upload_folder if it doesn't exist
            os.makedirs(os.path.join(upload_folder), exist_ok=True)
        except OSError as e:
            # Handle the error if the upload_folder already exists
            print("Error:", e.errno)

        # Save the uploaded file to the 'upload' upload_folder
        file_path = os.path.join(upload_folder, secure_filename(file.filename))
        file.save(file_path)

        # Get the filename from the uploaded file
        video_path = file_path

        # Process the video and obtain the processed and detected images as NumPy arrays
        database_path, storage_path = os.path.split(video_path)
        database_path = extract_filename(storage_path)

        processed_base64, detected_base64, file_name = process_video(video_path, storage_path, database_path)

        # Render the template with the forms and base64 strings of the images
        return render_template('home.html', upload_form=upload_form, processed_base64=processed_base64, 
                                detected_base64=detected_base64, file_name=file_name)

    # elif directory_form.validate_on_submit():
    #     directory_path = directory_form.directory_path.data

    #     # full_video_path = os.path.join(video_directory, directory_path)

    #     # full_video_path = quote(full_video_path)

    #     return redirect(f'/view/files/{directory_path}')

    return render_template('home.html', upload_form=upload_form, video_directory=video_directory)


@app.route('/view/files/<video_directory>', methods=['GET', 'POST'])
def view_files(video_directory):
    folders = os.listdir(video_directory)
    
    folder_files = {}
    
    for folder in folders:
        folder_files[folder] = os.listdir(os.path.join(video_directory, folder))
    
    return render_template('files.html', video_directory=video_directory, folders=folders, folder_files=folder_files)


@app.route('/view/video_1/<file_name>')
def display_1(file_name):
    return render_template('video_1.html', file_name=file_name)


@app.route('/detection/<video_directory>/<folder>/<file>', methods=['GET', 'POST'])
def detection(video_directory, folder, file):
    video_path = os.path.join(video_directory, folder, file)

    # Process the video and obtain the processed and detected images as NumPy arrays
    database_path, storage_path = os.path.split(video_path)
    database_path = extract_filename(storage_path)

    processed_base64, detected_base64, file_name = process_video(video_path, storage_path, database_path)

    return render_template('prediction.html', processed_base64=processed_base64, detected_base64=detected_base64,
                            file=file, folder=folder, video_directory=video_directory)

@app.route('/view/video_2/<video_directory>/<folder>/<file>')
def display_2(video_directory, folder, file):
    # folders = full_video_path.split("\\")
    # folder = folders[2]
    return render_template('video_2.html', video_directory=video_directory, folder=folder, file=file)
