"""
birefnet_model.py
------------------------------------
BiRefNet Background Removal
"""

import torch
import numpy as np
import cv2

from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation


# -------------------------------------------------
# Device
# -------------------------------------------------

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {DEVICE}")


# -------------------------------------------------
# Load model only ONCE
# -------------------------------------------------

print("Loading BiRefNet...")

model = AutoModelForImageSegmentation.from_pretrained(
    "ZhengPeng7/BiRefNet",
    trust_remote_code=True
)

model.to(DEVICE)

# CPU requires float32
if DEVICE == "cpu":
    model.float()

model.eval()

print("BiRefNet Loaded Successfully")


# -------------------------------------------------
# Image Transform
# -------------------------------------------------

transform = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


# -------------------------------------------------
# Remove Background
# -------------------------------------------------

def remove_background(image: Image.Image):

    print("========== INSIDE remove_background ==========")

    original_size = image.size

    image = image.convert("RGB")

    input_tensor = (
        transform(image)
        .unsqueeze(0)
        .to(DEVICE)
    )

    if DEVICE == "cpu":
        input_tensor = input_tensor.float()

    with torch.no_grad():
        pred = model(input_tensor)[-1]
        pred = pred.sigmoid()

    # Convert prediction to numpy
    mask = pred[0][0].cpu().numpy()

    # Normalize to 0-255
    mask = (mask - mask.min()) / (mask.max() - mask.min() + 1e-8)
    mask = (mask * 255).astype(np.uint8)

    # Resize to original image size
    mask = cv2.resize(
        mask,
        original_size,
        interpolation=cv2.INTER_LINEAR
    )

    # Clean mask
    kernel = np.ones((3, 3), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    mask = cv2.GaussianBlur(
        mask,
        (5, 5),
        0
    )

    # Convert to binary mask
    _, mask = cv2.threshold(
        mask,
        128,
        255,
        cv2.THRESH_BINARY
    )

    # Convert mask to PIL Image
    alpha = Image.fromarray(mask)

    # Save mask for debugging
    alpha.save("mask.png")

    # Apply alpha channel
    result = image.convert("RGBA")
    result.putalpha(alpha)

    # Save transparent PNG for debugging
    result.save("transparent_result.png")

    print("========== Background Removed ==========")

    return result