from PIL import Image
from urllib.request import urlopen


def create_image(images_url, filename):
    img_file_1 = images_url[0]
    img_file_2 = images_url[1]
    img_file_3 = images_url[2]
    img_file_4 = images_url[3]

    im_1 = Image.open(urlopen(img_file_1))
    im_2 = Image.open(urlopen(img_file_2))
    im_3 = Image.open(urlopen(img_file_3))
    im_4 = Image.open(urlopen(img_file_4))
    im_1 = im_1.resize((500, 300))
    im_2 = im_2.resize((500, 300))
    im_3 = im_3.resize((500, 300))
    im_4 = im_4.resize((500, 300))
    new_image = Image.new('RGB', (2 * im_1.size[0], 2 * im_1.size[1]), (300, 300, 300))
    new_image.paste(im_1, (0, 0))
    new_image.paste(im_2, (im_1.size[0], 0))
    new_image.paste(im_3, (0, im_1.size[1]))
    new_image.paste(im_4, (im_1.size[0], im_1.size[1]))
    new_image.save(f'{filename}.jpg', 'JPEG')


def blender(url1, url2, filename):
    image1 = Image.open(urlopen(url1))
    image2 = Image.open(urlopen(url2))
    if image1.size != image2.size:
        image1 = image1.resize(image2.size)

    if image1.mode != image2.mode:
        image1 = image1.convert(image2.mode)

    blend_factor = 0.5
    blended_image = Image.blend(image1, image2, blend_factor)
    blended_image.save(filename)

