### **人脸情绪识别系统**



介绍视频https://www.bilibili.com/video/BV1Kk4y1C7tL/

#### ./PC

模型识别效果展示

![image](https://github.com/lrioxh/facialExpression/blob/main/pic/image-20210118153507172.png)

运行recognition_camera.py可利用摄像头实时识别

#### ./云主机

部署服务器所用, 服务器为flask+gunicorn+nginx架构, 系统centos7, 作为小程序上传图片识别的后端



#### ./小程序

查询及图片识别小程序