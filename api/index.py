import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
from PIL import Image, ImageEnhance, ImageFilter

# Configuriamo Flask per cercare i file fuori dalla cartella api/
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# Su Vercel l'unica cartella con permessi di scrittura è /tmp
UPLOAD_FOLDER = '/tmp'

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

    img = Image.open(filepath)

    brightness = float(values.get('brightness', 1))
    contrast = float(values.get('contrast', 1))
    saturation = float(values.get('saturation', 1))
    blur = float(values.get('blur', 0))
    rotate = int(values.get('rotate', 0))

    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)

    if blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    if rotate != 0:
        img = img.rotate(rotate, expand=True)

    temp_filename = str(uuid.uuid4()) + '.png'
    temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
    img.save(temp_filepath)

    return jsonify({'temp_filename': temp_filename})

# Rotta necessaria per servire le immagini dalla cartella /tmp di Vercel
@app.route('/get-img/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
    
