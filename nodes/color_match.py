import numpy as np
import torch
from color_matcher import ColorMatcher
from color_matcher.normalizer import Normalizer
import comfy.utils


class ColorMatch:
    METHODS = ["mkl", "hm", "reinhard", "mvgd", "hm-mvgd-hm", "hm-mkl-hm"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "src_images": ("IMAGE",),
                "ref_image": ("IMAGE",),
                "method": (cls.METHODS, {"default": "mkl"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "match_color"
    CATEGORY = "image/color"

    def match_color(self, src_images, ref_image, method):
        # Convert reference image to numpy uint8 (use first frame only)
        ref_np = (ref_image[0].cpu().numpy() * 255).astype(np.uint8)

        batch_size = src_images.shape[0]
        result_frames = []
        pbar = comfy.utils.ProgressBar(batch_size)

        cm = ColorMatcher()

        for i in range(batch_size):
            src_np = (src_images[i].cpu().numpy() * 255).astype(np.uint8)
            matched = cm.transfer(src=src_np, ref=ref_np, method=method)
            matched = Normalizer(matched).uint8_norm()
            # Convert back to float32 tensor
            matched_tensor = torch.from_numpy(matched.astype(np.float32) / 255.0)
            result_frames.append(matched_tensor)
            pbar.update(1)

        return (torch.stack(result_frames),)
