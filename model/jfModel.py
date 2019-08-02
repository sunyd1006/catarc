import binascii
import serial
import serial.tools.list_ports
import time

'''
    JF11模块：这是检测的
'''


def datastr2datadict(data):
    strings = data.replace(' ', '')
    mydict = {}
    indexList = [x+1 for x in range(int(len(strings)/2))]
    byteList = [strings[x]+strings[x+1]
                for x in range(0, int(len(strings)), 2)]
    mydict.update(zip(indexList, byteList))
    return mydict


def getvalue(mydata):
    '''
        function: to print some value of human's key points.
        data: a data which is Hex, like 'ff 0c 0c ...'
    '''
    def hexstr2decstr(data):
        return int(data.upper(), 16)
    data = datastr2datadict(mydata)
    acdata = []
    for i in range(2, 66):
        acdata.append(hexstr2decstr(data[i]))

    heartRate = hexstr2decstr(data[66])
    bloodOxygen = hexstr2decstr(data[67])
    diastolicBp = hexstr2decstr(data[68])
    systolicBp = hexstr2decstr(data[72])
    microcirculation = hexstr2decstr(data[73])

    return {'acdata': acdata, 'heartRate': heartRate, 'bloodOxygen': bloodOxygen, 'diastolicBp': diastolicBp, 'systolicBp': systolicBp, 'microcirculation': microcirculation}

#  十六进制显示 方法1


def hexShow(argv):
    try:
        result = ''
        hLen = len(argv)
        for i in range(hLen):
            hvol = argv[i]
            hhex = '%02x' % hvol
            result += hhex+' '
        print('hexShow:', result)
    except:
        pass


def findPort():
    '''
        return like 'COM*' or '/dev/ttyS*'
        win: find port like 'COM*'
        linux: find port like '/dev/ttyS*'
    '''
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        return None
    else:
        # port_serial 默认是None, 若对应的模块插入，才返回端口号。
        port_serial = None
        # item like ['com4', Silicon Las Cp210x Usb to UART Bridge(COM4)', 'USB VID:PID=10C4:EA60 SER=0001 LOCATION=1-3']
        for item in port_list:
            if 'CH340' in item[1]:
                port_serial = item[0]
        return port_serial


def createSerialJF():
    port = findPort()
    if port is None:
        print('JF11(CH340) can''t be found!')
    else:
        try:
            ser = serial.Serial(port, 38400)
        except Exception as e:
            print('Open ',port, e )
            ser = None
        finally:
            return ser


if __name__ == "__main__":
    t = createSerialJF()
    if t is not None:
        strInput = '8A'
        while True:
            n = t.write(bytes.fromhex(strInput))

            print(n)
            time.sleep(1.28)  # sleep() 与 inWaiting() 最好配对使用
            num = t.inWaiting()
            print('未读取的包：', num)

            if num:
                # 十六进制显示方法2
                data = str(binascii.b2a_hex(t.read(76)))[2:-1]
                # 输出格式
                print(getvalue(data))

            # 实际上不执行，强制关停后就没执行了。
            t.write(bytes.fromhex('00'))
