import os

from config import STATIC_ROOT, IMAGES_ROOT, VIDEOS_ROOT
from services import ImageDetection, VideoDetection


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
    src: you may set index of camera, example - 0 (WEB Camera), 1 - second Camera ...
"""

my_video = VideoDetection(
    src=0,
    scale_factor=1.2,
    min_neighbors=5,

    rect_color=(0, 0, 0),
    rect_thickness=1,
    text_color=(0, 255, 0),
    text='Face',
    delay=1,
    fourcc='MJPG',
    output_path=os.path.join(STATIC_ROOT, 'examples/detected_faces.avi')
)

my_video.detect()

