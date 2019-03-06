#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct
import math

import numpy as np

from thumbor.detectors import BaseDetector
from thumbor.point import PrimaryColorPoint

class Detector(BaseDetector):
    def detect(self, callback):
        try:
            image = self.context.modules.engine.get_rgb_image()

            # resize image to optimize calculating of average color by reducing points count
            width = 24
            height = 24
            resized_image = image.resize((width, height))

            # ~5kb
            # print(sys.getsizeof(colors))
            colors = resized_image.getcolors(width * height)

            c = 0 # count
            r = 0
            g = 0
            b = 0
            for color in colors:
                c += color[0]
                r += color[1][0]
                g += color[1][1]
                b += color[1][2]

            avg_r = r / c
            avg_g = g / c
            avg_b = b / c

            primary_color_str = 'rgb({}, {}, {})'.format(avg_r, avg_g, avg_b)
        except Exception as e:
            print('[PrimaryColorDetector]', e)
            primary_color_str = 'rgb(255, 255, 255)'

        self.context.request.focal_points.append(
            PrimaryColorPoint(0, 0, primary_color_str)
        )

        callback([])
