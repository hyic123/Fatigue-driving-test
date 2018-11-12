from get_feature_with_label import get_labeled
from sklearn import svm
import numpy as np


def get_data(u):
    X1 = list()
    X2 = list()
    y = list()
    for i in range(30):
        if i == u - 1:
            continue
        for j in range(12):
            t1, t2, t3 = get_labeled(i + 1, j + 1)
            X1.append(t1)
            X2.append(t2)
            y.append(t3)
    return X1, X2, y


def train(u):  # train without uth people
    X, t, y = get_data(u)
    clf = svm.SVC()
    clf.fit(X, y)
    return clf


def train_yawn(u):
    X1, X2, y = get_data(u)
    y_yawn = list()
    for it in y:
        if it == "yawn":
            y_yawn.append("yawn")
        else:
            y_yawn.append("not")
    clf_yawn = svm.SVC()
    clf_yawn.fit(X2, y_yawn)
    X_2 = list()
    y_2 = list()
    for i in range(len(X1)):
        if y[i] != "yawn":
            X_2.append(X1[i])
            y_2.append(y[i])
    clf_2 = svm.SVC()
    clf_2.fit(X_2, y_2)
    return clf_yawn, clf_2


if __name__ == "__main__":
    cnty = 0
    sum = 0

    """
    for stu in range(30):
        clf = train(stu+1)
        cnt = 0
        for i in range(12):
            fea, fea_yawn, label = get_labeled(stu+1,i+1)
            pre = clf.predict(np.array(fea).reshape(1, -1))
            print(pre, label)
            if pre == label:
                cnt += 1
            if pre != label and label == "yawn":
                cnty += 1
        print(cnt/12)
        sum = sum + cnt/12
        print(stu, cnty)
    print (sum/30)
    """
    for stu in range(30):
        clf_1, clf_2 = train_yawn(stu + 1)
        cnt = 0
        for i in range(12):
            fea, fea_yawn, label = get_labeled(stu + 1, i + 1)
            pre = clf_1.predict(np.array(fea_yawn).reshape(1, -1))
            if pre != "yawn":
                pre = clf_2.predict(np.array(fea).reshape(1, -1))
            print(pre, label)
            if pre == label:
                cnt += 1
            if pre != label and label == "yawn":
                cnty += 1
        print(cnt / 12)
        sum = sum + cnt / 12
        print(stu, cnty)
    print(sum / 30)
    #"""
    #c1, c2 = train_yawn(27)
    #l1, l2, l = get_labeled(27, 11)
    #print(l2)
    #print(c1.predict(np.array([0.7]).reshape(1, -1)))