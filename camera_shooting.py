import cv2
import numpy as np
import MSR
import threading
import eye_process
import random
def get_frame(thres): #每隔n分钟调用一次该函数进行疲劳判断
    cap = cv2.VideoCapture(0)
    #fourcc=cv2.VideoWriter_fourcc(*'XVID')

    #outFile = "paishe.avi"
    if cap.isOpened(): #判断是否可以正常打开
        ret, frame = cap.read()
    else:
        ret = False
    #out = cv2.VideoWriter("paishe.avi",fourcc,20.0,(640,480))
    timeF = 5  # 视频帧计数间隔频率
    time = 0 # 计时/计数
    close_count = 0 # 闭眼计数
    count = 0 # 计数分母

    while ret:  # 循环读取视频帧
        rval, frame = cap.read()
        #out.write(frame)
        #frame = cv2.imread('test.png')
        if (time % timeF == 0):  # 每隔timeF帧进行存储操作
            x, y, z = frame.shape
            image = cv2.resize(frame, (int(y / 3), int(x / 3)), interpolation=cv2.INTER_CUBIC)

            # cv2.imwrite('test.jpg',image)
            # run.guangzhao("test.jpg")
            # state = get_line.get_result("new_test.jpg")
            name = 'init_img/time_' + str(time) + '.jpg'  # 视频中读取并resize后图片以""
            cv2.imwrite(name, image)
            new_name = MSR.guangzhao(name)
            state = eye_process.get_result(new_name)
            if state==1:
                print('睁眼~')
            elif state==0:
                print('闭眼~')
            elif state ==-1:
                print('检测失败~')
            #print(state)
            if state != -1:
                count += 1
            else:#返回值为-1
                name = 'error/' + str(time)+'.jpg'
            if state == 0:#返回值为0
                close_count += 1
                name='close/' + str(time)+'.jpg'
            else:
                if state==1:#返回值为1
                    name='open/' + str(time)+'.jpg'
            cv2.imwrite(name, image)
        time = time + 1
        if time == 200:
            break;
    cap.release()
    cv2.destroyAllWindows()
    if count  == 0:
        return -1
    perclos = close_count/count
    if perclos > thres:
        #如果截取的帧当中，20%以上的时间都判断为几乎闭眼状态，则认为此时已经是眼疲劳状态
        return 1
    else:
        return 0

def fun_timer(thres):
    #global Is_tired
    print('Start running!')
    Is_tired = -1  # 程序未运行是-1
    Is_tired = get_frame(thres)
    print(Is_tired)
    if Is_tired == 1:
        print("当前处于疲劳状态，休息一下再玩吧！")
    elif Is_tired == 0:
        print("精神状态很好哦！")
    else:
        print("图片有问题哦！")
    #global timer
    return Is_tired
    #timer = threading.Timer(60, fun_timer)  # 每隔十分钟运行
    #timer.start()

def get_thres(age, task):
    t = 0;
    thres = 0
    if age == "10~20":
        t = -0.01
    elif age == "20~40":
        t = -0.02
    elif age == "40~60":
        t = -0.03
    elif age == "60以上":
        t = -0.04

    if task == "写作业":
        thres = 0.4
    elif task == "玩游戏":
        thres = 0.25
    elif task == "看视频":
        thres = 0.35
    elif task == "其他":
        thres = 0.4
    new_thres = thres + t
    return new_thres

def start():
    timer = threading.Timer(1, fun_timer)
    timer.start()

if __name__ == '__main__':
    timer = threading.Timer(1, fun_timer)
    timer.start()
