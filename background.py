"""
background.py
---------------------------------------
BiRefNet Background Processor
"""

from birefnet_model import remove_background


class BackgroundProcessor:

    def process(self, image):

        return remove_background(image)


background_processor = BackgroundProcessor()