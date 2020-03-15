import os


import cv2
from users.models import Employees

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = BASE_DIR + '/static/dataset/'
FACE_CASCADE = cv2.CascadeClassifier(BASE_DIR + '/data/haarcascades/haarcascade_frontalface_default.xml')


def create_dir(name):
    try:
        os.mkdir(path + str(name))
        return True
    except FileExistsError:
        return False


def delete_dir(name):
    try:
        os.removedirs(path + str(name))
        return True
    except FileNotFoundError:
        return False


def capture_image(user_id, mode):
    users = Employees.objects.filter(id=user_id).get()
    user_path = users.name + '__id__' + str(users.id)
    if mode == 0:
        sample = 0
    elif mode == 1:
        no_files = len([name for name in os.listdir(path + '' + user_path) if
                        os.path.isfile(os.path.join(path + '' + user_path, name))])
        sample = no_files

    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        frame = img.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sample = sample + 1
            cv2.imwrite(path + str(user_path) + '/' + str(sample) + '.jpg', gray[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (150, 255, 0), 2)
            cv2.waitKey(100)

        cv2.imshow("Capture Sample For Training", img)
        cv2.waitKey(1)
        if mode == 0:
            if sample > 60:
                break
        elif mode == 1:
            if sample > (no_files + 30):
                break

    cap.release()
    cv2.destroyAllWindows()
    users.data_status = True
    users.save()
    return True
