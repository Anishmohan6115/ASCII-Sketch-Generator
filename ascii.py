#!.\venv\Scripts\python.exe
import colorsys
import sys
from PIL import Image, ImageFilter
from PIL import ImageOps
class Level(object):

    def __init__(self, minv, maxv, gamma):
        self.minv= minv/255.0
        self.maxv= maxv/255.0
        self._interval= self.maxv - self.minv
        self._invgamma= 1.0/gamma

    def new_level(self, value):
        if value <= self.minv: return 0.0
        if value >= self.maxv: return 1.0
        return ((value - self.minv)/self._interval)**self._invgamma

    def convert_and_level(self, band_values):
        h, s, v= colorsys.rgb_to_hsv(*(i/255.0 for i in band_values))
        new_v= self.new_level(v)
        return tuple(int(255*i)
                for i
                in colorsys.hsv_to_rgb(h, s, new_v))

def level_image(image, minv=0, maxv=255, gamma=1.0):
    """Level the brightness of image (a PIL.Image instance)
    All values ≤ minv will become 0
    All values ≥ maxv will become 255
    gamma controls the curve for all values between minv and maxv"""

    if image.mode != "RGB":
        raise ValueError("this works with RGB images only")

    new_image= image.copy()

    leveller= Level(minv, maxv, gamma)
    levelled_data= [
        leveller.convert_and_level(data)
        for data in image.getdata()]
    new_image.putdata(levelled_data)
    return new_image

#Take image input from terminal
img = Image.open(sys.argv[1])

#Apply a low pass filter so that high frequencies are ripped out
blur_filter = ImageFilter.GaussianBlur(radius=16)
blur_img = img.filter(blur_filter)

#Invert the image and blend in with the original image with 50% opacity
inv_img = ImageOps.invert(blur_img)
blend = Image.blend(inv_img, img, 0.5)

#Adjust the levels to a min,max and gamma values
img = level_image(blend,78,125,0.78)
img.save("sketch.jpg")
