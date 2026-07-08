"""
config.py
----------------------------------------
Configuration
"""

import os

# -----------------------------
# Project folders
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

MEMBERS_DIR = os.path.join(UPLOADS_DIR, "members")

PROCESSED_DIR = os.path.join(UPLOADS_DIR, "members_processed")

TEMP_DIR = os.path.join(BASE_DIR, "temp")

BACKGROUND_IMAGE = os.path.join(BASE_DIR, "background.png")

# -----------------------------
# Output
# -----------------------------

OUTPUT_SIZE = (400, 400)

TARGET_FILE_SIZE_KB = 250

# -----------------------------
# Face Detection
# -----------------------------

MAX_FACES = 1

# Crop padding
TOP_PADDING = 1.0
SIDE_PADDING = 0.8
BOTTOM_PADDING = 2.2

# -----------------------------
# Create folders automatically
# -----------------------------

os.makedirs(MEMBERS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)