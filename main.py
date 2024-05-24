import os
import flask
from matplotlib import pyplot as plt
from PIL import Image
from flask import Flask, render_template, redirect, url_for, session
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from image_rebuild import graf, polosa

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__, template_folder="templates")
photos = UploadSet('photos', IMAGES)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.getcwd(), 'uploads')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'),
                      FileRequired('File was empty!')])
    submit = SubmitField('Upload')

@app.route("/retry")
def retry():
    try:
        for p in os.listdir("uploads"):
            os.remove(f'uploads/{p}')
    except:
        pass
    return flask.redirect('/')

@app.route("/", methods=['GET', 'POST'])
def image():
    form = UploadForm()
    polosa_image = None
    histogram_image = None

    for filename in os.listdir(app.config['UPLOADED_PHOTOS_DEST']):
        file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Не удалось удалить файл {filename}: {e}')


    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        session['file_url'] = file_url

        file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
        image = Image.open(file_path)
        polosa_image = polosa(image, 10)
        polosa_image.save('static/polosa_image.png')
        histogram_image = graf(image)

    return render_template('index.html', form=form, polosa_image=polosa_image, histogram_image=histogram_image)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == "__main__":
    app.run(debug=True)

