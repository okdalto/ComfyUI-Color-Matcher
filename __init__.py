"""
ComfyUI Color Matcher - Custom Node
Applies color matching from a reference image to source images/video frames.
"""

from .nodes.color_match import ColorMatch

NODE_CLASS_MAPPINGS = {
    "ColorMatch": ColorMatch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ColorMatch": "Color Match",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
