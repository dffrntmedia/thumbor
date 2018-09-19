#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct
import math

import numpy as np

from thumbor.detectors import BaseDetector
from thumbor.point import PrimaryColorPoint

class Detector(BaseDetector):

    # such implementation will conflict with other detectors

    def detect(self, callback):
        # resize image to optimize calculating of average color by reducing points count
        if self.context.request.width and self.context.request.height:
            self.context.modules.engine.resize(self.context.request.width, self.context.request.height)

        image_data = self.context.modules.engine.image_data_as_rgb()
        color_type, color_string = image_data

        step = len(color_type)

        try:
            colors = [color_string[i:i+step] for i in range(0, len(color_string), step)]

            # converting to numbers from hex strings
            number_colors = [[struct.unpack('@B', color_component)[0] for color_component in color] for color in colors]

            avg_color_component_list = np.matrix(number_colors).mean(axis=0).tolist()[0]

            number_colors = [str(int(math.ceil(color_component))) for color_component in avg_color_component_list]

            primary_color_str = '{}({})'.format(color_type.lower(), ', '.join(number_colors))
        except:
            primary_color_str = 'rgb(255, 255, 255, 255)'

        self.context.request.focal_points.append(
            PrimaryColorPoint(0, 0, primary_color_str)
        )

        callback([])
