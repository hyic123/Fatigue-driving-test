import numpy as np
import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_landmark(file):  # get 68 landmarks of an image

    img = cv2.imread(file)

    rects = detector(img, 0)  # number of faces,it's always 1 in this project
    landmarks = np.matrix([0, 0] for i in range(68))
    for i in range(len(rects)):
        landmarks = np.matrix([[p.x, p.y] for p in predictor(img, rects[i]).parts()])
    return landmarks # return a marix, each row represent a landmark's position

if __name__ == "__main__": # check this function
    file = "01.jpg"
    landmarks = get_landmark(file)
    print(landmarks[1,0])

    img = cv2.imread(file)
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])
        print(idx, pos)
        cv2.circle(img, pos, 1, color=(0, 255, 0))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(idx), pos, font, 0.3, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.namedWindow("img", 2)
    cv2.imshow("img", img)
    cv2.waitKey(0)