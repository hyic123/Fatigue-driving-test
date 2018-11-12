from get_landmark import get_landmark
import numpy as np
import os

prefix1 = "/home/chenyangdong/dip/picture/dataset_picture/"
prefix2 = "/home/chenyangdong/dip/point/"


for i in range(30):
    suffix = ""
    suffix += "U"
    suffix += "%02d" % (i + 1)
    folder = prefix2 + suffix+"/"
    if not os.path.exists(folder):
        os.mkdir(folder)
    print("%02d U" % i)
    for j in range(12):
        print("%02d V" % j)
        suffix = ""
        suffix += "U"
        suffix += "%02d" % (i+1)
        suffix += "/V"
        suffix += "%02d" % (j+1)
        suffix += "/"
        folder = prefix2+suffix
        if not os.path.exists(folder):
            os.mkdir(folder)

        cur = 1
        s = "%02d" % cur
        filename = prefix1 + suffix + s + ".jpg"
        print(filename)
        # get landmarks from every image
        while os.path.exists(filename):
            try:
                landmarks = get_landmark(filename)
                outfile = prefix2 + suffix + s + ".txt"
                print(cur)
                cur += 1
                s = "%02d" % cur
                filename = prefix1 + suffix + s + ".jpg"
                with open(outfile, 'w') as f:
                    for k in range(68):
                        print("%d %d" % (landmarks[k,0], landmarks[k,1]), file=f)
            except:
                cur += 1
                s = "%02d" % cur
                filename = prefix1 + suffix + s + ".jpg"
                continue

