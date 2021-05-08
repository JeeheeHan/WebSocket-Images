import os
from jinja2 import StrictUndefined
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import random
from model import db, Chat, connect_to_db
from crud import create_image_path
import datetime


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
    return render_template("index.html")

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
    emit('add image', res)
    #TODO: add crud to save the base64 as a pic and save the route into DB 
    #make someway so the JS function can open the pic or just route the picture as s new line like chat app
    #add file type restrictiono on img input element


if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()

    socketio.run(app, host='0.0.0.0', port='5001', debug=True)


