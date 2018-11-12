import os
import math


def get_marks(filename):
    with open(filename) as f:
        lines = f.readlines()
    ret = list()
    for line in lines:
        tmp = line.split()
        ret.append((int(tmp[0]), int(tmp[1])))
    return ret


def get_point(mat, idx):
    return mat[idx, 0], mat[idx, 1]


def get_useful(landmarks):
    """
        00.鼻尖 30
        01.鼻根 27
        02.下巴 8
        03.左眼外角 36
        04.   内角 39
        05.   眼球 37 38 40 41
        09.右眼外角 45
        10.   内角 42
        11.   眼球 43 44 46 47
        15.嘴中心 66
        16.嘴左角 48
        17.嘴右角 54
        18.嘴顶端 51
        19.嘴底端 57
        20.左脸最外 0
        21.右脸最外 16
        22.鼻梁 28
    """
    mapping = [30, 27, 8, 36, 39, 37, 38, 40, 41, 45, 42, 43, 44, 46, 47, 66, 48, 54, 51, 57, 0, 16, 28]
    tmp = list()
    for i in range(len(mapping)):
        tmp.append(landmarks[mapping[i]])
    return tmp


# calc standard deviation
def get_std(data):
    mean = (sum(data) * 1.0)/len(data)
    len_data = len(data)
    ret = 0
    for it in range(len_data):
        ret = ret + (data[it] - mean)**2
    return math.sqrt((ret*1.0)/len_data)


def get_range(data):
    max = -500000
    min = 500000
    len_data = len(data)
    for it in range(len_data):
        if data[it] < min:
            min = data[it]
        elif data[it] >max :
            max = data[it]
    return (max-min)


def get_mouth_height_std(data):
    mouth_height= list()
    for it in data:
        mouth_height.append(it[19][1] - it[18][1])
    return get_std(mouth_height)*1.0

def get_eye_height_std(data):
    eye_height = list()
    for it in data:        
        lefteye_height = ((it[7][1] + it[8][1]) - (it[5][1] + it[6][1])) / 2
        righteye_height = ((it[13][1] + it[14][1]) - (it[11][1] + it[12][1])) / 2
        eye_height.append((lefteye_height+righteye_height) / 2)
    return get_std(eye_height)


def get_mouth_height_range(data):
    mouth_height = list()
    for it in data:
        mouth_height.append(it[19][1] - it[18][1])
    return get_range(mouth_height)


def get_eye_height_range(data):
    eye_height = list()
    for it in data:
        lefteye_height = ((it[7][1] + it[8][1]) - (it[5][1] + it[6][1])) / 2
        righteye_height = ((it[13][1] + it[14][1]) - (it[11][1] + it[12][1])) / 2
        eye_height.append((lefteye_height + righteye_height) / 2)
    return get_range(eye_height)

def get_lean_with_nose(data):
    ret = list()
    for it in data:  # 鼻跟到鼻梁和鼻尖距离的比值
        l1 = it[22][1] - it[1][1]
        l2 = it[0][1] - it[1][1]
        ret.append((l1**2)/(l2**2))
    return get_std(ret)

def get_lean_with_face(data):
    ret = list()
    for it in data:  # 脸的宽高之比
        l1 = it[21][0] - it[20][0]
        l2 = it[2][1] - (it[21][1] + it[20][1]) / 2
        ret.append((l2 ** 2) / (l1 ** 2))
    return get_std(ret)

def get_turn_with_eye(data):
    ret = list()
    for it in data:  # 两眼内角距离和外角距离比
        l1 = it[10][0]- it[4][0]
        l2 = it[9][0]- it[3][0]
        ret.append((l1 ** 2) / (l2 ** 2))
    return get_std(ret)

def get_mouth_height_num(data):
    mouth_height = list()
    for it in data:
        t = it[19][1] - it[18][1]
        t -= 30
        if t<0:
            t = 0
        mouth_height.append(t)
    return get_std(mouth_height) * 1.0


def get_eye_height_num(data):
    eye_height = list()
    for it in data:
        lefteye_height = ((it[7][1] + it[8][1]) - (it[5][1] + it[6][1])) / 2
        righteye_height = ((it[13][1] + it[14][1]) - (it[11][1] + it[12][1])) / 2
        eye_height.append((lefteye_height+righteye_height) / 2)
    ret = 0
    for it in eye_height:
        if it <= 4:
            ret = ret + 1
    return ret

def get_mouth_len(data):
    ret = list()
    for it in data:
        mouth_width = it[17][0]-it[16][0]
        face_width = it[21][0] - it[20][0]
        ret.append((face_width**2)/(mouth_width**2))
    return sum(ret)/len(ret)

def get_feature(dirct):  # get feature of a set of image in directory dir

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
        landmarks = get_marks(filename)
        if (len(landmarks) >= 66):
            fea_set.append(get_useful(landmarks))

        cur += 1
        s = "%02d" % cur
        filename = dirct + s + ".txt"

        while (cur < 64) and (not os.path.exists(filename)):
            cur += 1
            s = "%02d" % cur
            filename = dirct + s + ".txt"

    # calc mean
    length = len(fea_set)


#    face_width = fea_all[21][0] - fea_all[20][0]
#    face_height = fea_all[2][1] - (fea_all[21][1] + fea_all[20][1]) / 2
#    mouth_width = fea_all[17][0] - fea_all[16][0]
#    mouth_height = fea_all[19][1] - fea_all[18][1]
#    lefteye_width = fea_all[4][0] - fea_all[3][0]
#    lefteye_height = ((fea_all[7][1] + fea_all[8][1]) - (fea_all[5][1] + fea_all[6][1])) / 2
#    righteye_width = fea_all[9][0] - fea_all[10][0]
#    righteye_height = ((fea_all[13][1] + fea_all[14][1]) - (fea_all[11][1] + fea_all[12][1])) / 2



    fea = list()
    yawn_fea = list()
    yawn_fea.append(get_mouth_height_std(fea_set))
    #yawn_fea.append(get_mouth_height_range(fea_set))
    fea.append(get_mouth_height_std(fea_set))
    fea.append(get_eye_height_std(fea_set))
    #fea.append(get_mouth_height_range(fea_set))
    #fea.append(get_eye_height_range(fea_set))
    #fea.append(get_lean_with_nose(fea_set))
    #fea.append(get_lean_with_face(fea_set))
    #fea.append(get_turn_with_eye(fea_set))
    #fea.append(get_mouth_height_num(fea_set))
    fea.append(get_eye_height_num(fea_set))
    #fea.append(get_mouth_len(fea_set))

    return fea, yawn_fea

if __name__ == "__main__":
    print(get_feature("/home/chenyangdong/dip/point/U27/V10/"))
