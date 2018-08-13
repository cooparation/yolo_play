# coding=utf-8
# 制作中文label ，命名规则为cn_类索引_字体.png


import os


# 获取物体名list
# path是物体名list文件地址
# 返回值是一个列表,索引是物体id，值为该类物体的名字
def get_name_list(path):
    name_list = []
    f = open(path)
    for line in f:
        line = line.rstrip()
        name_list.append(line)
    return name_list

# 制作标签，s是字体大小
def make_labels(s):
    i = 0
    for word in l:
        os.system(
            "convert -fill black -background white -bordercolor white -border 4  -font /usr/share/fonts/truetype/arphic/ukai.ttc -pointsize %d label:\"%s\" \"cn_%d_%d.png\"" % (
            s, word, i, s / 12 - 1))
        i = i + 1


# l=["人","自行车","车","摩托车","飞机","大巴","火车","卡车","船","交通灯","消防栓","停止标识","停车计时器","长凳","鸟","猫","狗","马","羊","牛","大象","熊","斑马","长颈鹿","背包","伞","手提包","领带","手提箱","飞盘","雪橇","滑雪板","体育用球","风筝","棒球棒","棒球手套","滑板","冲浪板","网球拍","瓶子","红酒杯","杯子","叉子","小刀","勺子","碗","香蕉","苹果","三明治","橘子","西兰花","萝卜","热狗","披萨","甜甜圈","蛋糕","椅子","沙发","盆栽","床","餐桌","厕所","显示器","笔记本","鼠标","遥控","键盘","手机","微波炉","烤箱","吐司机","水槽","冰箱","书","闹钟","花瓶","剪刀","泰迪熊","吹风机","牙刷"]
l = get_name_list("/raid/pengchong_data/Tools/Paul_YOLO/data/paul_cn.names")

for i in [12, 24, 36, 48, 60, 72, 84, 96]:
    make_labels(i)
