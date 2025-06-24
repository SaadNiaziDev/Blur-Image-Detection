import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import cv2
import base64
from enhanced_analysis import EnhancedAnalyzer

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
    return render_template('index.html', title="Advanced Image Detection & Analysis Tool")

@app.route('/ocr_analysis', methods=['POST'])
def ocr_analysis():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Initialize enhanced analyzer
            analyzer = EnhancedAnalyzer()
            
            # Run OCR analysis
            results = analyzer.analyze_ocr(filepath)
            
            if "error" in results:
                return jsonify({'error': results["error"]}), 400
            
            # Load original image for display
            image = cv2.imread(filepath)
            if image is None:
                return jsonify({'error': 'Failed to read image'}), 400
            
            # Convert image to base64 for display
            original_b64 = encode_image_to_base64(image)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'original_image': original_b64,
                'results': results
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/human_detection', methods=['POST'])
def human_detection():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Initialize enhanced analyzer
            analyzer = EnhancedAnalyzer()
            
            # Run human detection analysis
            results = analyzer.analyze_human_detection(filepath)
            
            if "error" in results:
                return jsonify({'error': results["error"]}), 400
            
            # Load original image for display
            image = cv2.imread(filepath)
            if image is None:
                return jsonify({'error': 'Failed to read image'}), 400
            
            # Convert original image to base64 for display
            original_b64 = encode_image_to_base64(image)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'original_image': original_b64,
                'results': results
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/blur_detection', methods=['POST'])
def blur_detection():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Initialize enhanced analyzer
            analyzer = EnhancedAnalyzer()
            
            # Run blur detection analysis
            results = analyzer.analyze_blur_detection(filepath)
            
            if "error" in results:
                return jsonify({'error': results["error"]}), 400
            
            # Load original image for display
            image = cv2.imread(filepath)
            if image is None:
                return jsonify({'error': 'Failed to read image'}), 400
            
            # Convert image to base64 for display
            original_b64 = encode_image_to_base64(image)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'original_image': original_b64,
                'results': results
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Enhanced Image Analysis Tool is running'})

if __name__ == '__main__':
    print("Starting Enhanced Image Analysis Tool...")
    print("Web UI will be available at: http://localhost:3000")
    print("Health check: http://localhost:3000/health")
    app.run(debug=True, host='0.0.0.0', port=3000, threaded=True) 