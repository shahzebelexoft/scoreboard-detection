import os, io
import base64
from PIL import Image
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from detect_video_v4 import predict
from utils import *
from flask import Flask, render_template, url_for

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'scoredetection'
app.config['UPLOAD_FOLDER'] = r'static/upload'
# app.use_static_for_assets = True


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Process Video")


class ProcessForm(FlaskForm):
    submit = SubmitField("Process Video")


@app.route('/about')  # Defines the '/about' route
def about():
    print("About...")
    return "About this"


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def  home():
    # Create instances of the forms
    upload_form = UploadFileForm()
    process_form = ProcessForm()

    # Handle file upload
    if upload_form.validate_on_submit():
        file = upload_form.file.data
        try:
            # Create the 'upload' folder if it doesn't exist
            os.makedirs(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    app.config['UPLOAD_FOLDER']))
        except OSError as e:
            # Handle the error if the folder already exists
            e.errno
        # Save the uploaded file to the 'upload' folder
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

    # Handle video processing form submission
    if process_form.validate_on_submit():
        # Get the filename from the uploaded file

        # Get the filename from the uploaded file
        videeo_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        # Process the video and obtain the processed and detected images as NumPy arrays

        database_path, storage_path = os.path.split(videeo_path)

        database_path = extract_filename(storage_path)

        processed_image, detected_image, file_name= predict(videeo_path, storage_path=storage_path,
                                                        database_path=database_path) # type: ignore

        # Convert the NumPy arrays to PIL images
        processed_pil_image = Image.fromarray(processed_image)
        detected_pil_image = Image.fromarray(detected_image)

        # Save the PIL images to bytes
        processed_bytes = io.BytesIO()
        processed_pil_image.save(processed_bytes, format='PNG')

        detected_bytes = io.BytesIO()
        detected_pil_image.save(detected_bytes, format='PNG')

        # Convert the bytes to base64 strings
        processed_base64 = base64.b64encode(processed_bytes.getvalue()).decode('utf-8')
        detected_base64 = base64.b64encode(detected_bytes.getvalue()).decode('utf-8')

        print(file_name)

        # Render the template with the forms and base64 strings of the images
        return render_template('index_v3.html', upload_form=upload_form, process_form=process_form,
                                processed_base64=processed_base64, detected_base64=detected_base64, file_name=file_name)

    # Render the template with the forms
    return render_template('index_v3.html', upload_form=upload_form, process_form=process_form)


@app.route('/view/video/<file_name>')
def display(file_name):
    # print('display_image filename: ' + file_name)
    # return "Hello, world!"
    return render_template('video.html', file_name=file_name)


if __name__ == '__main__':
    # Run the Flask application
    app.run()
