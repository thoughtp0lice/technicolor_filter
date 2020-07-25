from PIL import Image
import numpy as np
from .technicolor import Technicolor


def read_image(img):
    """
    read image stored at @img
    returns a Technicolor object
    """
    if isinstance(img, str):
        out = Image.open(img)
    return Technicolor(out)


def from_array(img):
    """
    take a array @img
    return a Technicolor object
    """
    img = np.array(img)
    return Technicolor(img)
