# AI Image Processing Agent

An AI-powered image processing application built with **FastAPI**, **BiRefNet**, and **InsightFace** that transforms ordinary portrait images into professional profile photos.

The application automatically detects the subject, removes the background using deep learning, intelligently crops the image, and allows users to apply professional backgrounds before exporting a high-quality image.

## Features

- AI Face Detection using InsightFace
- Automatic Background Removal using BiRefNet
- Smart Head & Shoulder Cropping
- Automatic Face Centering
- Background Selection Interface
- Zoom & Position Adjustment
- Export as High-Quality Image
- FastAPI Backend
- Responsive Web Interface
- REST API for easy integration with existing websites

## Tech Stack

- Python
- FastAPI
- InsightFace
- BiRefNet
- PyTorch
- Transformers
- OpenCV
- Pillow
- HTML
- CSS
- JavaScript

## Project Workflow

1. Upload an image.
2. Detect the primary face.
3. Calculate an intelligent crop around the subject.
4. Remove the background using BiRefNet.
5. Present professional background options.
6. Allow image positioning and scaling.
7. Export the final optimized image.

## API Endpoint

```
POST /process-image
```

Accepts an image and returns the processed transparent image.

## Future Improvements

- AI-powered automatic background selection
- Automatic subject positioning
- Smart image quality assessment
- Automatic image enhancement
- Multiple output formats
- Batch image processing

## Author

Adina Abrar
