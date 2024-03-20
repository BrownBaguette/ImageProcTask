#Following code blurs a given input image using the mean filter(box blur method). The radius can be controlled accordingly to achieve required
#smoothness of the input image. Unfortunately could not implement fixes for edge effects. Code should run well for a reasonable value of
#radius.

from PIL import Image
import numpy as np
import os

def box_blur(image, radius):
    #storing the dimensions of the image , that it returns as a tuple respectively into the two variables.
    width, height = image.size

    #creating a new blank image with RGB color channel and image dimensions
    blurred_image = Image.new("RGB", (width, height))

    # loads the pixel data of the input image image, allowing direct access to individual pixel values. Kind of like a 2D array.
    #for indexing of the 2d array refer to my sticky notes.
    blurred_pixels = blurred_image.load()

    # Convert image to numpy array for easier manipulation. Gives a 3d array width x heigth x channels.
    img_array = np.array(image)


    #height and width are not inclusive in the range. Range begins from 0.
    for y in range(height):
        for x in range(width):
            # Defining the region of interest. Not perfectly accurate near the edges. Edges average is not perfect using the kernel radius
            #but approximates pretty decently.
            x_min = max(0, x - radius)
            x_max = min(width - 1, x + radius)
            y_min = max(0, y - radius)
            y_max = min(height - 1, y + radius)

            # Accumulate the pixel values within the region of interest
            total_r, total_g, total_b = 0, 0, 0
            num_pixels = 0
            for yy in range(y_min, y_max + 1):
                for xx in range(x_min, x_max + 1):
                    r, g, b = img_array[yy, xx]
                    total_r += r
                    total_g += g
                    total_b += b
                    num_pixels += 1

            # Compute the average pixel value within the region of interest
            avg_r = total_r // num_pixels
            avg_g = total_g // num_pixels
            avg_b = total_b // num_pixels

            # Set the blurred pixel value in the new image
            blurred_pixels[x, y] = (avg_r, avg_g, avg_b)

    return blurred_image



#Setting up a path to the desktop as initially didn't use relative path.
desktop_path = "C:\\Users\\Hi\\Desktop"

#As the image is in same folder as code no need to explicitly mention its path. Can just use relative path ie accessing by name as they are in
#the same folder. 
input_image_path = os.path.join('hills.jpg')

#In case the file does not exist , the code snippet does not make a new file but rather just constructs the path as a string  akin to window's
#string when using the address bar.
output_image_path = os.path.join(desktop_path, 'Blurred_Trial1.jpg')


#setting up the radius for box blur here. Tells how many pixels around each pixel will be used for averaging.
#Higher radius means more smoothing. Although the edges may be a bit janky. A close second will be use smaller radius multiple times.
radius = 3

#self explanatory part.
input_image = Image.open(input_image_path)
blurred_image = box_blur(input_image, radius)
blurred_image.save(output_image_path)
