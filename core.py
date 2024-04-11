import os

from config import STATIC_ROOT, IMAGES_ROOT, VIDEOS_ROOT
from services import ImageDetection


"""
    Example of ImageDetection
"""

my_img = ImageDetection(
    path=os.path.join(IMAGES_ROOT, 'img.png'),
    scale_factor=1.25,
    min_neighbors=5,

    output_path=os.path.join(STATIC_ROOT, 'examples/detected_faces.png'),
    text='Face',
    text_color=(0, 0, 0),
    rect_color=(0, 0, 255)
)
my_img.detect()


"""
    Example of VideoDetection
"""
