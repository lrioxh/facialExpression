from flask import Flask, request
import os
from model import CNN3
import recognition
import datetime
import random

# model = CNN3()
# model.load_weights('./models/cnn3_best_weights.h5')


def create_uuid(): #生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum


app = Flask(__name__)
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'photo')
#svc_l=joblib.load('SVC_L.pkl')
'''
@app.route('/picrec', methods=['post']) # 上传图片识别
def picrec():
    img_list = request.files['file']
    # HOG特征提取参数
    cell_size = 10
    bin_size = 9
    angle_unit = 360 / bin_size
    X=[]
    global ValidList = []
    for kk in range(len(img_list)):
        x1 = featureExtract(img_list[kk])
        if x1 != -1:
            X.append(x1)
            ValidList.append(kk)
    global Y=svc_l.predict(X)

    return y
get
@app.route('/save', methods=['post'])   # 结果保存数据库
def save():
    APP_ID = '***'
    APP_SECRET = '****'
    ENV = 'test-****'
    ID = request.get_json()['id']
    timeStamp=request.get_json()['timestamp']
    timeStamp=[timeStamp[i] for i in ValidList]
    Y=list(Y)

    db = wxCloud(APP_ID, APP_SECRET, ENV)
    db.collection = 'test'
    if db.query_data(id=ID):
        print(1)
        db.update_data(     #存在则更新
            id=ID,
            timeStamp=timeStamp,
            mood=Y
        )
    else:
        print(0)
        db.add_data(        #不存在则添加
            id=ID,
            timeStamp=timeStamp,
            mood=Y
        )

    return 0
'''
@app.route('/')
def hello():
    return 'hello'

@app.route('/add',methods=['GET','POST'])
def add():
    data=request.get_json()['num']
    return str(data+1)


@app.route('/test', methods=['GET'])
def test():
    x = request.args.get('x')
    return str(float(x)**2)

@app.route('/up_photo', methods=['GET','POST'])
def up_photo():
    img = request.files.get('file')

    filename = create_uuid()+'.'+ img.filename.split('.')[-1]
    img.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    # print(filename)

    # Y = svc_l.predict(X)

    return str(1)


@app.route('/reg', methods=['GET','POST'])
def reg():
    img = request.files.get('file')

    filename = create_uuid()+'.'+ img.filename.split('.')[-1]
    path=os.path.join(app.config['UPLOAD_PATH'], filename)
    img.save(path)
    # print(path)
    recognition.upload_recognition('./photo/'+filename, filename)
    # print(filename)

    # Y = svc_l.predict(X)

    return './output/'+filename

if __name__ == '__main__':
    # recognition.upload_recognition('./photo/2020113000123968.png', '2020113000123968.png')
    app.run(debug=True,
            host='127.0.0.1',
            port=8080
            )