#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import base64

class EnhancedAnalyzer:
    def __init__(self):
        # Load Haar cascade for face detection only
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
    def analyze_ocr(self, image_path):
        """
        Enhanced OCR analysis targeting black text on green ID card background
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Could not load image"}
        
        # Convert to RGB for PIL operations
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        
        try:
            # Multiple OCR attempts with black text targeting
            ocr_results = []
            
            # 1. Black text extraction
            black_text_pil = self._extract_black_text(pil_image)
            ocr_results.append(self._run_ocr_with_config(black_text_pil, 'eng+urd', '--oem 3 --psm 6'))
            
            # 2. Enhanced contrast for black text
            enhanced_black_pil = self._enhance_black_text_for_ocr(pil_image)
            ocr_results.append(self._run_ocr_with_config(enhanced_black_pil, 'eng+urd', '--oem 3 --psm 6'))
            
            # 3. Denoised black text
            denoised_black_pil = self._denoise_black_text(pil_image)
            ocr_results.append(self._run_ocr_with_config(denoised_black_pil, 'eng+urd', '--oem 3 --psm 6'))
            
            # 4. Sharpened black text
            sharpened_black_pil = self._sharpen_black_text(pil_image)
            ocr_results.append(self._run_ocr_with_config(sharpened_black_pil, 'eng+urd', '--oem 3 --psm 6'))
            
            # Find best OCR result
            best_result = max(ocr_results, key=lambda x: x['confidence'])
            
            # Create OCR visualization highlighting black text regions
            ocr_visualization = self._create_black_text_ocr_visualization(image, best_result)
            
            # Language detection
            language_info = self._detect_languages(best_result['text'])
            
            return {
                "score": round(best_result['confidence'], 2),
                "confidence": round(best_result['confidence'], 2),
                "text_found": best_result['text_found'],
                "text_count": best_result['text_count'],
                "detected_text": best_result['text'][:200] + "..." if len(best_result['text']) > 200 else best_result['text'],
                "language_info": language_info,
                "visualization": ocr_visualization,
                "details": f"Found {best_result['text_count']} black text elements with {best_result['confidence']:.1f}% avg confidence {language_info}",
                "all_attempts": [r['confidence'] for r in ocr_results]
            }
            
        except Exception as e:
            return {"error": f"OCR error: {str(e)}"}
    
    def analyze_human_detection(self, image_path):
        """
        Face detection with visualization
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Could not load image"}
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Face detection only
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(20, 20))
        
        # Calculate confidence based on face detection
        confidence = self._calculate_face_confidence(faces, image.shape)
        
        # Create visualization
        vis_image = image.copy()
        
        # Draw bounding boxes for detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(vis_image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green for faces
            cv2.putText(vis_image, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', vis_image)
        vis_b64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        
        return {
            "human_detected": len(faces) > 0,
            "confidence": round(confidence, 2),
            "face_count": len(faces),
            "total_detections": len(faces),
            "visualization": vis_b64,
            "details": self._generate_face_detection_details(faces, confidence)
        }
    
    def analyze_blur_detection(self, image_path):
        """
        Enhanced blur detection with blur map visualization
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Could not load image"}
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Multiple blur detection methods
        methods = {
            "laplacian": self._laplacian_blur_detection(gray),
            "sobel": self._sobel_blur_detection(gray),
            "fft": self._fft_blur_detection(gray),
            "gradient": self._gradient_blur_detection(gray),
            "edge_density": self._edge_density_blur_detection(gray)
        }
        
        # Calculate weighted average
        weights = {"laplacian": 0.3, "sobel": 0.25, "fft": 0.2, "gradient": 0.15, "edge_density": 0.1}
        weighted_score = sum(methods[method] * weights[method] for method in methods)
        
        # Create blur map visualization
        blur_map = self._create_blur_map(gray)
        
        return {
            "score": round(weighted_score, 2),
            "methods": methods,
            "blur_map": blur_map,
            "details": f"Multi-method blur analysis: Laplacian={methods['laplacian']:.1f}, Sobel={methods['sobel']:.1f}, FFT={methods['fft']:.1f}"
        }
    
    def _run_ocr_with_config(self, pil_image, lang, config):
        """Run OCR with specific configuration"""
        ocr_data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT, config=config, lang=lang)
        
        if not ocr_data['text'] or all(text.strip() == '' for text in ocr_data['text']):
            return {"confidence": 0, "text_found": False, "text_count": 0, "text": "", "boxes": []}
        
        confidences = [int(conf) for conf, text in zip(ocr_data['conf'], ocr_data['text']) 
                      if int(conf) > 0 and text.strip()]
        
        if not confidences:
            return {"confidence": 0, "text_found": False, "text_count": 0, "text": "", "boxes": []}
        
        avg_confidence = np.mean(confidences)
        text_count = len(confidences)
        detected_text = ' '.join([text.strip() for conf, text in zip(ocr_data['conf'], ocr_data['text']) 
                                 if int(conf) > 0 and text.strip()])
        
        # Extract bounding boxes for visualization
        boxes = []
        for i, (conf, text) in enumerate(zip(ocr_data['conf'], ocr_data['text'])):
            if int(conf) > 0 and text.strip():
                x = ocr_data['left'][i]
                y = ocr_data['top'][i]
                w = ocr_data['width'][i]
                h = ocr_data['height'][i]
                confidence = int(conf)
                boxes.append((x, y, w, h, confidence, text.strip()))
        
        return {
            "confidence": avg_confidence,
            "text_found": True,
            "text_count": text_count,
            "text": detected_text,
            "boxes": boxes
        }
    
    def _extract_black_text(self, pil_image):
        """Extract black text regions from green ID card background"""
        # Convert to numpy array
        img_array = np.array(pil_image)
        
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Define black color range (low saturation, low value)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])  # Low value (brightness) for black
        
        # Create mask for black regions
        black_mask = cv2.inRange(hsv, lower_black, upper_black)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((2, 2), np.uint8)
        black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel)
        black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)
        
        # Create white background with black text
        result = np.ones_like(img_array) * 255  # White background
        result[black_mask == 255] = [0, 0, 0]   # Black text
        
        return Image.fromarray(result)
    
    def _enhance_black_text_for_ocr(self, pil_image):
        """Enhance black text specifically for OCR on ID cards"""
        # Extract black text first
        black_text_pil = self._extract_black_text(pil_image)
        
        # Convert to grayscale
        gray = black_text_pil.convert('L')
        
        # Apply adaptive threshold to make text more prominent
        gray_array = np.array(gray)
        adaptive_thresh = cv2.adaptiveThreshold(gray_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Invert to get black text on white background
        inverted = cv2.bitwise_not(adaptive_thresh)
        
        return Image.fromarray(inverted)
    
    def _denoise_black_text(self, pil_image):
        """Apply denoising specifically for black text"""
        # Extract black text first
        black_text_pil = self._extract_black_text(pil_image)
        
        # Convert to numpy array
        img_array = np.array(black_text_pil)
        
        # Apply bilateral filter for edge-preserving denoising
        denoised = cv2.bilateralFilter(img_array, 9, 75, 75)
        
        # Apply morphological operations to clean up text
        kernel = np.ones((1, 1), np.uint8)
        denoised = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
        
        return Image.fromarray(denoised)
    
    def _sharpen_black_text(self, pil_image):
        """Apply sharpening specifically for black text"""
        # Extract black text first
        black_text_pil = self._extract_black_text(pil_image)
        
        # Apply unsharp mask
        sharpened = black_text_pil.filter(ImageFilter.UnsharpMask(radius=1, percent=200, threshold=2))
        
        return sharpened
    
    def _create_black_text_ocr_visualization(self, image, ocr_result):
        """Create OCR visualization highlighting black text regions"""
        vis_image = image.copy()
        
        if not ocr_result['text_found']:
            # If no text found, show black text extraction
            black_text_pil = self._extract_black_text(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
            black_text_array = np.array(black_text_pil)
            black_text_bgr = cv2.cvtColor(black_text_array, cv2.COLOR_RGB2BGR)
            
            # Add overlay text
            cv2.putText(black_text_bgr, "No black text detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Convert to base64
            _, buffer = cv2.imencode('.jpg', black_text_bgr)
            return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        else:
            # Draw bounding boxes for detected black text
            for box in ocr_result['boxes']:
                x, y, w, h, confidence, text = box
                
                # Color based on confidence
                if confidence >= 80:
                    color = (0, 255, 0)  # Green for high confidence
                elif confidence >= 60:
                    color = (0, 255, 255)  # Yellow for medium confidence
                else:
                    color = (0, 0, 255)  # Red for low confidence
                
                # Draw rectangle
                cv2.rectangle(vis_image, (x, y), (x + w, y + h), color, 2)
                
                # Add confidence label
                label = f"{confidence}%"
                cv2.putText(vis_image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Add overlay indicating black text focus
            cv2.putText(vis_image, "Black Text Detection", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(vis_image, "Green ID Card Background", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', vis_image)
        return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
    
    def _detect_languages(self, text):
        """Enhanced language detection"""
        urdu_chars = sum(1 for char in text if '\u0600' <= char <= '\u06ff' or '\u0750' <= char <= '\u077f')
        english_chars = sum(1 for char in text if char.isascii() and char.isalpha())
        numeric_chars = sum(1 for char in text if char.isdigit())
        
        languages = []
        if urdu_chars > 0:
            languages.append("Urdu")
        if english_chars > 0:
            languages.append("English")
        if numeric_chars > 0:
            languages.append("Numbers")
        
        if len(languages) > 1:
            return f"({', '.join(languages)})"
        elif len(languages) == 1:
            return f"({languages[0]})"
        else:
            return "(Unknown)"
    
    def _laplacian_blur_detection(self, gray):
        """Laplacian variance blur detection"""
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return min(100, (laplacian_var / 10))
    
    def _sobel_blur_detection(self, gray):
        """Sobel edge-based blur detection"""
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        return min(100, np.mean(sobel_magnitude) / 2)
    
    def _fft_blur_detection(self, gray):
        """FFT-based blur detection"""
        # Apply FFT
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.log(np.abs(f_shift) + 1)
        
        # Calculate high-frequency content
        rows, cols = gray.shape
        crow, ccol = rows//2, cols//2
        high_freq = magnitude_spectrum[crow-30:crow+30, ccol-30:ccol+30]
        
        return min(100, np.mean(high_freq) * 2)
    
    def _gradient_blur_detection(self, gray):
        """Gradient-based blur detection"""
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        return min(100, np.mean(gradient_magnitude) / 3)
    
    def _edge_density_blur_detection(self, gray):
        """Edge density-based blur detection"""
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        return min(100, edge_density * 1000)
    
    def _create_blur_map(self, gray):
        """Create detailed blur map visualization"""
        # Create local blur map using sliding window
        height, width = gray.shape
        blur_map = np.zeros((height, width))
        window_size = 15
        
        for i in range(0, height - window_size, window_size//2):
            for j in range(0, width - window_size, window_size//2):
                window = gray[i:i+window_size, j:j+window_size]
                laplacian_var = cv2.Laplacian(window, cv2.CV_64F).var()
                blur_value = min(255, max(0, 255 - (laplacian_var / 2)))
                blur_map[i:i+window_size, j:j+window_size] = blur_value
        
        # Normalize and convert to uint8
        blur_map = np.uint8(blur_map)
        
        # Apply colormap for better visualization
        blur_map_colored = cv2.applyColorMap(blur_map, cv2.COLORMAP_JET)
        
        # Convert to base64
        _, buffer = cv2.imencode('.jpg', blur_map_colored)
        return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
    
    def _calculate_face_confidence(self, faces, image_shape):
        """Calculate confidence based on face detection"""
        total_area = image_shape[0] * image_shape[1]
        confidence = 0
        
        for (x, y, w, h) in faces:
            face_area = w * h
            area_ratio = face_area / total_area
            confidence += min(100, area_ratio * 100)
        
        return min(100, confidence)
    
    def _generate_face_detection_details(self, faces, confidence):
        """Generate detailed face detection description"""
        face_count = len(faces)
        
        if face_count > 0:
            return f"Detected {face_count} face(s). Human presence confirmed ({confidence:.1f}%)."
        else:
            return f"No human features detected in the image ({confidence:.1f}% confidence)." 