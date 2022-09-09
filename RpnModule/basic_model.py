"""A simple module that contains the simplest iteration of a 
region proposal network for training on the 
shapes dataset"""
import sys
sys.path.insert(1, "/Users/carlosolivares/random-shapes-dataset")
from collections import namedtuple
import torch
import torchvision
import matplotlib.pyplot as plt
from torchvision.models.detection.anchor_utils import AnchorGenerator
from torchvision.models.detection.image_list import ImageList
from torchvision.models.detection import rpn
from torchvision import transforms as T
from Modules import image_maker, shapes, colors


## treansforms I will use

def vgg16_featuremapper():
    model_repo = 'pytorch/vision:v0.10.1'
    model_name = 'vgg16'
    full_pretrained_vgg16 = torch.hub.load(
        repo_or_dir=model_repo,
        model=model_name,
        pretrained=True
    )
    for child in full_pretrained_vgg16.children():
        break
    model = torch.nn.Sequential(child)
    return model

normalize = T.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

standard_transform = T.Compose(
    [
        T.ToTensor(),
        normalize,
    ]
)

anchor_generator = AnchorGenerator()
num_feature_map_channels = 512

rpn_pre_nms_top_n = {"training": 2000, "testing": 1000}
rpn_post_nms_top_n = {"training": 2000, "testing": 1000}
rpn_nms_thresh = 0.7
rpn_fg_iou_thresh = 0.7
rpn_bg_iou_thresh = 0.2
rpn_batch_size_per_image = 256
rpn_positive_fraction = 0.5

class BasicRegionProposalNetwork():
    """The simplest iteration of a region proposal network
    as faithful to the original implementation from the paper
    as possible"""

    def __init__():
        self.vgg16_backbone = vgg16_featuremapper()
        self.anchor_generator = anchor_generator
        self.anchors_per_location = anchor_generator.num_anchors_per_location()[0]
        self.rpn_head = rpn.RPNHead(in_channels=num_feature_map_channels,
                                    num_anchors=self.anchors_per_location)
        self.rpn(
            anchor_generator=anchor_generator,
            head=self.rpn_head
            fg_iou_thresh=rpn_fg_iou_thresh,
            bg_iou_thresh=rpn_bg_iou_thresh,
            batch_size_per_image=rpn_batch_size_per_image,
            positive_fraction=rpn_postive_fraction,
            pre_nms_top_n=rpn_pre_nms_top_n,
            post_nms_top_n=rpn_post_nms_top_n,
            nms_thresh=rpn_nms_thresh
            )

