from pathlib import Path

from setuptools import setup, find_packages


core_dir = Path(__file__).parent

long_description = (core_dir / "README.md").read_text()

setup(
    name="facialfinder",
    version="0.0.4",
    url="https://github.com/Anonimous05/FacialFinder",
    author="Airas Tolonov",
    author_email="airastolonov05@gmail.com",
    description="Simple tool for Face Detection on Image or Video, realtime detection support.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'facialfinder': ['datasets/*.xml']},
    install_requires=[
        'numpy==1.26.4',
        'opencv-python==4.9.0.80',
        'progressbar2==4.4.2'
    ],
)
