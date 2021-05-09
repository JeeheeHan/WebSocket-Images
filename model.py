"""Models for chat with just images app"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri = 'postgresql:///imagepath', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = False
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connect to DB!')

class Chat(db.Model):
    """Chat table with images and username"""
    __tablename__ = "chat"

    id = db.Column(db.Integer,
                    autoincrement = True,
                    primary_key=True)
    # username = db.Column(db.String(30), unique=True)
    image_path = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'<Chat id:{self.id} image_path:{self.image_path}>'

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    Chat.query.delete()

    # Add sample fake images
    ab = Chat(image_path="./static/images/test.png")
    cd = Chat(image_path="./static/images/test2.png")
    ef = Chat(image_path="./static/images/test3.png")


    db.session.add_all([ab, cd, ef])
    db.session.commit()

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all()