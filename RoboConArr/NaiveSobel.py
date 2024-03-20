from PIL import Image
import numpy as np
import os



def custom_box_blur(image, kernel):
    width, height = image.size
    blurred_image = Image.new("RGB", (width, height))
    blurred_pixels = blurred_image.load()
    img_array = np.array(image)

    for y in range(height):
        for x in range(width):
            x_min = max(0, x - len(kernel) // 2)
            x_max = min(width - 1, x + len(kernel) // 2)
            y_min = max(0, y - len(kernel) // 2)
            y_max = min(height - 1, y + len(kernel) // 2)

            total_r, total_g, total_b = 0, 0, 0

            for yy in range(y_min, y_max + 1):
                for xx in range(x_min, x_max + 1):
                    r, g, b = img_array[yy, xx]
                    kernel_value = kernel[yy - y_min][xx - x_min]  # Access kernel value
                    total_r += r * kernel_value
                    total_g += g * kernel_value
                    total_b += b * kernel_value

            avg_r = total_r 
            avg_g = total_g 
            avg_b = total_b 

            blurred_pixels[x, y] = (avg_r, avg_g, avg_b)

    return blurred_image

#play around with the existing kernel values but orient it differently for different angles of sobel.
custom_kernel = [
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
]


desktop_path = "C:\\Users\\Hi\\Desktop"
input_image_path = os.path.join('flower.jpg')
output_image_path = os.path.join(desktop_path, 'Blurred_Trial4.jpg')

#self explanatory part.
input_image = Image.open(input_image_path)
blurred_image = custom_box_blur(input_image, custom_kernel)
blurred_image.save(output_image_path)

