from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
socketio = SocketIO(app)

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            socketio.emit('reload')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Set up file watching
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    # Run the app
    socketio.run(app, debug=True)
