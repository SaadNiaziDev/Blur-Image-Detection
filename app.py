import os
import json
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import cv2
from blur_detection import estimate_blur, fix_image_size, pretty_blur_map
import base64
import numpy as np

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Ensure upload and results directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(image):
    """Convert OpenCV image to base64 string for display"""
    _, buffer = cv2.imencode('.jpg', image)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Get threshold from form
        threshold = float(request.form.get('threshold', 100.0))
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process the image
            image = cv2.imread(filepath)
            if image is None:
                return jsonify({'error': 'Failed to read image'}), 400
            
            # Fix image size for consistent scoring
            image = fix_image_size(image)
            
            # Run blur detection
            blur_map, score, blurry = estimate_blur(image, threshold=threshold)
            
            # Create pretty blur map for visualization
            pretty_map = pretty_blur_map(blur_map)
            
            # Convert images to base64 for display
            original_b64 = encode_image_to_base64(image)
            blur_map_b64 = encode_image_to_base64(pretty_map)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'score': float(score),
                'blurry': blurry,
                'threshold': threshold,
                'original_image': original_b64,
                'blur_map': blur_map_b64
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/batch_upload', methods=['POST'])
def batch_upload():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files[]')
    threshold = float(request.form.get('threshold', 100.0))
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Process the image
                image = cv2.imread(filepath)
                if image is not None:
                    image = fix_image_size(image)
                    blur_map, score, blurry = estimate_blur(image, threshold=threshold)
                    
                    results.append({
                        'filename': filename,
                        'score': float(score),
                        'blurry': blurry
                    })
                
                # Clean up
                os.remove(filepath)
                
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                results.append({
                    'filename': filename,
                    'error': str(e)
                })
    
    return jsonify({
        'success': True,
        'results': results,
        'threshold': threshold
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Blur Detection Web UI is running'})

if __name__ == '__main__':
    print("Starting Blur Detection Web UI...")
    print("Web UI will be available at: http://localhost:5001")
    print("Health check: http://localhost:5001/health")
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True) 