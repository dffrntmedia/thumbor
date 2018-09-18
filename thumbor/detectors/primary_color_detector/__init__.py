#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct

from thumbor.detectors import BaseDetector
from thumbor.point import PrimaryColorPoint
from thumbor.utils import logger

class Detector(BaseDetector):

    def detect(self, callback):
        image_data = self.context.modules.engine.image_data_as_rgb()
        color_type, color_string = image_data

        step = len(color_type)

        colors = [color_string[i:i+step] for i in range(0, len(color_string), step)]

        colors_dict = {}

        for color in colors:
            if not color in colors_dict:
                colors_dict[color] = 0
            colors_dict[color] += 1

        primary_color = None
        max_color_count = 0

        for key, val in colors_dict.items():
            if val > max_color_count:
                max_color_count = val
                primary_color = key

        primary_color_str = color_type.lower() + '(' + (', '.join([str(struct.unpack('@B', a)[0]) for a in primary_color])) + ')'

        self.context.request.focal_points.append(
            PrimaryColorPoint(0, 0, primary_color_str)
        )

        callback([])
