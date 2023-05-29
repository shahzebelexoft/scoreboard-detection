from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import InputRequired, DataRequired


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Process Video")
    
class DirectoryForm(FlaskForm):
    directory_path = StringField('Directory Path', validators=[DataRequired()])
    submit = SubmitField('Submit')