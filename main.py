from PIL import Image
import os
import io

# 16 tall 9 width to 1 1 or 4 tall 3 width

def limit_img_size(img_filename, img_target_filename, target_filesize, tolerance=5):
    img = img_orig = Image.open(img_filename)

    # Proportion, width is always the bigger dimensino, height is the other one
    width, height = img.size
    aspect = width / height

    try:
        exif = img.info['exif']
        no_exif=False
    except:
        no_exif=True

    if proportions=='0':
        pass

    elif proportions=='1':

        if width > height:

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

        else:

            a = height - width
            a = int(a / 2)
            left = 0
            top = a
            right = width
            bottom = height - a
            img = img.crop((left, top, right, bottom))
            img_orig = img
            width, height = img.size
            aspect = width / height
            print(aspect)

    elif proportions=='2' and (width / height > 1.333333 or height / width > 1.333333):

        if width > height:

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

        else:

            t = aspect
            h2 = (4 * t * height) / 3 # new height
            a = (height - h2) / 2

            left = 0
            top = a
            right = width
            bottom = height - a
            img = img.crop((left, top, right, bottom))
            img_orig = img
            width, height = img.size
            aspect = width / height
            print(aspect)


    elif proportions=='2' and (width / height < 1.333333 or height / width < 1.333333):

        if width > height:

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

        else:

            t = 1 / aspect

            w2 = (3 * t * width) / 4
            b = (width - w2) / 2

            left = b
            top = 0
            right = width - b
            bottom = height
            img = img.crop((left, top, right, bottom))
            img_orig = img
            width, height = img.size
            aspect = width / height
            print(aspect)

    while True:

        with io.BytesIO() as buffer:
            if no_exif==False:
                img.save(buffer, format="JPEG", exif=exif)
                data = buffer.getvalue()
            else:
                img.save(buffer, format="JPEG")
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

size_bytes = input("Enter target size in Kb?")
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
            1000 * int(size_bytes),   # bytes
            tolerance = 5    # percent of what the file may be bigger than target_filesize
        )
