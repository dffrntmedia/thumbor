#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct
import math

from thumbor.detectors import BaseDetector
from thumbor.point import PrimaryColorPoint
from thumbor.utils import logger

class Detector(BaseDetector):

    def detect(self, callback):
        self.context.modules.engine.resize(self.context.request.width, self.context.request.height)

        image_data = self.context.modules.engine.image_data_as_rgb()
        color_type, color_string = image_data

        step = len(color_type)

        colors = [color_string[i:i+step] for i in range(0, len(color_string), step)]

        # colors_dict = {}

        numb_colors = [[struct.unpack('@B', component)[0] for component in color] for color in colors]

        points_count = len(numb_colors)

        numb_colors = zip(*numb_colors)

        numb_colors = [sum(list) for list in numb_colors]

        numb_colors = [str(int(math.ceil(a / points_count))) for a in numb_colors]

        print(numb_colors)

        # for color in colors:
        #     if not color in colors_dict:
        #         colors_dict[color] = 0
        #     colors_dict[color] += 1

        # primary_color = None
        # max_color_count = 0

        # for key, val in colors_dict.items():
        #     if val > max_color_count:
        #         max_color_count = val
        #         primary_color = key

        # primary_color_str = color_type.lower() + '(' + (', '.join([str(struct.unpack('@B', a)[0]) for a in primary_color])) + ')'

        primary_color_str = color_type.lower() + '(' + (', '.join(numb_colors)) + ')'

        self.context.request.focal_points.append(
            PrimaryColorPoint(0, 0, primary_color_str)
        )

        callback([])
