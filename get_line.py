import requests
import base64
import cv2
import numpy as np
import math
import run
class Point:
    def __init__(self, x, y):
        self.x = x  # 初始化点的横纵坐标
        self.y = y


class Line:
    def __init__(self, start, end):
        self.start = start  # 初始化线的起始点
        self.end = end  # 初始化点的另一个点
        try:  # 若线的k.b均存在
            k = float(end.y - start.y) / (end.x - start.x)  # 斜率
            b = float(start.y) - k * start.x  # 截距
            self.k = k
            self.b = b
            self.min = min(start.x, end.x)  # 定义域
            self.max = max(start.x, end.x)
            self.has_k = True  # 若斜率存在
        except ZeroDivisionError:  # 斜率不存在
            self.b = start.x  # k=0
            self.min = min(start.y, end.y)
            self.max = max(start.y, end.y)
            self.has_k = False


class Image:
    def __init__(self, img_filename):
        f = open(img_filename, 'rb')
        self._base64 = base64.b64encode(f.read())
        f.close()
        self._ip = cv2.imread(img_filename)
        self._name=img_filename.split('_')[2] # 0.jpg
        self._left = []
        self._right = []
        self._size=[]
        self._left_scope = {}
        self._right_scope = {}
        self._scope={}
        self.get_eyes_point()

        #assert min(self._left) <= 0 or min(self._right)<= 0, '检测失败，左右眼必须全部出现'
    def if_eyes(self):#判断是否检测出人脸(通过存储左右眼坐标数组)
        return len(self._left)+len(self._right)

    def get_eyes_point(  # 获取左右眼点的具体坐标值
            self,
            access_token='24.50be4e6ced3afbe6c23551e730aa012d.2592000.1528208032.282335-11197866',
            url='https://aip.baidubce.com/rest/2.0/face/v3/detect'):
        url += '?access_token=%s' % access_token
        response = requests.post(url=url, data={'image': self._base64, "image_type": "BASE64",
                                                "face_field": "faceshape,facetype,age,landmark"})
        Re=response.json()
        if Re["result"]==None:#若未检测到人脸
            return

        eye_point = response.json()['result']['face_list'][0]['landmark72']

        self._left = eye_point[13:21]
        self._right = eye_point[30:38]
        #assert self._left[0]['x']<0 or self._right[4]['x']<=0,'检测失败，左右眼必须全部出现'
        self._size=[eye_point[1],eye_point[12],eye_point[5],eye_point[6],eye_point[24],eye_point[41],eye_point[34],eye_point[13],eye_point[22],eye_point[43]]
        return {
            'left': eye_point[13:21],
            'right': eye_point[30:38]
        }

    def _get_scope(self):  # 分别获取左右眼的x、y定义域
        def get_scope_tmp(l):
            x_min = x_max = l[0]['x']
            y_min = y_max = l[0]['y']
            line_store = []
            for i, each in enumerate(l):
                if each['x'] < x_min:
                    x_min = each['x']
                if each['x'] > x_max:
                    x_max = each['x']
                if each['y'] < y_min:
                    y_min = each['y']
                if each['y'] > y_min:
                    y_max = each['y']
                p0 = each
                try:
                    p1 = l[i + 1]
                except IndexError:
                    p1 = l[0]
                t=self._ip.shape[0]
                line_store.append(Line(start=Point(p0['x'], t - p0['y']),
                                       end=Point(p1['x'], t - p1['y'])))

            return {
                       'x_min': round(x_min),
                       'x_max': round(x_max),
                       'y_min': round(y_min),
                       'y_max': round(y_max)
                   }, line_store

        l_temp = get_scope_tmp(self._left)
        r_temp = get_scope_tmp(self._right)
        size_temp=get_scope_tmp(self._size)
        self._left_scope, self.left_line_store = l_temp
        self._right_scope, self.right_line_store = r_temp
        self._scope,self.line_store=size_temp

    def get_ratio(self):  # 第二个特征，每个眼睛区域内白色像素点所占比例
        def get_ratio_temp(scope, store,size):
            count = 0  # 在区域内的像素点个数
            flag = 0


            binary_ip = cv2.cvtColor(self._ip.copy(), cv2.COLOR_BGR2GRAY)
            sum=0
            cnt = 0
            temp = []
            x_size1=self._scope['x_min']
            x_size2=self._scope['x_max']
            y_size1=self._scope['y_min']
            y_size2=self._scope['y_max']
            x_size, y_size = binary_ip.shape

            if x_size1<0:
                x_size1=0
            if x_size2>x_size:
                x_size2=x_size
            if y_size1<0:
                y_size1=0
            if y_size2>y_size:
                y_size2=y_size
            print(x_size1,x_size2,y_size1,y_size2)

            for i in range(x_size1,x_size2):
                for j in range(y_size1,y_size2):
                    sum+=binary_ip[i][j]
                    cnt+=1
            if cnt==0:
                cnt=1

            for i in range(x_size1,x_size2):
                for j in range(y_size1,y_size2):
                    sum+=binary_ip[i][j]
                    cnt+=1

            ret, thresh1 = cv2.threshold(binary_ip,(sum/cnt)*0.7, 255, cv2.THRESH_BINARY)
            binary_name='binary/binary_time_'+self._name
            cv2.imwrite(binary_name, thresh1)
            if x_size<scope['y_max'] or y_size<scope['x_max']:
                return -1
            for x in range(scope['x_min'], scope['x_max']):
                for y in range(scope['y_min'], scope['y_max']):
                    if is_in_it(Point(x, (self._ip.shape)[0] - y), store):
                        count += 1
                        cur_rgb = thresh1[y][x]
                        if cur_rgb == 255:  # 统计白色像素点个数
                            flag += 1
                        # print(cur_rgb[0], cur_rgb[1], cur_rgb[2])
                        # cv2.circle(new, (x, y), 1, (int(cur_rgb[0]), int(cur_rgb[1]), int(cur_rgb[2])))

            if count==0:
                return -1
            return float(flag) / count

        self._get_scope()
        l_re = get_ratio_temp(self._left_scope, self.left_line_store,self._scope)
        r_re = get_ratio_temp(self._right_scope, self.right_line_store,self._scope)
        return l_re, r_re

    def get_l_w(self):  # 第二个衡量因素，得到最右眼长宽比
        l = self._left
        r = self._right
        l1 = l[0]
        l2 = l[4]
        l3 = l[2]
        l4 = l[6]
        r1 = r[0]
        r2 = r[4]
        r3 = r[2]
        r4 = r[6]
        l_d = math.sqrt(math.pow((l1['x'] - l2['x']), 2) + math.pow((l1['y'] - l2['y']), 2)) / math.sqrt(
            math.pow((l3['x'] - l4['x']), 2) + math.pow((l3['y'] - l4['y']), 2))
        r_d = math.sqrt(math.pow((r1['x'] - r2['x']), 2) + math.pow((r1['y'] - r2['y']), 2)) / math.sqrt(
            math.pow((r3['x'] - r4['x']), 2) + math.pow((r3['y'] - r4['y']), 2))
        return l_d, r_d


