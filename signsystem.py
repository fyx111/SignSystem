import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog

from untitled import *
import numpy as np
from aip import AipFace
from urllib import request
import base64
import cv2
import datetime
import pymysql

APP_ID = '25884575'
API_KEY = 'g3IGO5CNXzmC0UAGCO8BKCz4'
SECRET_KEY = 'GF3KHgTtH9HjmEuGVGoxGGrgnuaKMRGP'
BaiduClient = AipFace(APP_ID, API_KEY, SECRET_KEY)  # 百度人脸识别API账号信息
IMAGE_TYPE = 'BASE64'  # 图像编码方式
GROUP = 'Class1'  # 用户组信息
url = "http://192.168.1.115:8080/?action=snapshot"  # 从推流地址取截图用于opencv处理

def downloadImg():  # 从推流地址取截图用于opencv处理
    global url
    with request.urlopen(url) as f:
        data = f.read()
        img1 = np.frombuffer(data, np.uint8)
        img_cv = cv2.imdecode(img1, cv2.IMREAD_COLOR)
        return img_cv

def transimage():  # 对图片的格式进行转换
    f = open('faceimage.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img

def go_api(image):  # 上传到百度api进行人脸检测
    result = BaiduClient.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP)
    if result['error_msg'] == 'SUCCESS':
        name = result['result']['user_list'][0]['user_id']
        score = result['result']['user_list'][0]['score']
        if score > 85:  # 相似度
            if name == '1913001008':
                StudentID = 1913001008
            return StudentID
        else:
            name = 'Unknow'
            return 0
    if result['error_msg'] == 'pic not has face':
        return 0

database = pymysql.Connect(  # 连接数据库
    host='180.76.158.224',
    port=3306,
    user='fyx',
    passwd='123',
    db='classroom1132',
    charset='utf8'
)

class MyClass(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)
        self.setupUi(self)
        self.timer_camera = QTimer(self)
        self.timer_camera.start(30)
    def slot2(self):#槽函数
        t3 = datetime.datetime.now().weekday()  # 判断周几
        self.label_2.setText("今日已经保存数据！")
        cursor = database.cursor()  # 获取游标
        if t3 == 0:  # 周一
            sql = """insert into summary select date,StudentID,signedin from Monday;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
            sql = """update Monday set signedin=0;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
        elif t3 == 1:  # 周二
            sql = """insert into summary select date,StudentID,signedin from Tuesday;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
            sql = """update Tuesday set signedin=0;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
        elif t3 == 2:  # 周三
            sql = """insert into summary select date,StudentID,signedin from Wednesday;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
            sql = """update Wednesday set signedin=0;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
        elif t3 == 3:  # 周四
            sql = """insert into summary select date,StudentID,signedin from Thursday;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
            sql = """update Thursday set signedin=0;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
        elif t3 == 4:  # 周五
            sql = """insert into summary select date,StudentID,signedin from Friday;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
            sql = """update Friday set signedin=0;"""  # 先保存数据，然后置零
            cursor.execute(sql)  # 执行sql语句
            database.commit()  # 提交到数据库执行
    def slot1(self):
        self.timer_camera.timeout.connect(self.show_single)
    def show_single(self):
        t=datetime.datetime.now().weekday()#判断周几
        t2 = datetime.datetime.now().hour  # 判断时间，目的在于判断第二天是否来临，方便改成“今日还未保存数据！”
        cursor = database.cursor()  # 获取游标
        image = downloadImg()  # 根据路径读取一张图片
        cv2.imwrite('faceimage.jpg', image)  # 拍摄一次照片
        if t2==0:
            self.label_2.setText("今日还未保存数据！")#自动还原
        img = transimage()  # 转换照片格式
        StudentID = go_api(img)  # 将转换了格式的图片上传到百度云
        self.label.setText("未匹配到人脸")
        if StudentID != 0:
            if StudentID == 1913001008:  # 扫到1913001008的人脸
                self.label.setText("识别成功为范艺轩，签到成功！")
                if t == 0:
                    sql = """update Monday set date=curdate(),signedin=1 where StudentID=1913001008"""  # SQL插入语句
                    cursor.execute(sql)  # 执行sql语句
                    database.commit()  # 提交到数据库执行
                elif t == 1:
                    sql = """update Tuesday set date=curdate(),signedin=1 where StudentID=1913001008"""  # SQL插入语句
                    cursor.execute(sql)  # 执行sql语句
                    database.commit()  # 提交到数据库执行
                elif t == 2:
                    sql = """update Wednesday set date=curdate(),signedin=1 where StudentID=1913001008"""  # SQL插入语句
                    cursor.execute(sql)  # 执行sql语句
                    database.commit()  # 提交到数据库执行
                elif t == 3:
                    sql = """update Thursday set date=curdate(),signedin=1 where StudentID=1913001008"""  # SQL插入语句
                    cursor.execute(sql)  # 执行sql语句
                    database.commit()  # 提交到数据库执行
                elif t == 4:
                    sql = """update Friday set date=curdate(),signedin=1 where StudentID=1913001008"""  # SQL插入语句
                    cursor.execute(sql)  # 执行sql语句
                    database.commit()  # 提交到数据库执行
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.showImage.setPixmap(QPixmap.fromImage(image))
if __name__ == '__main__':
    app = QApplication([])
    stats = MyClass()
    stats.show()
    sys.exit(app.exec_())
    database.close()  # 关闭数据库