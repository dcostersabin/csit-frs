import cv2
import imutils.paths as paths
import face_recognition
import pickle
import os
from django.http import HttpResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dataset = BASE_DIR + "/static/dataset/"

trained_data = BASE_DIR + "/data/trainedData/encoding1.pickle"


def train():
    print("Deleted Previous Trained Data")
    image_paths = list(paths.list_images(dataset))
    known_encodings = []
    known_names = []

    for (i, imagePath) in enumerate(image_paths):
        print("[INFO] processing image {}/{}".format(i + 1, len(image_paths)))
        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(name)
            print("[INFO] serializing encodings...")
            data = {"encodings": known_encodings, "names": known_names}
            output = open(trained_data, "wb")
            pickle.dump(data, output)
            output.close()
    return True