def is_cross(p, l):  # 判断两条直线是否相交
    if l.has_k:
        try:
            x = float(p.y - l.b) / l.k  # 计算交点的横坐标
            return l.min <= x <= l.max and x > p.x  # 确定是否在定义域内
        except ZeroDivisionError:  # k=0
            return l.min <= p.x <= l.max and p.y == l.b
    else:  # 斜率不存在
        return l.min <= p.y <= l.max

def is_in_it(p, line_list):  # 判断某点P是否在line_list围成的区域内
    flag = 0
    for each in line_list:
        if is_cross(p, each):
            flag += 1

    return flag % 2 != 0

def get_result(filename):  # 获取最终结果，返回值0表示闭眼，1表示睁眼
    img = Image(filename)
    if img.if_eyes()==0:
        return -1
    l_rate, r_rate = img.get_ratio()
    print(l_rate,r_rate)
    l_d, r_d = img.get_l_w()
    l_result = l_rate * 0.5 + l_d * 0.5
    r_result = r_rate * 0.5 + r_d * 0.5
    print(l_result,r_result)
    if l_rate==-1 or r_rate==-1:
        return -1
    else:
        if l_result > 2.15 and r_result > 2.15:
            return 0
        else:
            return 1

if __name__ == '__main__':
    image = cv2.imread('test8.jpg')
    x, y, z = image.shape
    new = cv2.resize(image, (int(y / 3), int(x / 3)), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('small.jpg',new)
    new_t=run.new_pic('small.jpg')
    cv2.imwrite('msr.jpg',new_t)
    t = get_result('msr.jpg')
    if t == 1:
        print("睁眼")
    elif t == 0:
        print("闭眼")
    else:#返回值为-1,眼睛不全
        print("舍弃")
