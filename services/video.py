import os

import cv2
from progressbar import ProgressBar

from config import DATASETS_ROOT


class VideoDetection:

    def __init__(self,
                 src: str,
                 scale_factor: float,
                 min_neighbors: int,

                 rect_color: tuple = (255, 0, 0),
                 rect_thickness: int = 1,
                 text: str = None,
                 text_color: tuple = (255, 0, 0),
                 show_title: str = 'Result of detection',
                 delay: int = 1,
                 fourcc: str = 'mp4v',
                 output_path: str = None
                 ):
        """
        :param src: path to file OR index of camera REQUIRED
        :param scale_factor: (Read the OpenCV docs) REQUIRED
        :param min_neighbors: (Read the OpenCV docs) REQUIRED

        :param rect_color: color of rectangle (detected objects) must be tuple (B, G, R)
        :param rect_thickness: rectangle thickness must be integer
        :param text: title of detected objects
        :param text_color: color of text (detected objects) must be tuple (B, G, R)
        :param show_title: title of detected objects window
        :param delay: cv2.waitKey(delay)
        :param output_path: if you call .detect() method, you must set result file path
        """
        self.src: str = src
        self.scale_factor: float = scale_factor
        self.min_neighbors: int = min_neighbors

        self.rect_color: tuple = rect_color
        self.rect_thickness: float = rect_thickness
        self.text: str = text
        self.text_color: tuple = text_color
        self.show_title: str = show_title
        self.delay: int = delay
        self.fourcc: str = fourcc
        self.output_path: str = output_path

        self.capture: cv2.VideoCapture = None
        self.original_video: cv2.typing.MatLike = None
        self.prepared_video: cv2.typing.MatLike = None
        self.size = None
        self.duration = None

        self._count: int = 0

        self._prepare_video()

    def _prepare_video(self):
        self.capture = cv2.VideoCapture(self.src)

        if not self.capture.isOpened():
            raise ValueError('Error reading video file or camera')

        self.size = (self.capture.get(3).__int__(), self.capture.get(4).__int__())
        frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.duration = frames / fps

    def _detect(self):
        """
        This method need for use faces.xml dataset (prepared for face detection) (default)
        And save detected results in instance.results attr
        """
        dataset = cv2.CascadeClassifier(os.path.join(DATASETS_ROOT, 'faces.xml'))
        self.results = dataset.detectMultiScale(
            self.prepared_video,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors
        )
        self.count = self.results.__len__()

    def _draw_detected_objects(self):
        """
        This method need for draw detected objects on instance.original_file
        And put text for every detected objects
        """
        for x, y, w, h in self.results:
            if self.text:
                cv2.putText(self.original_video, self.text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, self.text_color,
                            2)

            cv2.rectangle(self.original_video, (x, y), (x + h, y + w), self.rect_color, self.rect_thickness)

    def _show(self, write: bool = False):
        """
        Show detection of video or camera
        Click 'Q' for close Result Window
        """
        out, bar = None, None
        if write:
            if self.output_path is None:
                raise AttributeError('instance.output_path is required')

            out = cv2.VideoWriter(self.output_path, cv2.VideoWriter_fourcc(*self.fourcc), 20.0, self.size)
            # progressbar for saving detection
            bar = ProgressBar(max_value=100, prefix='Detection')

        while self.capture.isOpened():
            if write and type(self.src) == str:
                current_msc = "%.2f" % (self.capture.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                bar.update(round((float(current_msc) / self.duration) * 100))

            success, self.original_video = self.capture.read()
            self.prepared_video = cv2.cvtColor(self.original_video, cv2.COLOR_BGR2GRAY)

            self._detect()
            self._draw_detected_objects()

            if write & success:
                out.write(self.original_video)

            if write and type(self.src) == int or not write:
                cv2.imshow(self.show_title, self.original_video)

            if cv2.waitKey(self.delay) & 0xFF == ord('q'):
                self.capture.release()
                if out:
                    out.release()
                cv2.destroyAllWindows()

    def show(self):
        try:
            self._show()
        except (KeyboardInterrupt, cv2.error) as error:
            pass

    def detect(self):
        try:
            self._show(write=True)
        except (KeyboardInterrupt, cv2.error) as error:
            pass
