# Brighter-Eyes
实验环境：Windows10/pycharm/python3.6
依赖库：opencv3, pyqt5

# 代码说明：
eye_process.py：获取眼部特征点坐标，图片二值化，判断睁闭眼 <br>
MSR.py：对图片进行光照归一化处理，MSR算法的实现 <br>
video.py ：在pyqt5中播放本地视频 <br>
window.py : 程序入口，用pyqt5搭建界面，并实现间隔一段时间后台调用摄像头获取视频流，调用eye_process.py获取睁闭眼状态 <br>
camera_shooting.py：从视频流中读取多张图片 <br>

# 资源文件
init_img：存储拍摄到的尺寸归一化后的待检测图片 <br>
MSR：存储光照归一化后的图片 <br>
binary：存储二值化后的图片 <br>
open：判断为睁眼的图片 <br>
close：判断为闭眼的图片 <br>
error：无法判断的图片，一只眼/无脸部… <br>
src：存储界面资源图片及资源视频 <br>
