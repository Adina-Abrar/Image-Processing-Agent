"""
enhancer.py
----------------------------------------
Professional Portrait Enhancer

Features
---------
✓ Preserve transparency (RGBA)
✓ Auto White Balance
✓ CLAHE Contrast Enhancement
✓ Mild Denoise
✓ Professional Sharpening
✓ Natural Colors
✓ Does NOT resize or stretch image
"""

import cv2
import numpy as np

from PIL import Image, ImageEnhance


class ImageEnhancer:

    def __init__(self):
        pass

    # ---------------------------------------
    # White Balance (Gray World Algorithm)
    # ---------------------------------------

    def white_balance(self, img):

        img = img.astype(np.float32)

        b, g, r = cv2.split(img)

        b_avg = np.mean(b)
        g_avg = np.mean(g)
        r_avg = np.mean(r)

        gray = (b_avg + g_avg + r_avg) / 3

        if b_avg > 0:
            b *= gray / b_avg

        if g_avg > 0:
            g *= gray / g_avg

        if r_avg > 0:
            r *= gray / r_avg

        img = cv2.merge((b, g, r))

        img = np.clip(img, 0, 255).astype(np.uint8)

        return img

    # ---------------------------------------
    # CLAHE Contrast Enhancement
    # ---------------------------------------

    def enhance_contrast(self, img):

        lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=1.8,
            tileGridSize=(8, 8)
        )

        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))

        return cv2.cvtColor(
            lab,
            cv2.COLOR_LAB2RGB
        )

    # ---------------------------------------
    # Noise Reduction
    # ---------------------------------------

    def denoise(self, img):

        return cv2.fastNlMeansDenoisingColored(
            img,
            None,
            4,
            4,
            7,
            21
        )

    # ---------------------------------------
    # Sharpen
    # ---------------------------------------

    def sharpen(self, img):

        gaussian = cv2.GaussianBlur(
            img,
            (0, 0),
            2
        )

        return cv2.addWeighted(
            img,
            1.15,
            gaussian,
            -0.15,
            0
        )

    # ---------------------------------------
    # Final Enhancement
    # ---------------------------------------

    def process(self, image):

        # ---------------------------------------
        # Preserve Alpha Channel
        # ---------------------------------------

        if image.mode == "RGBA":

            alpha = image.getchannel("A")

            rgb = image.convert("RGB")

        else:

            alpha = None

            rgb = image.convert("RGB")

        img = np.array(rgb)

        # ---------------------------------------
        # White Balance
        # ---------------------------------------

        img = self.white_balance(img)

        # ---------------------------------------
        # CLAHE
        # ---------------------------------------

        img = self.enhance_contrast(img)

        # ---------------------------------------
        # Denoise
        # ---------------------------------------

        img = self.denoise(img)

        # ---------------------------------------
        # Sharpen
        # ---------------------------------------

        img = self.sharpen(img)

        image = Image.fromarray(img)

        # ---------------------------------------
        # Final Natural Adjustments
        # ---------------------------------------

        image = ImageEnhance.Color(image).enhance(1.05)

        image = ImageEnhance.Contrast(image).enhance(1.06)

        image = ImageEnhance.Brightness(image).enhance(1.02)

        image = ImageEnhance.Sharpness(image).enhance(1.15)

        # ---------------------------------------
        # Restore Alpha Channel
        # ---------------------------------------

        if alpha is not None:

            result = image.convert("RGBA")

            result.putalpha(alpha)

            return result
        

        return image


enhancer = ImageEnhancer()