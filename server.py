import json
import time
import binascii
import serial
import serial.tools.list_ports
from flask import Flask, render_template

import model.driveModel as drive
import model.faceModel as face
import model.gymcuModel as gymcu
import model.jfModel as jf

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
@app.route('/index')
def index():
    # 初始页面，没有get参数
    return render_template('index.html')


# reuslt 用于在 /start/ 与 /end/ 请求见传递数据
resultgymcu = {}
@app.route('/startGymcu/', methods=['post'])
def startGymcu():
    '''
            gyMcu模块有两种指令模式，1. a5 45 ba, 连续输出。2. a5 15 ba, 查询输出
    '''
    global resultgymcu
    temp = {}
    resultgymcu = {}
    # gymcu,  温度模块
    gyt = gymcu.createSerialGyt()
    if gyt is not None:
        strInput = 'a5 15 ba'
        gyt.write(bytes.fromhex(strInput))
        gymcu.time.sleep(0.3)  # sleep() 与 inWaiting() 最好配对使用
        num = gyt.inWaiting()
        print('gymcu未读取的包：', num)
        temp = {}
        if num:
            # 十六进制显示方法2
            data = str(gymcu.binascii.b2a_hex(gyt.read(9)))[2:-1]
            # to=(25.2, 26.3)
            to = gymcu.getToAndTa(data)
            temp = {'to': to[0]}
        resultgymcu.update(temp)
    return json.dumps(resultgymcu)


# reuslt 用于在 /start/ 与 /end/ 请求见传递数据
resultjf = {}
@app.route('/startJf/', methods=['post'])
def startJf():
    '''
        心率模块的处理函数
    '''
    global resultjf
    resultjf = {}
    temp = {}

    jft = jf.createSerialJF()
    if jft is not None:
        strInput = '8A'
        jft.write(bytes.fromhex(strInput))
        time.sleep(1.28)  # sleep() 与 inWaiting() 最好配对使用
        numOfjf = jft.inWaiting()
        print('jf11未读取的包：', numOfjf)
        if numOfjf:
            # 十六进制显示方法2
            data = str(binascii.b2a_hex(jft.read(76)))[2:-1]
            jfdict = jf.getvalue(data)
            temp = {'acdata': jfdict['acdata'], 'heartRate': jfdict['heartRate'], 'bloodOxygen': jfdict['bloodOxygen'],
                    'diastolicBp': jfdict['diastolicBp'], 'systolicBp': jfdict['systolicBp'], 'microcirculation': jfdict['microcirculation']}
        resultjf.update(temp)
    return json.dumps(resultjf)

@app.route('/end/', methods=['GET'])
def endIndex():
    global resultgymcu
    global resultjf
    result = dict(resultgymcu, **resultjf)
    return json.dumps(result)

@app.route('/ai.html')
def ai():
    # 初始页面，没有get参数
    return render_template('ai.html')

@app.route('/startAi/', methods=['POST'])
def startAi():
    # 用的相对与GUI_FALSK的路径。
    # face.getScore() 返回类似：88.88
    faceScore = '%.2f' % (face.getScore('img/peopleCM.jpg', 'img/peopleGB.jpg'))
    dirveDict = drive.getFiveSocre()
    print('driverDict..................................', dirveDict is None)
    if dirveDict is not None:
        print('dirveDict', dirveDict)
        phoneScore =  '%.2f' % (( 1- dirveDict['cellphone']['score'] )*100 )
        smokeScore = '%.2f' % (( 1- dirveDict['smoke']['score'] )*100)
        seatBeltScore ='%.2f' % ((1- dirveDict['not_buckling_up']['score'])*100)
        lookAheadScore ='%.2f' % (( 1- dirveDict['not_facing_front']['score'])*100)
        handLeavingWheelScore = '%.2f' % ((1- dirveDict['both_hands_leaving_wheel']['score'])*100)
    else:
        phoneScore = 0
        smokeScore = 0
        seatBeltScore = 0
        lookAheadScore = 0
        handLeavingWheelScore = 0
    param = {'faceScore': faceScore, 'phoneScore': phoneScore, 'smokeScore': smokeScore,
             'seatBeltScore': seatBeltScore, 'lookAheadScore': lookAheadScore, 'handLeavingWheelScore': handLeavingWheelScore}
    return json.dumps(param)




if __name__ == '__main__':
    app.run(debug=True)
