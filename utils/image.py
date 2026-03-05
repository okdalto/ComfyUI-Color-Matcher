import numpy as np
import torch
from PIL import Image


def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def rgb_crop(rgb, region):
    return rgb[region[1]:region[3], region[0]:region[2]]

def rgb_crop_batch(rgbs, region):
    return rgbs[:, region[1]:region[3], region[0]:region[2]]

def get_rgb_size(rgb):
    return rgb.shape[1], rgb.shape[0]
