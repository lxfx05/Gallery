import os
import uuid
import base64
from io import BytesIO
from flask import Flask, request, jsonify, render_template
from PIL import Image, ImageEnhance, ImageFilter

app = Flask(__name__, template_folder='../templates', static_folder='../static')
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
    filename = data.get('filename')
    v = data.get('value', {})
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img = Image.open(filepath).convert("RGB")

    # Elaborazione veloce
    img = ImageEnhance.Brightness(img).enhance(float(v.get('brightness', 1)))
    img = ImageEnhance.Contrast(img).enhance(float(v.get('contrast', 1)))
    img = ImageEnhance.Color(img).enhance(float(v.get('saturation', 1)))
    
    blur = float(v.get('blur', 0))
    if blur > 0: img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    
    rotate = int(v.get('rotate', 0))
    if rotate != 0: img = img.rotate(-rotate, expand=True)

    # CONVERSIONE IMMEDIATA IN BASE64 (Senza salvare file)
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=85) # JPEG è più leggero di PNG per l'anteprima
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({'image': f"data:image/jpeg;base64,{img_str}"})
            
