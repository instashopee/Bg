from flask import Flask, render_template, request, redirect, url_for,send_file
from PIL import Image
from rembg import remove
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def remove_background(image_path):
    img = Image.open(image_path)

    # Convert image to RGB mode if it has an alpha channel
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    background_removed = remove(img)
    return background_removed

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        image_file = request.files['image']
        if image_file.filename == '':
            return redirect(request.url)
        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(image_path)
            background_removed = remove_background(image_path)
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'removed_{image_file.filename}')
            background_removed.save(output_path, 'PNG')  # Save as PNG instead of JPEG
            os.remove(image_path)
            return redirect(url_for('result', filename=f'removed_{image_file.filename}'))
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)
@app.route('/download/<filename>', methods=['POST'])
def download_image(filename):
    image_path = os.path.join(app.root_path, 'static', 'output', filename)
    return send_file(image_path, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)
