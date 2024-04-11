import os

import cv2

from config import DATASETS_ROOT


class ImageDetection:

    def __init__(self, path: str, scale_factor: float, min_neighbors: int,
                 rect_color: tuple = (255, 0, 0), text: str = None, text_color: tuple = (255, 0, 0),
                 show_title: str = 'Result of detection', delay: int = 0, output_path: str = None):
        """
        :param path: path to file (.png, .jpeg, .jpg, ...)
        :param scale_factor: (Read the OpenCV docs)
        :param min_neighbors: (Read the OpenCV docs)
        :param rect_color: color of rectangle (detected objects) must be tuple (B, G, R)
        :param text: title of detected objects
        :param text_color: color of text (detected objects) must be tuple (B, G, R)
        :param show_title: title of detected objects window
        :param delay: cv2.waitKey(delay)
        :param output_path: if you call .detect() method, you must set result file path
        """
        self.path = path
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.rect_color = rect_color
        self.text = text
        self.text_color = text_color
        self.show_title = show_title
        self.delay = delay
        self.output_path = output_path
        self.original_file = None
        self.prepared_file = None
        self.count = 0

        self._prepare_file()

    def _prepare_file(self):
        self.original_file = cv2.imread(self.path)
        self.prepared_file = cv2.cvtColor(self.original_file, cv2.COLOR_BGR2GRAY)

    def _detect(self):
        """
        This method need for use faces.xml dataset (prepared for face detection) (default)
        And save detected results in instance.results attr
        """
        dataset = cv2.CascadeClassifier(os.path.join(DATASETS_ROOT, 'faces.xml'))
        self.results = dataset.detectMultiScale(
            self.prepared_file,
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
                cv2.putText(self.original_file, self.text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, self.text_color, 2)

            cv2.rectangle(self.original_file, (x, y), (x + h, y + w), self.rect_color)

    def show(self):
        """
        Show result of detection on Window
        PS: every method of this class have comments!!!
        """
        self._detect()
        self._draw_detected_objects()

        cv2.imshow(self.show_title, self.original_file)
        cv2.waitKey(self.delay)

    def detect(self):
        """
        Detect objects and save the instance.output_path file
        :return: path to detected file

        PS: every method of this class have comments!!!
        """
        if self.output_path is None:
            raise AttributeError('instance.output_path required')

        self._detect()
        self._draw_detected_objects()

        cv2.imwrite(self.output_path, self.original_file)
        return self.output_path
