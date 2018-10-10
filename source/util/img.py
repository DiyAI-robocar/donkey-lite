import io

from PIL import Image
import numpy as np


def img_to_binary(img: object) -> object:
    """
    ToDo
    :param img: PIL image
    :return: binary stream (used to save to database)
    """
    f = io.BytesIO()
    img.save(f, format='jpeg')
    return f.getvalue()


def arr_to_binary(arr: list) -> object:
    """
    ToDo
    :param arr: numpy array with shape (Hight, Width, Channels)
    :return: binary stream (used to save to database)
    """
    img = arr_to_img(arr)
    return img_to_binary(img)


def arr_to_img(arr: list) -> object:
    """
    ToDo
    :param arr: numpy array with shape (Hight, Width, Channels)
    :return: binary stream (used to save to database)
    """
    arr = np.uint8(arr)
    img = Image.fromarray(arr)
    return img
