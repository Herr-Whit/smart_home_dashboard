from PIL import Image
import numpy as np

def png_to_bmp(png_path, bmp_path):
    img = Image.open(png_path)
    ary = np.array(img)

    ary = ary.mean(axis=2)

    bitmap = np.dot((ary > 200).astype(float),255)
    im = Image.fromarray(bitmap.astype(np.uint8))
    im.save(bmp_path)
    return bmp_path