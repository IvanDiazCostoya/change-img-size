from PIL import Image
import os
import io

# 16 tall 9 width to 1 1 or 4 tall 3 width

def limit_img_size(img_filename, img_target_filename, target_filesize, tolerance=5):
    img = img_orig = Image.open(img_filename)

    # Proportion, width is always the bigger dimensino, height is the other one
    d1, d2 = img.size
    width = max(d1, d2)
    height = min(d1, d2)
    aspect = width / height

    exif = img.info['exif']

    if proportions=='0':
        pass

    elif proportions=='1':

        a = width - height
        a = int(a / 2)
        left = a
        top = 0
        right = width - a
        bottom = height
        img = img.crop((left, top, right, bottom))
        img_orig = img
        width, height = img.size
        aspect = width / height
        print(aspect)

    elif proportions=='2' and aspect > 1.333333:

        t = 1 / aspect
        w2 = (4 * t * width) / 3 # new width
        a = (width - w2) / 2

        left = a
        top = 0
        right = width - a
        bottom = height
        img = img.crop((left, top, right, bottom))
        img_orig = img
        width, height = img.size
        aspect = width / height
        print(aspect)

    elif proportions=='2' and aspect < 1.333333:

        h2 = (3 * aspect * height) / 4
        b = (height - h2) / 2

        left = 0
        top = b
        right = width
        bottom = height - b
        img = img.crop((left, top, right, bottom))
        img_orig = img
        width, height = img.size
        aspect = width / height
        print(aspect)

    while True:

        with io.BytesIO() as buffer:
            img.save(buffer, format="JPEG", exif=exif)
            data = buffer.getvalue()
        filesize = len(data)
        size_deviation = filesize / target_filesize
        print("size: {}; factor: {:.3f}".format(filesize, size_deviation))

        if size_deviation <= (100 + tolerance) / 100:
            # filesize fits
            with open(img_target_filename, "wb") as f:
                f.write(data)
            break

        else:

            # filesize not good enough => adapt width and height
            # use sqrt of deviation since applied both in width and height
            new_width = img.size[0] / size_deviation**0.5
            new_height = new_width / aspect

            # resize from img_orig to not lose quality
            img = img_orig.resize((int(new_width), int(new_height)))

size = input("Enter target size in Kb?")
proportions = input("Enter proportions (0 -> Unchanged, 1 -> 1/1, 2 -> 3/4)")

os.mkdir("new_files")

path = os.getcwd()

tree = os.walk(path)

for d in os.listdir(path):

    if os.path.splitext(d)[1] == ".jpg" or os.path.splitext(d)[1] == ".JPG" or os.path.splitext(d)[1] == ".jpeg" or os.path.splitext(d)[1] == ".JPEG":
        print(d)

        limit_img_size(
            d,   #  input file
            "new_files" + os.sep + d,     #  target file
            1000 * int(size),   # bytes
            tolerance = 5    # percent of what the file may be bigger than target_filesize
        )
