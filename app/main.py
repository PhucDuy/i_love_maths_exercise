"""
This module is the main flask application.
"""

from flask import Flask, request, render_template
from blueprints import *
import cv2
import numpy as np
import tensorflow as tf
import re
import mahotas
import base64
import imutils

app = Flask(__name__)
app.secret_key = b'A Super Secret Key'

# YOUR PART: Load model and list out label names
model =
label_names =


app.register_blueprint(home_page)


def parse_image(imgData):
    imgstr = re.search(b"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(imgstr)
    with open("output.jpg", "wb") as file:
        file.write(img_decode)
    return img_decode


def deskew(image, width):
    # YOUR CODE HERE

    return image


def center_extent(image, size):
    # YOUR CODE HERE
    return extent


@app.route("/upload/", methods=["POST"])
def upload_file():
    img_raw = parse_image(request.get_data())
    nparr = np.fromstring(img_raw, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # YOUR PART: convert to gray
    gray =

    # YOUR PART: blur with GaussianBlur (play around with parameters)
    blurred =

    # YOUR PART: edge with adaptiveThreshold (play around with parameters)
    edged =

    # YOUR PART: find contours, remember to input with edged.copy()
    (cnts, _) =

    cnts = sorted([(c, cv2.boundingRect(c)[0])
                   for c in cnts], key=lambda x: x[1])

    math_detect = []

    for (c, _) in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w >= 5 and h > 5:
            roi = edged[y:y+int(1.2*h), x:x+w]
            thresh = roi.copy()

            # YOUR PART: deskew now with size 28
            thresh =

            # YOUR PART: center_extent now with size (28, 28)
            thresh =

            # YOUR PART: normalize and make sure the image has the same shape
            # with the data we used to train the model.
            thresh =
            thresh =
            thresh =

            # Prediction
            predictions = model.predict(thresh)
            digit = int(np.argmax(predictions, axis=1))

            # Detect 1 and /
            if label_names[digit] == "1":
                countt = 0
                for i in range(len(thresh[0][9])):
                    if thresh[0][9][i] > 0:
                        countt += 1
                if countt >= 3:
                    math_detect.append("1")
                else:
                    math_detect.append("/")

            else:
                math_detect.append(label_names[digit])

    def convert_math(math_detect):
        """ To convert label 10, 11, 12 to *, -, +
        """
        for i in range(0, len(math_detect)):
            if math_detect[i] == '10':
                math_detect[i] = '*'
            # YOUR PART: change labels 11 and 12 back to - and *

        return math_detect

    def calculate_string(math_detect):
        math_detect = convert_math(math_detect)
        calculator = ''.join(str(item) for item in math_detect)
        result = calculator
        return result

    result = calculate_string(math_detect)

    return result


@app.route("/calcu/", methods=["POST"])
def calcu():
    val = request.get_data()
    val = str(request.get_data())
    val1 = val[2:-1]

    result = str(eval(val1))
    return result


if __name__ == '__main__':
    app.run(debug=True)
