import PIL
from PIL import Image, ImageDraw
import colorsys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

#%load_ext autoreload
#%autoreload 2
from Modules import shapes
from Modules import colors
from Modules import image_maker

savepath = '../throwaway/'

color_picker = colors.ColorPicker(colors.KNOWN_COLORS, colors.default_hls_settings)

img_generator = image_maker.ImageMaker(image_shape=(224, 224),
                                       color_picker=color_picker,
                                       number_of_colors=4,
                                       shapes = [
                                           shapes.Triangle(),
                                           shapes.Circle(specifications={
                                               'min_size': 30,
                                               'max_size': 82
                                           }),
                                           shapes.Square(specifications={
                                               'min_size': 25,
                                               'max_size': 66
                                           })
                                       ]
)

#image_maker.make_full_image_analysis(image_as_array, image_instance, savepath)

for i in range(40):
    image_instance = img_generator()

    image = image_maker.construct_image(image_instance)

    image_as_array = np.array(image)
    image_maker.show_an_example(image_as_array, image_instance)
