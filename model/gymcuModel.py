import binascii
import serial
import serial.tools.list_ports
import time


def datastr2datadict(data):
    strings = data.replace(' ', '')
    mydict = {}
    indexList = [x+1 for x in range(int(len(strings)/2))]
    byteList = [strings[x]+strings[x+1]
                for x in range(0, int(len(strings)), 2)]
    mydict.update(zip(indexList, byteList))
    return mydict


def getToAndTa(mydata):
    '''
        function: to print some value of temperature sensor
        data: a data which is Hex, like '5a 5a 45...'
    '''
    def hexstr2decstr(data):
        return int(data.upper(), 16)

    data = datastr2datadict(mydata)
    to = hexstr2decstr(data[5]+data[6])/100
    ta = hexstr2decstr(data[7]+data[8])/100
    return to, ta


def hexShow(argv):
    '''
        : 十六进制显示 方法1
    '''
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
            if 'CP210x' in item[1]:

                port_serial = item[0]
        return port_serial


def createSerialGyt():
    port = findPort()
    if port is None:
        print('Gymeu(CP210x) model can''t be found')
        return None
    else:
        try:
            ser = serial.Serial(port, 115200)
        except Exception :
            ser = None
        finally:
            return  ser       
            
        

# 以下逻辑已写入控制层，在控制层中调用数据
def getTemperature():
    port = findPort()
    if port is None:
        print('The Serial port can''t be found')
        quit()
    else:
        t = serial.Serial(port, 115200)
        print("check which port was really used >", t.port)
        '''
            gyMcu模块有两种指令模式，1. a5 45 ba, 连续输出。2. a5 15 ba, 查询输出
        '''
        strInput = 'a5 15 ba'
        print('Command: ', strInput)

    while True:
        try:
            # 如果输入不是十六进制数据--
            n = t.write(bytes.fromhex(strInput))
        except:
            # --则将其作为字符串输出
            n = t.write(bytes(strInput, encoding='utf-8'))

        print(n)
        time.sleep(0.3)  # sleep() 与 inWaiting() 最好配对使用
        num = t.inWaiting()
        print('未读取的包：', num)

        if num:
            # 十六进制显示方法2
            data = str(binascii.b2a_hex(t.read(9)))[2:-1]
            print('data', data)
            print(getToAndTa(data))

 
    

if __name__ == '__main__':
    getTemperature()
