import os

CORE_DIR: str = os.getcwd()

DATASETS_ROOT: str = os.path.join(CORE_DIR, 'datasets')

STATIC_ROOT: str = os.path.join(CORE_DIR, 'static')
IMAGES_ROOT: str = os.path.join(STATIC_ROOT, 'images')
VIDEOS_ROOT: str = os.path.join(STATIC_ROOT, 'videos')
