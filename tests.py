import unittest
import coverage
import json

covered = coverage.coverage(branch=True)
covered.start()

#Create a fake server essentially without disturbing the real one
from flask import Flask, session, request, json as flask_json
from flask_socketio import SocketIO, send, emit, Namespace

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
    emit('add image', {'image':'somelongdata'})
    if not data.get('noackargs'):
        return data

@socketio.on('my custom event')
def on_custom_event(data):
    emit('my custom response', data)
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
        print("--"*20)
        print("Test for connect")
        print("--"*20)
        print("client is:")
        client = socketio.test_client(app)
        print("client2 is:")
        client2 = socketio.test_client(app)
        self.assertTrue(client.is_connected())
        self.assertTrue(client2.is_connected())

        #on connect server will send args: "connected"
        received = client.get_received()
        print("test_connect () -> \n" + str(received)+"\n")
        self.assertEqual(len(received), 1)
        print("Length of received: 1 \n")
        self.assertNotEqual(client.eio_sid, client2.eio_sid)
        print("client.eio_sid != client2.eio_sid")
        print(client.eio_sid +" != "+client2.eio_sid+"\n")
        self.assertEqual(received[0]['args'], 'Connected')
        print("reeived[0]['args] = 'Connected' \n")

        client.disconnect()
        print("client is: disconnected")
        self.assertFalse(client.is_connected())
        self.assertTrue(client2.is_connected())
        print("client2 is: still connected")
        client2.disconnect()
        self.assertFalse(client2.is_connected())
        print("client2 is: disconnected \n")
        print("test_connect -> Passed")
        print("--"*20)

    def test_disconnect(self):
        """Testing on disconnection"""
        print("--"*20)
        print("Test for disconnect")
        print("--"*20)     
        global disconnected
        disconnected = None
        print("client is:")
        client = socketio.test_client(app)
        client.disconnect()
        self.assertEqual(disconnected, '/')
        print("client is: disconnected \n")
        print("test_disconnect -> Passed")
        print("--"*20)          

    def test_emit_images(self):
        """Testing on image data is emitted"""
        print("--"*20)
        print("Test for image data exchange")
        print("--"*20)  
        print("client is:")
        client = socketio.test_client(app)
        client.get_received()
        client.emit('new image', {'image':'somelongdata'})
        received = client.get_received()
        print("\n test_emit_images () -> \n" + str(received))
        self.assertEqual(len(received), 1)
        print("Length of received = 1")
        self.assertEqual(len(received[0]['args']), 1)
        print("Length of received['args']= 1")
        self.assertEqual(received[0]['name'], 'add image')
        print("Length of received[0]['name']= 'add image' ")
        self.assertEqual(received[0]['args'][0]['image'], 'somelongdata')
        print("Length of received[0]['args'][0]['image']= 'somelongdata' \n")
        print("Test -> test_emit_images -> Passed")
        print("--"*20)      
 



if __name__ == '__main__':
    unittest.main()
