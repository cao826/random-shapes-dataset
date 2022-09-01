"""Code to generate the shapes"""

from typing import Callable
from collections import namedtuple
import random
import PIL
from PIL import Image, ImageDraw

class Shape:
    """Definition for all shapes in the image. Each shape has a:
        - Type (e.g. 'circle') (this is our label)
        - rule: a function that takes the image shape as a parameter and
                returns a parameterization of the image
        - color: does it need to have this property?
        -specifications: holds other things it may need in a dict
    """
    def __init__(self, shapetype: str, rule: Callable,
                 specifications: dict = None):
        """Constructor"""
        self.type = shapetype
        self.rule = rule
        self.specifications = specifications

    def __call__(self, image_shape: tuple, color: tuple):
        """Builds the shape with the image size in mind"""
        if self.specifications:
            parameterization = self.rule(image_shape=image_shape,
                                         specifications=self.specifications)
        else:
            parameterization = self.rule(image_shape)
        shape = namedtuple(self.type, ['parameterization', 'color'])
        shape_instance = shape(parameterization, color)
        return shape_instance

def sample_points_within(image_shape: tuple, number_of_points: int):
    """Samples N points within the image shape"""
    height, width = image_shape
    x_coordinates = random.sample(population=range(width),
                                  k=number_of_points)
    y_coordinates = random.sample(population=range(height),
                                  k=number_of_points)
    if len(x_coordinates) == 1:
        x_coordinates = x_coordinates[0]
        y_coordinates = y_coordinates[0]
    return x_coordinates, y_coordinates

def triangle_rule(image_shape: tuple):
    """Generates a triangle within the image shape specified"""
    height, width = image_shape
    sample_size = min(height, width)
    sample_space = range(sample_size)
    x_coordinates = random.sample(population=sample_space,
                                  k=3)
    y_coordinates = random.sample(population=sample_space,
                                  k=3)
    parameterization = [(x_coordinates[i], y_coordinates[i])
                        for i in range(3)]
    return parameterization

def choose_size(bbox_specification: dict):
    """Chooses a random size within the bounds in specification"""
    min_size = bbox_specification['min_size']
    max_size = bbox_specification['max_size']

    size = random.randint(min_size, max_size)
    return size

def bounding_box_rule(image_shape: tuple, specifications: dict):
    """Rule for both squares and circles"""
    size = choose_size(specifications)
    starting_point = sample_points_within(image_shape=image_shape,
                                          number_of_points=1)
    other_point = tuple(point + size for point in starting_point)
    parameterization = [starting_point, other_point]
    return parameterization

class Triangle(Shape):
    """Triangle class. Used to make...................triangles."""
    def __init__(self, specifications=None):
        """constructor"""
        super().__init__(shapetype='Triangle',
                       rule=triangle_rule,
                       specifications=specifications,)

class Square(Shape):
    """Class for generating squares"""
    def __init__(self, specifications):
        """Constructor"""
        super().__init__(shapetype='Square',
                         rule=bounding_box_rule,
                         specifications=specifications,)

class Circle(Shape):
    """Class for constructing circles"""
    def __init__(self, specifications):
        """Constructor"""
        super().__init__(shapetype='Circle',
                         rule=bounding_box_rule,
                         specifications=specifications,)
