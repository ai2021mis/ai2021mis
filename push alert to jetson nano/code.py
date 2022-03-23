import io
import PIL
import requests
import numpy as np
import matplotlib.pylab as plt
import cv2
import os
import datetime
import base64

host_name = 'https://42a6-111-83-174-161.ngrok.io'
upload_message_url = host_name + '/api/yolo/'
username = 'user01'
password = 'user01'


def push_message(title, image):
    data = {
        'title': title,
        'image': image,
        'alert': 1,
        'timestamp': time_now(),
        'description': 'No helmet alert',
          }
    aaa = requests.post(upload_message_url, data=data, auth=(username, password))
    print(aaa)

def time_now():
    time = datetime.datetime.now()
    time = time.strftime("%Y/%m/%d %H:%M:%S")
    return time


def image_process(img_url):
    """ Turn image to numpy """
    img_numpy = cv2.imread(img_url)

    """ Turn numpy to bytes"""

    img_numpy_bytes = base64.b64encode(cv2.imencode('.jpg', img_numpy)[1]).decode()
    print(img_numpy_bytes[:100])
    print(type(img_numpy_bytes))
    img_shape = str(img_numpy.shape)

    """ Push message to api """
    img_numpy_toStr = img_numpy_bytes

    return img_numpy_toStr, img_shape


def main():

    """ Turn image to numpy """

    img_numpy = cv2.imread('./test.jpg')

    """ Turn numpy to bytes"""

    img_numpy_bytes = base64.b64encode(cv2.imencode('.jpg', img_numpy)[1]).decode()
    print(img_numpy_bytes[:100])
    print(type(img_numpy_bytes))
    img_shape = str(img_numpy.shape)

    """ Push message to api """
    img_numpy_toStr = img_numpy_bytes
    print('A:', img_numpy_toStr[:100])
    print(type(img_numpy_toStr))

    """ Receive message from api  """
    img_numpy_BytesToNumpy = base64.b64decode(img_numpy_toStr)
    print(img_numpy_BytesToNumpy[:100])
    print(type(img_numpy_BytesToNumpy))

    """ Convert message to Numpy"""

    img_numpy_BytesToNumpy = np.frombuffer(img_numpy_BytesToNumpy, dtype=np.uint8)


    """ Show image """
    # plt.imshow(img_numpy_BytesToNumpy)
    # plt.show()

    """ Save image to """
    directory = os.getcwd()
    directory = os.path.join(directory, 'test_result')
    print(directory)


    cv2_img = cv2.imdecode(img_numpy_BytesToNumpy, flags=1)
    cv2_path = os.path.join(directory, 'out_CV2.jpg')
    cv2.imwrite(cv2_path, cv2_img)


if __name__ == '__main__':
    # main()
    img_url = './test.jpg'
    img, img_shape = image_process(img_url)
    alert_name = input("AlertName")
    alert_name = alert_name + '.jpg'
    push_message(alert_name, img)
    print("Done")