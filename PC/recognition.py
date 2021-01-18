import os
import cv2
import numpy as np
from utils import index2emotion, expression_analysis, cv2_img_add_text
from flask import Flask, request
import datetime
import random
import tensorflow as tf
import keras
import base64

graph = tf.get_default_graph()
sess = keras.backend.get_session()

from model import CNN3
model = CNN3()
model.load_weights('./models/cnn3_best_weights.h5')
app = Flask(__name__)
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'photo')


def create_uuid(): #生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum


def face_detect(img_path):
    """
    检测测试图片的人脸
    :param img_path: 图片的完整路径
    :return:
    """
    face_cascade = cv2.CascadeClassifier('./dataset/params/haarcascade_frontalface_alt.xml')
    img = cv2.imread(img_path)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(30, 30)
    )
    return img, img_gray, faces


def generate_faces(face_img, img_size=48):
    """
    将探测到的人脸进行增广
    :param face_img: 灰度化的单个人脸图
    :param img_size: 目标图片大小
    :return:
    """
    face_img = face_img / 255.
    face_img = cv2.resize(face_img, (img_size, img_size), interpolation=cv2.INTER_LINEAR)
    resized_images = list()
    resized_images.append(face_img[:, :])
    resized_images.append(face_img[2:45, :])
    resized_images.append(cv2.flip(face_img[:, :], 1))
    # resized_images.append(cv2.flip(face_img[2], 1))
    # resized_images.append(cv2.flip(face_img[3], 1))
    # resized_images.append(cv2.flip(face_img[4], 1))
    resized_images.append(face_img[0:45, 0:45])
    resized_images.append(face_img[2:47, 0:45])
    resized_images.append(face_img[2:47, 2:47])

    for i in range(len(resized_images)):
        resized_images[i] = cv2.resize(resized_images[i], (img_size, img_size))
        resized_images[i] = np.expand_dims(resized_images[i], axis=-1)
    resized_images = np.array(resized_images)
    return resized_images


def predict_expression(img_path, model,filename):
    global graph, sess
    border_color = (0, 0, 0)  # 黑框框
    font_color = (255, 255, 255)  # 白字字
    img, img_gray, faces = face_detect(img_path)
    if len(faces) == 0:
        return 'no', [0, 0, 0, 0, 0, 0, 0, 0]
    # 遍历每一个脸
    emotions = []
    result_possibilitys = []
    for (x, y, w, h) in faces:
        face_img_gray = img_gray[y:y + h + 10, x:x + w + 10]
        faces_img_gray = generate_faces(face_img_gray)
        # 预测结果线性加权
        with sess.as_default():
            with graph.as_default():
                results = model.predict(faces_img_gray)
        result_sum = np.sum(results, axis=0).reshape(-1)
        label_index = np.argmax(result_sum, axis=0)
        emotion = index2emotion(label_index, 'en')
        cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), border_color, thickness=2)
        img = cv2_img_add_text(img, emotion, x + 5, y + 5, font_color, int(w*0.25)+15)
        emotions.append(emotion)
        result_possibilitys.append(result_sum)
    if not os.path.exists("./output"):
        os.makedirs("./output")
    cv2.imwrite('./output/'+filename, img)
    with open('./output/'+filename, 'rb') as f:
        img_data = f.read()
        image_base64 = str(base64.b64encode(img_data), encoding='utf-8')
    return image_base64, emotions[0], result_possibilitys[0]

# def upload_recognition(path,name):
#     predict_expression(path, model, name)
#     return 0

@app.route('/reg', methods=['GET','POST'])
def reg():
    img = request.files.get('file')

    filename = create_uuid()+'.'+ img.filename.split('.')[-1]
    path=os.path.join(app.config['UPLOAD_PATH'], filename)
    img.save(path)
    # print(path)
    b64=predict_expression('./photo/'+filename,model, filename)[0]
    # print(filename)
    print(b64)

    return b64

# filename='2020113000131090.jpg'
# upload_recognition('./photo/' + filename, filename)

# if __name__ == '__main__':
#     filename='2020113000131090.jpg'
#     upload_recognition('./photo/' + filename, filename)
#     # predict_expression('./faces.jpg', model,'res.png')
if __name__ == '__main__':
    # recognition.upload_recognition('./photo/2020113000123968.png', '2020113000123968.png')
    app.run(debug=True,
            host='127.0.0.1',
            port=8080
            )