"""
cropper.py
----------------------------------------
Professional Portrait Cropper
Keeps original aspect ratio
No stretching
"""

from PIL import Image, ImageOps

from config import OUTPUT_SIZE


class Cropper:

    def crop(self, image: Image.Image, crop_box):

        x1, y1, x2, y2 = crop_box

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image.width, x2)
        y2 = min(image.height, y2)

        return image.crop((x1, y1, x2, y2))

    def resize(self, image: Image.Image):

        image = ImageOps.fit(
            image,
            OUTPUT_SIZE,
            method=Image.LANCZOS,
            centering=(0.5, 0.35)
)

        return image

        # Transparent canvas
        canvas = Image.new(
            "RGBA",
            OUTPUT_SIZE,
            (0, 0, 0, 0)
        )

        x = (OUTPUT_SIZE[0] - image.width) // 2
        y = (OUTPUT_SIZE[1] - image.height) // 2

        if image.mode != "RGBA":
            image = image.convert("RGBA")

        canvas.paste(image, (x, y), image)

        return canvas

    def process(self, image, crop_box):

        image = self.crop(image, crop_box)

        image = self.resize(image)

        return image


cropper = Cropper()