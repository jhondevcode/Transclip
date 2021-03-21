import wx
from loaders import ImageLoader


def scale_bitmap(bitmap: wx.Bitmap, width: int, height: int):
    if bitmap is not None:
        image = wx.Bitmap.ConvertToImage(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result
    else:
        return None


def scale_image(image: wx.Image, width: int, height: int):
    if image is not None:
        return image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    else:
        return None


def img_to_bitmap(image: wx.Image):
    if image is not None:
        return wx.Bitmap(image)
    else:
        return None


def img_load_scaled_bitmap(name: str, width: int, height: int):
    if name != "":
        return img_to_bitmap(scale_image(ImageLoader(name).get(), width, height))
    else:
        return None


def check_button_bitmap(button, bitmap):
    if bitmap is not None:
        button.SetBitmap(bitmap)
