import os
import qrcode
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dinesh_secret_123"

UPLOAD_FOLDER = 'static/uploads'
QR_FOLDER = 'static/qr'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == "1234":  # change password here
            session['admin'] = True
            return redirect(url_for('index'))
    return '''
        <h2>Admin Login</h2>
        <form method="POST">
            <input type="password" name="password" placeholder="Enter password">
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    ...

@app.route('/logout')
def logout():
    ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('admin'):
        return redirect(url_for('login'))

    qr_image = None
    ...

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