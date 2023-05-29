from scoreboard.models import score_board
from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'scoredetection'
key = app.config['SECRET_KEY']

app.config['UPLOAD_FOLDER'] = r'scoreboard/static/upload'
upload_folder = app.config['UPLOAD_FOLDER']

app.config['VIDEOS_FOLDER'] = r'scoreboard\videos'
video_directory = app.config['VIDEOS_FOLDER']

from scoreboard import routes
