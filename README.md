# catarc
中国汽车技术研究中心——智能技术展示平台

2019年7-8月



#  目录说明
```
/catarc
|—— .vscode :  vscode的配置文件，且整个项目使用基于项目根目录的相对路径
|—— img :  model模块中调用的图片，eg: peopleCM.jpg 和 peopleGB.jpg。将被 `driveModel.py` 调用    
|—— model :  MVC模式的，M层，model层
        |—— `gymcuModel.py`: 读取**GYMCU（CP210x)温度传感器**的文件              
        |—— `jfModel.py` : 读取**JF11(CH340)传感器**数据的文件            
        |—— `faceModel.py` : 分析驾驶员 是否和 数据库中已存储的面部相   
        |—— `driveModel.py`: 分析图片中驾驶人物的几种状态   
|—— static :  Python 后端flask 框架的静态文件目录，主要存放前端Web相关的代码
        |——  img :  当然存放的Web 图片啦，由于 Flask 框架限制，网页中使用 /static/img/map.png 此类路径。        
|—— templates :  Flask 框架要求将Html 放入templates中
|—— README.md : 说明文档
|—— server.py : 在服务器中运行的文件。

```



# 使用说明

1. 服务器端：在 `catarc` 下运行 服务器端文件 `server.py`

2. 浏览器端：在 浏览器中输入 （http://localhost:5000/index.html)

3. 常见问题
① Linux中，Shell 报错 Permission denied（没有权限允许）

   - linux 下面没有对USB设备的访问权限导致的，所以要执行以下指令

     ```
     sudo chmod 777 /dev/ttyUSB0
     sudo chmod 777 /dev/ttyUSB1
     sudo chmod 777 /dev/ttyUSB2
     ```

   - 或者已经在其他程序代开过，比如重插
   
② Linux中 `img` 文件夹中图片下载失败：

   - 是 `img`  的读写权限可能有问题，改读写权限即可。



# Model文件夹中文件说明

- `gymcuModel.py` 读取温度传感器的模块

  - 在不同电脑上可能要装驱动。Win 和 Linux 串口号(win:'com*', linux:'/dev/*'), 已定义好选择的list，并且做了自动识别是Window 还是 Linux 的判断。
  - 注意要插上**GYMCU温度传感器**才可以使用.
  - 采集频率：可自定义，项目中用每0.5s 一次。

- `jfModel.py` :读取心率检测模块数据的模块

  - 在不同电脑上可能要装驱动。Win 和 Linux 串口号(win:'com*', linux:'/dev/*'), 已定义好选择的list，并且做了自动识别是Window 还是 Linux 的判断。
  - 注意要插上**JF11(CH340)传感器 ** 才可以使用.
  - 采集频率：1次/1.28s

- `faceModel.py` ：分析驾驶员 是否和 数据库中已存储的面部相同

  - 注意要插上**萤石摄像头，并将萤石摄像头联网后**，才可以使用
  - 这是分析的 `img/people.jpg` 图片，该图片模拟摄像头捕获车内驾驶人员的驾驶照片，并利用数据库中的人脸照片（`img/peopleGB.jpg`），进行对比。前期放在一起，后期可以连接数据库

- `driveModel.py` ：分析图片中驾驶人物的几种状态

  - 注意：分析 `img/people.jpg` 图片的驾驶行为。该图片模拟摄像头捕获车内驾驶人员的驾驶照片，在用萤石摄像头捕捉图片到本地后，分析驾驶人员的五项开车行为。

  | 目录               | 分数 |
  | ------------------ | ---- |
  | 是否未系安全带     | 80   |
  | 是否接打电话       | 80   |
  | 是否双手离开方向盘 | 80   |
  | 是否目视前方       | 80   |
  | 是否抽烟           | 80   |



# 后续开发

1. 设计模式：可以优化代码逻辑，调整代码组织方式，方便进行代码量的扩张。

2. 数据库：img 中图片可以优化到数据库中，未来可使用ADC平台的数据库，扩展 **ADC共享出行** 的智能科技。

3. 智能技术：可以内化为自己的算法团队，开展更深入，更广泛的研究。以期将 ADC共享出行 团队打造为 **智能驱动，服务第一** 的国内首屈一指的共享出行服务供应商。

4. 车辆改装：与车厂合作，将智能技术解决方案出售，提供方案解决服务，为数据资源中心主营业务收入 添砖加瓦。

   


# 版权

中国汽车技术研究中心数据资源中心©版权保留
