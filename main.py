from glob import glob
from io import BytesIO
import os
from zipfile import ZipFile
from scripts.imageProcessing import capture_frame, process_image
from flask import Flask, render_template, Response, send_file, send_from_directory

app = Flask(__name__,template_folder='scripts/templates')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(process_image(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/downloads')
def save():
    target = 'downloads/'
    stream = BytesIO()
    with ZipFile(stream,'w') as zf:
        for file in glob(os.path.join(target, '*.png')):
            zf.write(file, os.path.basename(file))
    stream.seek(0)
    return send_file(stream, as_attachment=True, download_name='frame.zip')


@app.route('/capture')
def capture():
    return Response(capture_frame())

def main():
    app.run(host='0.0.0.0',debug=True)

if __name__ == "__main__":
    main()