import os
from jinja2 import StrictUndefined
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import random
from model import db, Chat, connect_to_db
from crud import add_image_path, pull_latest_images
import datetime
import numpy as np
import base64

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'sosecret'
app.config['SESSION_TYPE'] = 'filesystem'

app.jinja_env.undefined = StrictUndefined

socketio = SocketIO(app)

@app.route('/')
def render_index():
    """homepage"""
    imgs = pull_latest_images()

    return render_template("index.html", imgs = imgs)

@socketio.on('connect')
def connected():
    """Print conncted if any one connects to the website"""
    print('Connected!')

@socketio.on('disconnect')
def diconnected():
    """Print disconnected if any one connects to the website"""
    print('Disconnected')


@socketio.on('new image')
def new_image_recieved (res):
    """Res from front end will be a dictionary of {imageData:'long data string"}
    Decode the string, then rename by a randomized number as PNG into static/images folder
    Save full file path into DB
    """
    base64_image = res['imageData'].partition(",")[2]

    imagedata = base64.b64decode(base64_image+'====')
    filename = str(random.randint(100,200)) + '.png'
    save_path = UPLOAD_FOLDER
    complete_path = os.path.join(save_path, filename)

    #Save file path into DB
    add_image_path(complete_path)

    #Write base64 to create an image into /static/images
    with open(complete_path, 'wb') as new_image:
        new_image.write(imagedata)
        new_image.close()
    emit('add image', res)



    #make someway so the JS function can open the pic or just route the picture as s new line like chat app
    #add file type restrictiono on img input element


if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()

    socketio.run(app, host='0.0.0.0', port='5001', debug=True)


