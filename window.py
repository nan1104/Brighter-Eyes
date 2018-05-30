#coding:utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import camera_shooting
import sys
import video

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint) #隐藏边框
        self.closebtn = QPushButton(self) #定义关闭按钮
        self.closebtn.setIcon(QIcon("./src/close.png"))
        self.closebtn.clicked.connect(self.close)
        self.closebtn.move(520,0)
        self.subbtn = QPushButton(self)  # 定义关闭按钮
        self.subbtn.setIcon(QIcon("./src/subtract.png"))
        self.subbtn.clicked.connect(self.tuopan)
        self.subbtn.move(490, 0)

        self.desktop_width = QApplication.desktop().width() #屏幕尺寸
        self.desktop_height = QApplication.desktop().height()
        self.resize(550, 450)
        self.move((self.desktop_width-self.width())/2,(self.desktop_height-self.height())/2) #将窗口放在屏幕中间
        self.setWindowTitle('Brighter Eyes')
        #设置背景图片
        #self.setStyleSheet("border-image: url(./backgroud1.jpg)");
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./src/first.jpg")))
        self.setPalette(window_pale)

        #开始按钮
        self.btn = QPushButton('Start',self)
        self.btn.move(200,250)
        #self.btn.setStyleSheet("QPushButton{background-color:#e6e6f2;color:#000000;font-size:30px;width:80px;height:30px;}")
        self.btn.setStyleSheet("width:80px;height:30px")
        self.btn.setToolTip('Press and Push')
        self.btn.clicked.connect(self.startState) #可以用connect连接一个函数
        self.show()

    def tuopan(self):
        tuopan = QSystemTrayIcon(self)
        icon = QIcon('./src/logo.png')
        tuopan.setIcon(icon)
        tuopan.show()
        tuopan.showMessage("brighter eyes", "你的护眼小助手被隐藏到这里了哦", icon=1)
        # 如果不show(), 便不会显示, 后面的showMessage也会失效.
        self.hide()
        tuopan.activated.connect(self.show)
        # 在系统托盘区域的图标被点击就会触发activated连接的函数(此例中是a函数)

    def startState(self):
        self.btn.close()
        QApplication.processEvents()
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./src/second2.jpg")))
        self.setPalette(window_pale)

        gridlayout = QGridLayout()
        gridlayout.setContentsMargins(30, 30, 30, 30)
        gridlayout.setSpacing(15)

        self.AgeList = QListWidget(self)
        self.AgeList.setObjectName("ageList")
        item = QListWidgetItem("10岁-20岁")
        self.AgeList.addItem(item)
        item = QListWidgetItem("20岁-40岁")
        self.AgeList.addItem(item)
        item = QListWidgetItem("40岁-60岁")
        self.AgeList.addItem(item)
        item = QListWidgetItem("60岁以上")
        self.AgeList.addItem(item)
        self.AgeList.setStyleSheet("QListWidget{background-color:None;color:#000000;font-size:18px;}")

        self.agelabel = QLabel("请选择你的年龄")
        #void addWidget(QWidget *, int row, int column, int rowSpan, int columnSpan, Qt::Alignment = 0);
        gridlayout.addWidget(self.agelabel,1,0,1,1)
        gridlayout.addWidget(self.AgeList,0,1,3,3,Qt.AlignCenter)

        self.professionList = QListWidget(self)
        self.professionList.setObjectName("professionList")
        item = QListWidgetItem("写作业")
        self.professionList.addItem(item)
        item = QListWidgetItem("玩游戏")
        self.professionList.addItem(item)
        item = QListWidgetItem("看视频")
        self.professionList.addItem(item)
        item = QListWidgetItem("其他")
        self.professionList.addItem(item)
        self.prolabel = QLabel("请选择你的用途")

        self.professionList.setStyleSheet("QListWidget{background-color:None;color:#000000;font-size:18px;}")
        #self.professionList.setResizeMode(QListWidget.Adjust)
        self.professionList.resize(100,100)
        gridlayout.addWidget(self.prolabel,4,0,1,1)
        gridlayout.addWidget(self.professionList,3,1,3,3,Qt.AlignCenter)

        self.nextbtn=QPushButton("下一步")
        self.quitbtn=QPushButton("取消")
        self.quitbtn.clicked.connect(QCoreApplication.quit)
        self.nextbtn.clicked.connect(self.makesure)
        gridlayout.addWidget(self.nextbtn,3,4,2,2,Qt.AlignCenter)
        gridlayout.addWidget(self.quitbtn,4,4,2,2,Qt.AlignCenter)
        self.setLayout(gridlayout)
        self.show()

    def makesure(self):
        age = self.AgeList.currentItem().text()
        job = self.professionList.currentItem().text()
        self.nextbtn.close()
        self.quitbtn.close()
        self.AgeList.close()
        self.professionList.close()
        self.agelabel.close()
        self.prolabel.close()
        QApplication.processEvents()
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./src/third.jpg")))
        self.setPalette(window_pale)
        self.thres = camera_shooting.get_thres(age, job)

        #可以先在页面上输出一些提示信息
        self.pbLogin = QPushButton(u'开始', self)
        self.pbCancel = QPushButton(u'取消', self)
        self.pbLogin.clicked.connect(self.begin)
        self.pbCancel.clicked.connect(QCoreApplication.quit)
        self.pbLogin.move(430, 270)
        self.pbCancel.move(430, 350)
        self.pbLogin.show()
        self.pbCancel.show()

    def begin(self):
        self.pbLogin.close()
        self.pbCancel.close()
        QApplication.processEvents()
        self.move(0.7 * self.desktop_width, 0.1 * self.desktop_height)
        self.resize(350, 250)
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./src/relax.jpg")))
        self.setPalette(window_pale)
        self.closebtn.move(320, 0)
        self.subbtn.move(290, 0)
        self.thread = MyThread(self.thres)  # 实例化线程
        self.thread.sinOut.connect(self.outputwindow)  # 将信号连接至槽
        self.thread.start()  # 开启线程

    def outputwindow(self,state):
        QApplication.processEvents()
        self.move(0.7*self.desktop_width, 0.1*self.desktop_height)
        self.resize(350,250)
        self.closebtn.move(320,0)
        self.subbtn.move(290,0)
        self.video = QPushButton("Video", self)
        self.video.move(100, 10)
        self.video.setStyleSheet(
            "QPushButton{font-size:15px;}")
        self.video.resize(50, 30)
        self.txt = QLabel(self)
        self.txt.setFont(QFont("Microsoft YaHei"))
        self.txt.setStyleSheet("QLabel{font-size:13px}")
        self.txt.move(10, 10)
        self.txt.setText("看看视频放松")
        self.video.clicked.connect(self.play_video)

        if state == 0: #正常状态
            window_pale = QPalette()
            window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./src/normal.jpg")))
            self.setPalette(window_pale)
            self.video.close()
            self.txt.close()

        elif state == 1: #疲劳状态
            window_pale = QPalette()
            window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./src/tired.jpg")))
            self.setPalette(window_pale)
            self.video.show()
            self.txt.show()
            self.show()

        elif state == -1: #特殊状态，检测不到人脸
            window_pale = QPalette()
            window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./src/relax.jpg")))
            self.setPalette(window_pale)
            self.txt.close()
            self.video.close()

    def play_video(self):
        self.hide()
        QApplication.processEvents()
        self.video.close()
        self.player = video.Player(sys.argv[1:])
        self.player.show()
        self.player.exec_()
        self.show()
        self.video.show()

class MyThread(QThread):
    sinOut = pyqtSignal(int) #int输出
    def __init__(self, thres):
        super().__init__()
        self.state = 0
        self.thres = thres

    def run(self):
        while True:
            self.state = camera_shooting.fun_timer(self.thres) #在线程中进行疲劳计算
            self.sinOut.emit(self.state)    #反馈信号出去
            time.sleep(600) #这里设置两次眼疲劳测试的间隔时间

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #sys.argv是一组命令行参数的列表。Python可以在shell里运行，
    #这个参数提供#对脚本控制的功能。
    main = MainWindow()
    #show()能让控件在桌面上显示出来。控件在内存里创建，之后才能在显示器上显示出来。
    sys.exit(app.exec_())
    #sys.exit()方法能确保主循环安全退出。外部环境能通知主控件怎么结束。