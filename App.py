import json
from video_process import VideoCamera

from flask import Flask, request, Response, jsonify

app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        global f, url
        url = None
        f = request.files['video']
        f.save('./videos/' + f.filename)
        return json.dumps(True)


def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            return "video or ipcam not connected"
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    name = request.args.get('name')
    video_process = VideoCamera(video='./videos/' + str(name))
    return Response(gen(video_process),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
