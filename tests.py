import unittest
import coverage
import json
import os

covered = coverage.coverage(branch=True)
covered.start()

#Create a fake server essentially without disturbing the real one
from flask import Flask, request
from flask_socketio import SocketIO, send, emit
import numpy as np
import base64

from model import connect_to_db, db, example_data
import crud

app = Flask(__name__)
app.config['SECRET_KEY'] = "sososecret"
socketio = SocketIO(app)
disconnected = None

####Mock socketio functions####
@socketio.on('connect')
def connected():
    """Test conncted if any one connects to the website"""
    if request.args.get('fail'):
        return False
    send('Connected')
    print('Connected')


@socketio.on('disconnect')
def disconnected():
    """Test disconnection and make status as '/'"""
    global disconnected
    disconnected = '/'

@socketio.on('new image')
def on_custom_event(data):
    """Test emitting back and forth the image"""
    base64_image = data['imageData']

    # imagedata = base64.b64decode(base64_image+'====')
    filename = str(random.randint(100,200)) + str(random.randint(100,200)) + '.png'
    save_path = UPLOAD_FOLDER
    complete_path = os.path.join(save_path, filename)

    crud.add_image_path(complete_path)

    #Write base64 to create an image into /static/images
    with open(complete_path, 'wb') as new_image:
        new_image.write(imagedata)
        new_image.close()    

    emit('add image', {'imagePath':complete_path}, broadcast=True)

    if not data.get('noackargs'):
        return data


class TestSocketIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
    
    def setUp(cls):
        pass

    def tearDown(cls):
        pass

    def test_connect(self):
        """Testing on mock environment on connection"""
        print("--"*40)
        print("Test for connect")
        print("--"*40)
        print("client is:")
        client = socketio.test_client(app)
        print("\nclient2 is:")
        client2 = socketio.test_client(app)
        self.assertTrue(client.is_connected())
        self.assertTrue(client2.is_connected())

        #on connect server will send args: "connected"
        received = client.get_received()
        print("\nsocketio.on('connect') ->\n received=" + str(received)+"\n")
        self.assertEqual(len(received), 1)
        print("\nLength of received: 1 \n")
        self.assertNotEqual(client.eio_sid, client2.eio_sid)
        print("\nclient.eio_sid != client2.eio_sid")
        print(client.eio_sid +" != "+client2.eio_sid+"\n")
        self.assertEqual(received[0]['args'], 'Connected')
        print("\nreeived[0]['args] = 'Connected' \n")

        client.disconnect()
        print("\nclient is: disconnected")
        self.assertFalse(client.is_connected())
        self.assertTrue(client2.is_connected())
        print("\nclient2 is: still connected")
        client2.disconnect()
        self.assertFalse(client2.is_connected())
        print("\nclient2 is: disconnected \n")
        print("Test -> test_connect -> Passed")
        print("--"*40)

    def test_disconnect(self):
        """Testing on disconnection"""
        print("--"*40)
        print("Test for disconnect")
        print("--"*40)     
        global disconnected
        disconnected = None
        print("\nclient is:")
        client = socketio.test_client(app)
        client.disconnect()
        self.assertEqual(disconnected, '/')
        print("\nclient is: disconnected \n")
        print("Test -> socketio.on('disconnect') -> Passed")
        print("--"*40)          

    def test_emit_images(self):
        """Testing on image data is emitted"""
        #Test image. get it locally and use it to test
        # image = load()

        print("--"*40)
        print("Test for image data exchange")
        print("--"*40)  
        print("client is:")
        client = socketio.test_client(app)
        client.get_received()
        print("\nclient emitted: \n[{'name': 'new image', 'args': [{'image': 'imageDATAURL'}], 'namespace': '/'}]\n")
        
        with open("test_image.png",'rb') as test_image:
            test_base64 = base64.b64encode(test_image.read())
        
        client.emit('new image', {'imageData':test_base64})
        received = client.get_received()

        print("test worked here")

        self.assertEqual(type(received['image']),str)

        # print("\nsocketio.on('new image')-> \nreceived:" + str(received)+"\n")
        self.assertEqual(len(received), 1)
        print("Length of received = 1")
        self.assertEqual(len(received[0]['args']), 1)
        print("\nLength of received['args']= 1")
        self.assertEqual(received[0]['name'], 'add image')
        print("\nLength of received[0]['name']= 'add image' ")
        self.assertEqual(received[0]['args'][0]['image'], 'return_image_route')
        print("\nLength of received[0]['args'][0]['image']= 'return_image_route' \n")
        print("\nTest -> test_emit_images -> Passed")
        print("--"*40)      

covered.stop()

class FlaskTestDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Do before every test"""
        # Get the Flask test client
        app.config['TESTING'] = True
        self.client = app.test_client()


        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        #Example data to seed images paths into testDB
        example_data()
    
    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_Chat_list(self):
        """Test getting image routes from DB."""
        print("--"*40)
        print("Test for querying image routes")
        print("--"*40)

        images = crud.pull_latest_images()
        print("List from example data:")
        print(images)
        self.assertEqual(images[0].image_path, "./static/images/test.png")
        print("\nimage[0].image_path = './static/images/test.png'\n")
        print("Test -> test_Chat_list -> Passed")
        print("--"*40)

if __name__ == '__main__':
    os.system('dropdb testdb')
    os.system('createdb testdb')
    
    unittest.main()
