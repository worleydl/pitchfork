from flask import Flask
from flask_socketio import SocketIO, emit, join_room
import eventlet
import redis
from threading import Thread

eventlet.monkey_patch()
app = Flask(__name__)

socketio = SocketIO(app)

def redis_thread():
	r = redis.Redis()
	pubsub = r.pubsub()
	pubsub.subscribe('post')
	
	for evt in pubsub.listen():
		socketio.emit('post', {}, room=int(evt['data']))

@socketio.on('join')
def join(message):
	join_room(int(message))

if __name__ == '__main__':
	# Fire up redis thread
	thread = Thread(target=redis_thread)	
	thread.daemon = True
	thread.start()

	socketio.run(app, host='0.0.0.0', debug=True)
