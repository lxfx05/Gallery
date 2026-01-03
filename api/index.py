import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
from PIL import Image, ImageEnhance, ImageFilter

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# Cartella temporanea per Vercel
UPLOAD_FOLDER = '/tmp'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return jsonify({'filename': filename})

@app.route('/api/edit', methods=['POST'])
def edit():
    data = request.get_json()
    filename = data.get('filename')
    values = data.get('value', {})
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    img = Image.open(filepath).convert("RGB")

    # Applicazione filtri
    img = ImageEnhance.Brightness(img).enhance(float(values.get('brightness', 1)))
    img = ImageEnhance.Contrast(img).enhance(float(values.get('contrast', 1)))
    img = ImageEnhance.Color(img).enhance(float(values.get('saturation', 1)))

    blur = float(values.get('blur', 0))
    if blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    
    rotate = int(values.get('rotate', 0))
    if rotate != 0:
        img = img.rotate(-rotate, expand=True) # Segno meno per rotazione oraria naturale

    temp_filename = f"edit_{uuid.uuid4()}.png"
    temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
    img.save(temp_filepath, "PNG")

    return jsonify({'temp_filename': temp_filename})

@app.route('/get-img/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
            
