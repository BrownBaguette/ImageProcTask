#Converted rgb to grayscale using the luminosity method
from PIL import Image
import os

def rgb_to_gray(rgb_image):
    width, height = rgb_image.size
    #Here L for luminance. PIL will now treat it as grayscale and perform accordingly
    gray_image = Image.new('L', (width, height))
    
    for y in range(height):
        for x in range(width):
            r, g, b = rgb_image.getpixel((x, y))
            gray_value = int(0.3 * r + 0.59 * g + 0.11 * b)
            
            gray_image.putpixel((x, y), gray_value)
    
    return gray_image

desktop_path = "C:\\Users\\Hi\\Desktop"
rgb_image = Image.open('bees.jpg')
output_image_path = os.path.join(desktop_path, 'gray3.jpg')
gray_image = rgb_to_gray(rgb_image)
gray_image.save(output_image_path)

