# Blur Detection Tool

A comprehensive blur detection solution that analyzes images to determine if they are blurry or sharp. This project provides both a command-line interface and a modern web UI with camera capture capabilities.

## 🎯 What It Does

This tool uses the **Laplacian variance method** to detect blur in images. It calculates the total variance of the Laplacian of an image, which provides a quick and accurate method for scoring how blurry an image is. Higher scores indicate sharper images.

### Key Features

- **🔍 Blur Detection**: Analyze single images or batches for blur detection
- **📊 Visual Results**: See blur maps showing which areas are blurry
- **📷 Camera Capture**: Take photos directly from your webcam for instant analysis
- **🌐 Web Interface**: Modern, responsive web UI with drag & drop support
- **💻 Command Line**: Fast batch processing for multiple images
- **📱 Mobile Friendly**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Option 1: Web UI (Recommended for most users)

```bash
# Clone the repository
git clone <repository-url>
cd BlurDetection2

# Start the web interface
./start_web_ui.sh
```

Then open your browser to: **http://localhost:5001**

### Option 2: Command Line

```bash
# Install dependencies
pip install -r requirements.txt

# Analyze a single image
python process.py -i your_image.jpg

# Analyze multiple images
python process.py -i image1.jpg image2.png directory_of_images/

# Save results to JSON
python process.py -i images/ -s results.json
```

## 📋 Requirements

- Python 3.6+
- OpenCV
- NumPy
- Flask (for web UI)

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🎨 Web Interface Features

### Three Ways to Analyze Images

#### 1. **Single Image Upload**

- Drag & drop or browse for a single image
- See side-by-side comparison: original vs blur map
- Get detailed blur score and classification

#### 2. **Batch Upload**

- Upload multiple images at once
- Get results for all images in a list format
- Quick overview of which images are blurry/sharp

#### 3. **📷 Camera Capture** _(NEW!)_

- **Live Camera Preview**: Real-time video feed from your webcam
- **Multiple Camera Support**: Choose between available cameras
- **Capture & Retake**: Take photos until you're satisfied
- **Instant Analysis**: Process captured images immediately

### Web UI Controls

- **Adjustable Threshold**: Customize blur detection sensitivity (default: 100.0)
- **Drag & Drop**: Easy file upload with visual feedback
- **Real-time Processing**: See results instantly
- **Responsive Design**: Works on all devices

## 💻 Command Line Usage

### Basic Usage

```bash
# Analyze a single image
python process.py -i image.jpg

# Analyze a directory of images
python process.py -i images/

# Analyze multiple sources
python process.py -i image1.jpg images/ image2.png
```

### Advanced Options

```bash
# Save results to JSON file
python process.py -i images/ -s results.json

# Adjust blur threshold (default: 100.0)
python process.py -i images/ -t 150.0

# Display images during processing
python process.py -i images/ -d

# Allow variable image sizes (not recommended for consistent scoring)
python process.py -i images/ -f

# Verbose logging
python process.py -i images/ -v
```

### Command Line Options

| Option                | Description                   | Default  |
| --------------------- | ----------------------------- | -------- |
| `-i, --images`        | Input images or directories   | Required |
| `-s, --save-path`     | Save results to JSON file     | None     |
| `-t, --threshold`     | Blur threshold value          | 100.0    |
| `-f, --variable-size` | Don't normalize image size    | False    |
| `-d, --display`       | Show images during processing | False    |
| `-v, --verbose`       | Enable debug logging          | False    |

## 📊 Understanding Results

### Blur Score

- **Higher values** = Sharper images
- **Lower values** = Blurrier images
- **Threshold comparison**: Images below threshold are classified as "blurry"

### Example Output

```json
{
	"images": ["/path/to/images/"],
	"threshold": 100.0,
	"fix_size": true,
	"results": [
		{
			"input_path": "/path/to/images/sharp_image.jpg",
			"score": 6984.81,
			"blurry": false
		},
		{
			"input_path": "/path/to/images/blurry_image.jpg",
			"score": 45.23,
			"blurry": true
		}
	]
}
```

### Web UI Results

- **Visual blur map**: Shows which areas are blurry (darker = more blurry)
- **Side-by-side comparison**: Original image vs blur detection map
- **Status indicators**: Clear "SHARP" or "BLURRY" labels
- **Score display**: Numerical blur score with threshold reference

## 🔧 Technical Details

### Algorithm

Based on the blog post [Blur Detection With OpenCV](https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/) by Adrian Rosebrock.

