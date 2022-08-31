"""
Code to randomly generate colors


This code has some elements that I would like to improve.
Specifically, there are a lot of hard coded values that I would like to
address.
"""
import colorsys
import random
import math

KNOWN_COLORS = [0, 30, 60, 90, 120, 210, 240, 270]

HLS_PARAMETERS = {'hue':360,
                  'lightness':100,
                  'saturation':100,}

default_hls_settings = {'lightness': 67,
                        'saturation': 41,}

def normalize_hls(coordinates: tuple):
    """normalizes the hls coordinates"""
    hue, lightness, saturation = coordinates
    return (hue / HLS_PARAMETERS['hue'],
            lightness / HLS_PARAMETERS['lightness'],
            saturation / HLS_PARAMETERS['saturation'])

def rgb_scaler(value: float):
    """converts a single float value to rgb"""
    rounding_safe_scalar = min(1.0, value)
    if rounding_safe_scalar == 1.0:
        return 255
    return value * 256

def to_rgb(normed_hls: tuple):
    """produces an rgb tuple"""
    return tuple( math.floor(rgb_scaler(value)) for value in normed_hls)

def convert_hls_rgb(unnormed_coord: tuple):
    """changes an unnormed coord in hls to an unnormed rgb coord"""
    return to_rgb(colorsys.hls_to_rgb(*normalize_hls(unnormed_coord)))

class ColorPicker():
    """Callable that chooses N colors for an image"""
    def __init__(self, hue_codes: list, hls_parameters: dict):
        self.hues = hue_codes
        self.hls_parameters = hls_parameters

    def get_color(self, hue_code):
        """Gets an rgb code from hue code and available information"""
        hls_coordinates = (hue_code,
                           self.hls_parameters['lightness'],
                           self.hls_parameters['saturation'])
        rgb_coordinate = convert_hls_rgb(hls_coordinates)
        return rgb_coordinate

    def __call__(self, n: int):
        """returns N hue codes"""
        if n > len(self.hues):
            raise Exception(('Usertrying to sample {n} colors, but '
                             'there are only {len(self.hues)} hue codes'))
        chosen_colors = random.sample(population=self.hues,
                             k=n)
        return [self.get_color(hue_code) for hue_code in chosen_colors]
