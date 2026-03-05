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
                "image_ref": ("IMAGE",),
                "image_target": ("IMAGE",),
                "method": (cls.METHODS, {"default": "mkl"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "match_color"
    CATEGORY = "image/color"

    def match_color(self, image_ref, image_target, method):
        # Convert reference image to numpy uint8 (use first frame only)
        ref_np = (image_ref[0].cpu().numpy() * 255).astype(np.uint8)

        batch_size = image_target.shape[0]
        result_frames = []
        pbar = comfy.utils.ProgressBar(batch_size)

        cm = ColorMatcher()

        for i in range(batch_size):
            src_np = (image_target[i].cpu().numpy() * 255).astype(np.uint8)
            matched = cm.transfer(src=src_np, ref=ref_np, method=method)
            matched = Normalizer(matched).uint8_norm()
            # Convert back to float32 tensor
            matched_tensor = torch.from_numpy(matched.astype(np.float32) / 255.0)
            result_frames.append(matched_tensor)
            pbar.update(1)

        return (torch.stack(result_frames),)
