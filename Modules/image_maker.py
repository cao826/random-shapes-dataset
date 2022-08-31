"""creates the images"""
import random
from PIL import Image, ImageDraw

def create_canvas(canvas_shape, canvas_color):
    """creates the blank canvas"""
    canvas = Image.new(mode='RGB',
                       size=canvas_shape,
                       color=canvas_color,)
    return canvas

def construct_shape(draw_instance, shapetype, shape_instance):
    """constructs the shapein the canvas"""
    if shapetype == 'Triangle':
        draw_instance.polygon(xy=shape_instance.parameterization,
                              fill=shape_instance.color)
    elif shapetype == 'Circle':
        draw_instance.ellipse(xy=shape_instance.parameterization,
                              fill=shape_instance.color)
    elif shapetype == 'Square':
        draw_instance.rectangle(xy=shape_instance.parameterization,
                                fill=shape_instance.color)
    else:
        raise Exception('Shape type not recognized')

def construct_image(image_instance):
    """constucts the actual image from the instance"""
    canvas = create_canvas(canvas_shape=image_instance['image_shape'],
                           canvas_color=image_instance['background_color'])
    draw_instance = ImageDraw.Draw(canvas)
    for shapetype, shape_instance in image_instance['shapes'].items():
        construct_shape(draw_instance, shapetype, shape_instance)
    return canvas

class ImageMaker():
    """class that makes the image"""
    def __init__(self, image_shape, shapes, color_picker, number_of_colors):
        """constructor"""
        self.shapes = shapes
        self.color_picker = color_picker
        self.number_of_colors = number_of_colors
        self.image_shape = image_shape

    def choose_shapes(self, colors):
        """chooses which shapes to add to the picture"""
        num_shapes_possible = len(self.shapes)
        number_of_shapes = random.randint(1, num_shapes_possible)
        chosen_shapes = {
                shape.type: shape(self.image_shape, colors.pop())
                for shape in random.sample(population=self.shapes,
                                           k=number_of_shapes)
                }
        return chosen_shapes

    def __call__(self):
        """make an image metadata. we will constuct it later"""
        image = dict()
        colors = self.color_picker(self.number_of_colors)
        image['image_shape'] = self.image_shape
        image['background_color'] = colors.pop()
        image['shapes'] = self.choose_shapes(colors)

        return image
