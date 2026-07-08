"""
compressor.py
----------------------------------------
PNG Optimizer
Preserves transparency
"""

import io
from PIL import Image


class ImageCompressor:

    def compress(self, image: Image.Image):

        buffer = io.BytesIO()

        image.save(

            buffer,

            format="PNG",

            optimize=True

        )

        size = buffer.tell() / 1024

        print(f"✅ PNG Optimized ({size:.1f} KB)")

        buffer.seek(0)

        return Image.open(buffer)


compressor = ImageCompressor()