**How it works:**

1. Convert image to grayscale
2. Apply Laplacian operator
3. Calculate variance of the Laplacian
4. Compare variance to threshold
5. Generate blur map for visualization

### Image Processing

- **Size Normalization**: Images are resized to HD resolution for consistent scoring
- **Format Support**: PNG, JPG, JPEG, GIF, BMP
- **File Size Limit**: 16MB per image (web UI)
- **Quality**: High-quality processing with OpenCV

### Web UI Architecture

- **Backend**: Flask web server
- **Frontend**: Vanilla JavaScript (no external dependencies)
- **Camera**: WebRTC MediaDevices API
- **Image Capture**: Canvas-based high-quality capture
- **Security**: Secure file handling, automatic cleanup

## 🌐 Browser Compatibility

### Web UI

- **Chrome 53+**: Full support
- **Firefox 36+**: Full support
- **Safari 11+**: Full support
- **Edge 12+**: Full support

### Camera Features

- **Desktop**: Full camera support
- **Mobile**: Requires HTTPS for camera access
- **Permissions**: Explicit user consent required

## 📁 Project Structure

```
BlurDetection2/
├── app.py                    # Flask web application
├── process.py                # Command-line interface
├── requirements.txt          # Python dependencies
├── start_web_ui.sh          # Web UI startup script
├── templates/
│   └── index.html           # Web interface
├── blur_detection/
│   ├── __init__.py          # Module exports
│   └── detection.py         # Core blur detection algorithm
├── venv/                    # Virtual environment (auto-created)
├── uploads/                 # Temporary upload directory (auto-created)
├── results/                 # Results directory (auto-created)
├── docs/                    # Documentation and demos
└── README.md               # This file
```

## 🚀 Getting Started

### For Web UI Users

1. **Start the application**:

   ```bash
   ./start_web_ui.sh
   ```

2. **Open your browser** to `http://localhost:5001`

3. **Choose your method**:

   - **Upload**: Drag & drop images or browse files
   - **Camera**: Click "📷 Camera" tab and capture photos
   - **Batch**: Upload multiple images at once

4. **Adjust settings**: Modify blur threshold if needed

5. **View results**: See blur scores, classifications, and visual maps

### For Command Line Users

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Analyze images**:

   ```bash
   # Single image
   python process.py -i your_image.jpg

   # Multiple images
   python process.py -i images/ -s results.json
   ```

3. **Review results**: Check console output or JSON file

## 🔒 Privacy & Security

- **Camera Access**: Requires explicit user permission
- **Local Processing**: All images processed locally
- **No Storage**: Images not permanently stored
- **Secure**: Standard web security practices
- **HTTPS Ready**: Works with HTTPS for mobile camera access

## 🛠️ Troubleshooting

### Web UI Issues

**Camera not starting:**

- Grant camera permissions to the website
- Check if camera is being used by another application
- Try refreshing the page

**Images not uploading:**

- Check file format (PNG, JPG, JPEG, GIF, BMP)
- Ensure file size is under 16MB
- Try a different browser

**Server not starting:**

- Check if port 5001 is available
- Ensure Python 3.6+ is installed
- Try running `./start_web_ui.sh` again

### Command Line Issues

**Import errors:**

- Install dependencies: `pip install -r requirements.txt`
- Use virtual environment: `python3 -m venv venv && source venv/bin/activate`

**Image reading errors:**

- Check file format and path
- Ensure images are not corrupted
- Try with `-v` flag for verbose output

### General Issues

**Performance:**

- Large images are automatically resized for consistent scoring
- Use `-f` flag to disable size normalization (not recommended)
- Batch processing is optimized for multiple images

**Accuracy:**

- Higher threshold = more strict blur detection
- Results depend on image content and quality
- Use visual blur maps to understand results better

## 📈 Use Cases

- **Photography**: Check if photos are in focus before editing
- **Quality Control**: Ensure product images are sharp
- **Document Scanning**: Verify scanned documents are readable
- **Real-time Analysis**: Use camera capture for immediate feedback
- **Batch Processing**: Analyze large collections of images

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is based on the work by Adrian Rosebrock and is licensed under the same terms as the original implementation.

## 🙏 Acknowledgments

- **Adrian Rosebrock**: Original blur detection algorithm and blog post
- **OpenCV**: Computer vision library
- **Flask**: Web framework for the UI
- **WebRTC**: Camera access technology

---

**Ready to detect blur?** Start with the web UI for an interactive experience, or use the command line for batch processing!
