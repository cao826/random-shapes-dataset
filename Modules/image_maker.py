"""creates the images"""
import random
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib import patches

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

def really_slow_mask_maker(image_array, color):
    """ugh"""
    rows, columns, channels = image_array.shape
    mask = np.zeros((rows, columns), float)
    for i in range(rows):
        for j in range(columns):
            r = image_array[i, j, 0]
            g = image_array[i, j, 1]
            b = image_array[i, j, 2]
            if (r, g, b) == color:
                mask[i, j] = 1
    return mask

def create_all_masks(image_array, image_instance):
    """creates a mask for all of the shapes present in the image"""
    masks_dict = dict()
    for shapetype, shape_instance in image_instance['shapes'].items():
        color = shape_instance.color
        mask = really_slow_mask_maker(image_array, color)
        masks_dict[shapetype] = mask
    return masks_dict

def get_bbox_dict(masks_dict: dict):
    """It was the best of times, it was the worst of times"""
    bbox_dict = dict()
    for shapetype, mask in masks_dict.items():
        bbox_dict[shapetype] = extract_bboxes(mask)[0]
    return bbox_dict

def get_height_and_width(y1, x1, y2, x2):
    """why does this have to be so painful"""
    height = abs(y2 - y1)
    width = abs(x2 - x1)
    return height, width

def make_patch(bbox):
    y1, x1, y2, x2 = bbox
    height, width = get_height_and_width(y1, x1, y2, x2)
    rect = patches.Rectangle((x1, y1),
                             width=width,
                             height=height,
                             edgecolor='r',
                             facecolor='none')
    return rect
def make_patches(bbox_dict):
    """makes all patches for all of the shapes"""
    return [make_patch(bbox) for bbox in bbox_dict.values()]

def make_full_image_analysis(image_array, image_instance):
    """makes everything we need to make the full plot of all the masksk and ground truth boxes"""
    mask_dict = create_all_masks(image_array, image_instance)
    bbox_dict = get_bbox_dict(mask_dict)
    number_of_axes = 2 + len(mask_dict)
    bbox_patches = make_patches(bbox_dict)
    fig, axs = plt.subplots(1, number_of_axes, figsize=(10, 6))
    axs[0].imshow(image_array)
    axs[0].axis('off')
    axs[1].imshow(image_array)
    axs[1].axis('off')
    for patch in bbox_patches:
        axs[1].add_patch(patch)
    i = 2
    for mask in mask_dict.values():
        axes = axs[i]
        axes.imshow(mask, cmap='gray')
        axes.axis('off')
        i+=1
    plt.show(block=False)
    plt.pause(6.5)
    plt.close()

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

### code adapted from Matterport's MaskRCNN

def extract_bboxes(mask):
    """Compute bounding boxes from masks.
    mask: [height, width, num_instances]. Mask pixels are either 1 or 0.

    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    comp_mask = np.expand_dims(mask, axis=2) #expands on the last dim for this function
    boxes = np.zeros([comp_mask.shape[-1], 4], dtype=np.int32)
    for i in range(comp_mask.shape[-1]):
        m = comp_mask[:, :, i]
        # Bounding box.
        horizontal_indicies = np.where(np.any(m, axis=0))[0]
        vertical_indicies = np.where(np.any(m, axis=1))[0]
        if horizontal_indicies.shape[0]:
            x1, x2 = horizontal_indicies[[0, -1]]
            y1, y2 = vertical_indicies[[0, -1]]
            # x2 and y2 should not be part of the box. Increment by 1.
            x2 += 1
            y2 += 1
        else:
            # No mask for this instance. Might happen due to
            # resizing or cropping. Set bbox to zeros
            x1, x2, y1, y2 = 0, 0, 0, 0
        boxes[i] = np.array([y1, x1, y2, x2])
    return boxes.astype(np.int32)
