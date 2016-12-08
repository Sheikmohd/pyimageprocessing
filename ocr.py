import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
import pytesser

def process_image(url):
    # image = _get_image(url)
    # image.filter(ImageFilter.SHARPEN)
    # return pytesseract.image_to_string(image)
    print "URL",url
    return pytesser.image_file_to_string(url)


# def _get_image(url):
#     return Image.open(StringIO(requests.get(url).content))
