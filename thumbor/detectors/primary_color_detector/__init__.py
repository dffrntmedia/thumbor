#!/usr/bin/python
# -*- coding: utf-8 -*-


from thumbor.detectors import BaseDetector
from thumbor.point import PrimaryColorPoint
from thumbor.utils import logger


class Detector(BaseDetector):

    def detect(self, callback):
        self.context.request.focal_points.append(
            PrimaryColorPoint(0, 0, "rgba(0, 0, 0, 1)")
        )
        callback([])
