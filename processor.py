"""
processor.py
---------------------------------------
Main Image Processing Pipeline
"""

from PIL import Image

from face_detector import detector
from cropper import cropper
from background import background_processor
from enhancer import enhancer
from compressor import compressor


class ImageProcessor:

    def process(self, image_path):

        print("=" * 60)
        print("🚀 Starting Image Processing")
        print("=" * 60)

        image = Image.open(image_path).convert("RGB")

        print("✅ Image loaded")

        # -------------------------
        # Face Detection
        # -------------------------

        result = detector.detect(image)

        if not result["success"]:
            raise Exception(result["message"])

        print(
            f"✅ Face detected ({result['confidence']:.2f})"
        )

        crop_box = result["crop_box"]

        # -------------------------
        # Crop
        # -------------------------

        image = cropper.process(
            image,
            crop_box
        )

        print("✅ Portrait cropped")

        # -------------------------
        # Background
        # -------------------------

 # -------------------------
# Remove Background
# -------------------------

        print("Entering Background Processor...")

        image = background_processor.process(image)

        print("Returned From Background Processor")

        print("Image Mode:", image.mode)

        # -------------------------
        # Enhancement
        # -------------------------

        image = enhancer.process(image)

        print("✅ Image enhanced")

        # -------------------------
        # Compression
        # -------------------------

        image = compressor.compress(image)
        print("Final Image Mode:", image.mode)

        print("✅ Image compressed")

        print("=" * 60)
        print("🎉 Processing Finished")
        print("=" * 60)

        return image


processor = ImageProcessor()