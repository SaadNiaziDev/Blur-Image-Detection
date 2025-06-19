# Blur Detection Web UI

A modern web interface for the blur detection tool that allows you to upload images or capture from camera to get instant blur analysis results.

## Features

- **Single Image Upload**: Upload one image at a time for detailed analysis
- **Batch Upload**: Process multiple images simultaneously
- **📷 Camera Capture**: Take photos directly from your webcam/camera
- **Drag & Drop**: Easy file upload with drag and drop support
- **Real-time Results**: See blur scores and visual blur maps instantly
- **Adjustable Threshold**: Customize the blur detection sensitivity
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Using the startup script (Recommended)

```bash
./start_web_ui.sh
```

### Option 2: Manual startup

1. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Start the web server:

```bash
python app.py
```

3. Open your web browser and go to:

```
http://localhost:5001
```

4. Upload images or capture from camera and view results!

## How to Use

### Single Image Analysis

1. Click on the "Single Image" tab
2. Drag and drop an image or click "Choose File"
3. Adjust the blur threshold if needed (default: 100.0)
4. Click "Process Images"
5. View the results showing:
   - Original image
   - Blur detection map
   - Blur score and classification (Sharp/Blurry)

### Batch Analysis

1. Click on the "Batch Upload" tab
2. Select multiple images
3. Adjust the blur threshold if needed
4. Click "Process Images"
5. View results for all images in a list format

### 📷 Camera Capture

1. Click on the "📷 Camera" tab
2. Select your preferred camera from the dropdown (if multiple cameras available)
3. Click "📷 Start Camera" to begin
4. Allow camera permissions when prompted by your browser
5. Click "📸 Capture Photo" to take a picture
6. Review the captured image and either:
   - Click "🔄 Retake" to capture a new photo
   - Click "🔍 Analyze Photo" to process the image
7. View the blur detection results

**Camera Features:**

- **Multiple Camera Support**: Choose between available cameras
- **Live Preview**: See what you're capturing in real-time
- **Capture & Retake**: Take multiple photos until you're satisfied
- **Instant Analysis**: Get blur detection results immediately after capture

## Understanding Results

- **Blur Score**: Higher values indicate sharper images
- **Threshold**: Images with scores below the threshold are classified as blurry
- **Blur Map**: Visual representation showing which areas of the image are blurry (darker areas = more blurry)

## Technical Details

- Built with Flask (Python web framework)
- Uses the existing blur detection algorithm from the original project
- Supports common image formats: PNG, JPG, JPEG, GIF, BMP
- Maximum file size: 16MB per image
- Images are automatically resized to HD resolution for consistent scoring
- Camera capture uses WebRTC MediaDevices API for browser compatibility

## Browser Compatibility

The camera functionality works in modern browsers that support the MediaDevices API:

- Chrome 53+
- Firefox 36+
- Safari 11+
- Edge 12+

## Troubleshooting

### General Issues

- If images fail to upload, check the file format and size
- Ensure all dependencies are installed correctly
- Check the console for any error messages
- If port 5001 is in use, you can modify the port in `app.py`

### Camera Issues

- **Camera not starting**: Make sure you've granted camera permissions to the website
- **No camera detected**: Check if your camera is connected and not being used by another application
- **Permission denied**: Click the camera icon in your browser's address bar to grant permissions
- **Multiple cameras**: Use the camera dropdown to select the correct camera
- **Mobile devices**: Ensure you're using HTTPS if accessing from a mobile device (camera requires secure context)

## Privacy & Security

- Camera access requires explicit user permission
- Captured images are processed locally and not stored permanently
- Images are automatically cleaned up after processing
- No camera data is transmitted to external servers
