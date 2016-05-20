import re
import cv2
import json
import math
import os


datapath = "/Users/mts/Projects/temp/facedata/010"
image_pattern = "^.*(\.jpeg|\.JPG|\.jpg)$"
crop_coef = ((-1.0, -0.7), (1.2 , 0.7))

def get_paths( folder_path ):
    images_path = list()
    img_reg = re.compile(image_pattern)
    for folder, subs, files in os.walk(folder_path):
        for filename in files:
            if img_reg.match(filename) and os.path.exists("%s.json" % os.path.join(folder, filename)):
                images_path.append(os.path.join(folder, filename))
    return images_path


def load_crop( img_path ):
    with open(img_path + ".json") as data_file:
        data = json.load(data_file)
    dot = list()
    for i in range(0, 3):
        y = int(data["landmarks"][str(i)]["y"])
        x = int(data["landmarks"][str(i)]["x"])
        dot.append((y,x))
        del x, y

    angle = math.atan2(dot[0][0] - dot[1][0], dot[0][1] - dot[1][1])
    M = cv2.getRotationMatrix2D((dot[2][0], dot[2][1]), math.degrees(angle), 1)

    rot_dot = list()
    for (y, x) in dot:
        x1 = int(M[0][0] * x + M[0][1] * y + M[0][2])
        y1 = int(M[1][0] * x + M[1][1] * y + M[1][2])
        rot_dot.append((y1, x1))
        del y1, x1

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    rows,cols,sz = img.shape
    del sz
    rot_img = cv2.warpAffine(img, M, (rows,cols))

    h = rot_dot[2][0] - rot_dot[1][0]
    w = rot_dot[0][1] - rot_dot[1][1]
    crop_dot = ((rot_dot[1][0] + int(h * crop_coef[0][0]), rot_dot[1][1] + int(w * crop_coef[0][1])),
                (rot_dot[2][0] + int(h * crop_coef[1][0]), rot_dot[2][1] + int(w * (0.5 + crop_coef[1][1]))))

    crop_img = rot_img[crop_dot[0][0]:crop_dot[1][0], crop_dot[0][1]:crop_dot[1][1]]
    return crop_img


paths = get_paths(datapath)
print "Total %i images" % len(paths)

result_path = datapath + "_result"
if not os.path.exists(result_path):
    os.makedirs(result_path)

counter = 1
for path in paths:
    print "%i/%i : %s" % (counter, len(paths), path)
    counter += 1
    img = load_crop(path)
    cv2.imwrite(os.path.join(result_path, os.path.basename(path)), img)

