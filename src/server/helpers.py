from PIL import Image
import numpy as np

def png_to_bmp(png_path, bmp_path):

    img = Image.open(png_path)
    ary = np.array(img)
    print(ary.shape)
    # Split the three channels
    # r,g,b = np.split(ary,3,axis=2)
    # r=r.reshape(-1)
    # g=r.reshape(-1)
    # b=r.reshape(-1)
    #
    # # Standard RGB to grayscale
    # bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2],
    # zip(r,g,b)))
    ary = ary.mean(axis=2)
    # bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((ary > 200).astype(float),255)
    im = Image.fromarray(bitmap.astype(np.uint8))
    im.save(bmp_path)