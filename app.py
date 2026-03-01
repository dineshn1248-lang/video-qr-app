import os
import qrcode
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
QR_FOLDER = 'static/qr'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None

    if request.method == 'POST':
        video = request.files['video']

        if video:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
            video.save(video_path)

            video_url = request.host_url + 'static/uploads/' + video.filename

            qr = qrcode.make(video_url)
            qr_path = os.path.join(QR_FOLDER, video.filename + ".png")
            qr.save(qr_path)

            qr_image = 'qr/' + video.filename + ".png"

    return render_template('index.html', qr_image=qr_image)

if __name__ == '__main__':
    app.run(debug=True)