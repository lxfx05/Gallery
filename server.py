import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
from PIL import Image, ImageEnhance, ImageFilter

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return jsonify({'filename': filename})

@app.route('/api/edit', methods=['POST'])
def edit():
    data = request.get_json()
    filename = data['filename']
    values = data['value']
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Apri immagine
    img = Image.open(filepath)

    # Lettura valori di modifica
    brightness = float(values.get('brightness', 1))
    contrast = float(values.get('contrast', 1))
    saturation = float(values.get('saturation', 1))
    blur = float(values.get('blur', 0))
    rotate = int(values.get('rotate', 0))

    # Applica luminosità
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)

    # Applica contrasto
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)

    # Applica saturazione
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)

    # Applica blur
    if blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))

    # Applica rotazione
    if rotate != 0:
        img = img.rotate(rotate, expand=True)

    # Salva immagine temporanea
    temp_filename = str(uuid.uuid4()) + '.png'
    temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
    img.save(temp_filepath)

    return jsonify({'temp_filename': temp_filename})

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    download = request.args.get('download', 'false').lower() == 'true'
    if download:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
