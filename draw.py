import get_feature
import matplotlib.pyplot as plt
import os


def get_point(dirct):
    cur = 1
    s = "%02d" % cur
    filename = dirct + s + ".txt"
    fea_set = []
    while not os.path.exists(filename):
        cur += 1
        s = "%02d" % cur
        filename = dirct + s + ".txt"

    # get landmarks from every image
    while os.path.exists(filename):
        landmarks = get_feature.get_marks(filename)
        if (len(landmarks) >= 66):
            fea_set.append(get_feature.get_useful(landmarks))

        cur += 1
        s = "%02d" % cur
        filename = dirct + s + ".txt"

        while (cur < 64) and (not os.path.exists(filename)):
            cur += 1
            s = "%02d" % cur
            filename = dirct + s + ".txt"
    return fea_set

def get_mouth_height(data):
    mouth_height= list()
    for it in data:
        mouth_height.append(it[19][1] - it[18][1])
    return mouth_height

def get_eye_height(data):
    eye_height = list()
    for it in data:
        lefteye_height = ((it[7][1] + it[8][1]) - (it[5][1] + it[6][1])) / 2
        righteye_height = ((it[13][1] + it[14][1]) - (it[11][1] + it[12][1])) / 2
        eye_height.append((lefteye_height+righteye_height) / 2)
    return eye_height


def get_lean_with_nose(data):
    ret = list()
    for it in data:  # 鼻跟到鼻梁和鼻尖距离的比值
        l1 = it[22][1] - it[1][1]
        l2 = it[0][1] - it[1][1]
        ret.append((l1**2)/(l2**2))
    return ret

def get_lean_with_face(data):
    ret = list()
    for it in data:  # 脸的宽高之比
        l1 = it[21][0] - it[20][0]
        l2 = it[2][1] - (it[21][1] + it[20][1]) / 2
        ret.append((l2 ** 2) / (l1 ** 2))
    return ret

def get_turn_with_eye(data):
    ret = list()
    for it in data:  # 两眼内角距离和外角距离比
        l1 = it[10][0]- it[4][0]
        l2 = it[9][0]- it[3][0]
        ret.append((l1 ** 2) / (l2 ** 2))
    return ret


def get_mouth_len(data):
    ret = list()
    for it in data:
        mouth_width = it[17][0]-it[16][0]
        face_width = it[21][0] - it[20][0]
        ret.append((face_width**2)/(mouth_width**2))
    return sum(ret)/len(ret)

def draw(data, ttl):
    i = 1
    x = list()
    for it in data:
        x.append(i)
        i += 1
    plt.figure()
    print(x, data)
    plt.plot(x, data)
    #plt.ylim(0,8)
    #plt.axhline(4,linestyle='-.', color = 'r')
    plt.xlabel("image")
    plt.ylabel("value")
    plt.title(ttl)
    #plt.show()
    plt.savefig("img/"+ttl+".png")

if __name__ == "__main__":
    feature = get_point("F:\sztx\dip\point\\U28\V07\\")
    print(feature)
    draw(get_turn_with_eye(feature), "eye-fatigue")