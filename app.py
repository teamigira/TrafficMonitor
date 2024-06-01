from flask import Flask, render_template, request, Response
# from Test2 import VideoStream

app = Flask(__name__)
# video_stream = VideoStream()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return render_template('video.html')


@app.route('/process', methods=['POST'])
def process():
    return render_template('result.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
