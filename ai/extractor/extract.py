import os

import cv2
from urllib.request import urlopen
import numpy

from helpers.envs.ai_envs import AIEnvs


class Extractor:

    def _contours(self, image):
        image = self.__url_to_image(image)
        original = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        dilate = cv2.dilate(thresh, kernel, iterations=1)

        # Find contours, obtain bounding box coordinates, and extract ROI
        contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        list_of_contours = contours[0] if len(contours) == 2 else contours[1]
        return original, image, list_of_contours

    def extract(self, data_list):
        image_number = 0
        for image in data_list:
            original, new_image, contours = self._contours(image=image.get('image'))
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(new_image, (x, y), (x + w, y + h), (36, 255, 12), 2)
                extracted_image = original[y:y + h, x:x + w]
                if extracted_image.shape[1] > 200:
                    cv2.imwrite("extracted_image{}.png".format(image_number), extracted_image)
                    os.remove(AIEnvs.BASE_IMAGE_URL + f'\extracted_image{image_number}.png')
                image_number += 1

    @staticmethod
    def __url_to_image(url, readFlag=cv2.IMREAD_COLOR):
        resp = urlopen(url)
        image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, readFlag)

        # return the image
        return image
