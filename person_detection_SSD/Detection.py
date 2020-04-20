import numpy as np
import os
import cv2


class Detection:
    def __init__(self):
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]

        my_path = os.path.abspath(os.path.dirname(__file__))

        self.net = cv2.dnn.readNetFromCaffe(os.path.join(my_path, './model/MobileNetSSD_deploy.prototxt.txt'),
                                            os.path.join(my_path, './model/MobileNetSSD_deploy.caffemodel'))

    def detect(self, img):
        (h, w) = img.shape[:2]

        blob = cv2.dnn.blobFromImage(cv2.resize(img, (1280, 720)), 0.007843, (300, 300), 127.5)

        self.net.setInput(blob)

        detections = self.net.forward()

        person_detect_location = []

        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.5:
                # extract the index of the class label from the `detections`,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                box = box.astype("int")

                if idx == 15:
                    person_detect_location.append(box)

        return person_detect_location


if __name__ == '__main__':
    api = Detection()

    img = cv2.imread('city-walk.png')

    detection = api.detect(img)

    for i in detection:
        cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), (255, 255), 2)

    cv2.imshow("Output", img)
    cv2.waitKey(0)
