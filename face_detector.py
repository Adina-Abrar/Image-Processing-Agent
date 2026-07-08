"""
face_detector.py
----------------
Detects one face using InsightFace and returns:
- Face bounding box
- Smart head & shoulder crop box
"""

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from config import (
    TOP_PADDING,
    SIDE_PADDING,
    BOTTOM_PADDING,
    MAX_FACES,
)

# ----------------------------
# Load model only once
# ----------------------------

app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)


class FaceDetector:

   def detect(self, image):

    img = np.array(image.convert("RGB"))

    faces = app.get(img)

    if len(faces) == 0:
        return {
            "success": False,
            "message": "No face detected."
        }

    # Select largest face
    faces = sorted(
        faces,
        key=lambda f: (
            (f.bbox[2] - f.bbox[0]) *
            (f.bbox[3] - f.bbox[1])
        ),
        reverse=True
    )

    face = faces[0]

    landmarks = face.landmark_2d_106

    h, w = img.shape[:2]

    # -----------------------------
    # Face measurements
    # -----------------------------

    left = np.min(landmarks[:, 0])
    right = np.max(landmarks[:, 0])

    top = np.min(landmarks[:, 1])
    bottom = np.max(landmarks[:, 1])

    face_width = right - left
    face_height = bottom - top

    center_x = (left + right) / 2

    # -----------------------------
    # Adaptive Crop
    # -----------------------------

    crop_width = int(face_width * 2.7)

    crop_height = int(face_height * 3.6)

    crop_x1 = int(center_x - crop_width / 2)
    crop_x2 = int(center_x + crop_width / 2)

    # More space above the hair
    crop_y1 = int(top - face_height * 1.15)

    # Include shoulders & upper chest
    crop_y2 = int(bottom + face_height * 2.1)

    # -----------------------------
    # Keep inside image
    # -----------------------------

    if crop_x1 < 0:
        crop_x2 += -crop_x1
        crop_x1 = 0

    if crop_x2 > w:
        crop_x1 -= (crop_x2 - w)
        crop_x2 = w

    if crop_y1 < 0:
        crop_y1 = 0

    if crop_y2 > h:
        crop_y2 = h

    crop_x1 = max(0, crop_x1)

    return {

        "success": True,

        "confidence": float(face.det_score),

        "face_box": tuple(face.bbox.astype(int)),

        "crop_box": (
            int(crop_x1),
            int(crop_y1),
            int(crop_x2),
            int(crop_y2)
        )

    }


detector = FaceDetector()