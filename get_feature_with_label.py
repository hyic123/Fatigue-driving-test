import os
import get_feature

def get_labeled(u,v): #0 normal 1 yawn 2 fatigue
    label_path = "F:\sztx\dip/picture/dataset.csv"
    data_path = "F:\sztx\dip/point/"
    data_path += "U%02d/V%02d/" % (u,v)
    with open(label_path) as f:
        lines = f.readlines()
        line = lines[12*(u-1) + v]
        label = line.split(',')[6]
        label = label.strip("\n")
    feature,yawn_feature = get_feature.get_feature(data_path)
    return feature, yawn_feature, label



if __name__ == "__main__":
    print(get_labeled(1,2))