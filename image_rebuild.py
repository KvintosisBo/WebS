import numpy as np
import time
from PIL import Image
from matplotlib import pyplot as plt

def polosa(image, p_width, vertical=True):
    image_array = np.array(image)
    height, width, _ = image_array.shape

    if vertical:
        new_image = np.zeros_like(image_array)
        for i in range(0, height, 2*p_width):
            new_image[i:i+p_width, :] = image_array[i:i+p_width:p_width, :]
        if height % (2*p_width) != 0:
            new_image[-p_width:, :] = image_array[-p_width:, :]
    else:
        new_image = np.zeros_like(image_array)
        for i in range(0, width, 2*p_width):
            new_image[:, i:i+p_width] = image_array[:, i:i+p_width:p_width]
        if width % (2*p_width) != 0:
            new_image[:, -p_width:] = image_array[:, -p_width:]

    return Image.fromarray(new_image.astype('uint8'))


def graf(image):
    colors = np.array(image).reshape(-1, 3)
    plt.figure(figsize=(10, 6))
    plt.hist(colors, bins=256, range=(0, 256), color=['r', 'g', 'b'], label=['Red', 'Green', 'Blue'], edgecolor='none')
    plt.xlabel('Значение цвета')
    plt.ylabel('Частота')
    plt.title('Распределение цветов в изображении')
    plt.legend()

    timestamp = time.time()
    histogram_filename = f'static/histogram_{timestamp}.png'
    plt.savefig(histogram_filename)
    plt.close()

    return histogram_filename

