# FMMU: BIO2021

课程：生物医学传感器综合实验

## 介绍

采用MAX30001进行生物阻抗和ECG测量，经由Micropython（ESP32）传输至PC并绘制肺阻抗图像。

Micropython开发平台使用01Studio的ESP32P，参考文档及例程见：
  - https://docs.01studio.cc/esp32/quickref.html
  - https://github.com/01studio-lab/MicroPython_Examples

## 大作业

  1. 读空FIFO（判断BTAL）或者读取定长数据，将读取到的数据打包经TCP发送至上位机，绘制图像并存储。
  2. 分析数据，提取应用相关的指标
