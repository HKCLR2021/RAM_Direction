#set PYTHONPATH = /home/adminis/anaconda3/envs/graspnet/bin/python

import cv2 
import numpy as np
import matplotlib.pyplot as plt
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageStat,ImageEnhance

def brightness( im_file ):
   #im = Image.open(im_file).convert('L')
   im = im_file.convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]

img_path = "shot_inverse_1_Color.png"

def image_infer(img_path):
    ###optimize brightness 
    img_pil = Image.open(img_path)
    img = np.asanyarray(img_pil)
   
    wid = 17 #16

    x1 =  513    #507
    x2 = x1+ wid
    y1 = 148    #145
    y2 = y1+wid

    img1 = img[y1:y2,x1:x2,:]

    i =25
    imgresize=cv2.resize(img1,(i*wid,i*wid))
    img_copy = copy.deepcopy(imgresize)

    ###optimize brightness 
    imgresize = Image.fromarray(imgresize)
    bright_x = 180/brightness(imgresize) #39.4 #nor3:max 16 #180
    opt_bright_img  =  ImageEnhance.Brightness(imgresize).enhance(bright_x)
    #print('######################brightness',brightness(opt_bright_img))
    img_br = np.asanyarray(opt_bright_img)
    img_br = cv2.cvtColor(img_br, cv2.COLOR_RGB2BGR)
    '''
    save_name =  sub_path + 'bri'
    save_path = os.path.join(args.output_dir, save_name )
    save_path = save_path + '.png'
    cv2.imwrite(save_path,img_br)
    '''

    '''
    #图像的非线性灰度变换: 幂律变换 (伽马变换)
    normImg = lambda x: 255. * (x-x.min()) / (x.max()-x.min()+1e-6)  # 归一化为 [0,255]
    imgGamma = np.power(img_br, 1.9) #1.9
    img_edges = np.uint8(normImg(imgGamma))
    #cv2.imwrite('cpower' + '.png',edges)
    save_name =  sub_path + 'box'
    save_path = os.path.join(args.output_dir, save_name )
    save_path = save_path + '.png'
    cv2.imwrite(save_path,img_edges)
    '''

    imgray=cv2.cvtColor(img_br,cv2.COLOR_BGR2GRAY)

    # 对得到的图像进行形态学操作（闭运算和开运算）
    kernel = np.ones((3, 3), np.uint8)
    #kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(imgray, cv2.MORPH_CLOSE, kernel) #闭运算：表示先进行膨胀操作，再进行腐蚀操作
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   #开运算：表示的是先进行腐蚀，再进行膨胀操作

    _, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_OTSU)
    ###edges = cv2.Canny(binary, threshold1=50, threshold2=200)
    edges = cv2.Canny(binary, 40, 180, L2gradient=True, apertureSize=3) 
    #lines_p = cv2.HoughLinesP(edges,1,np.pi/360,10,minLineLength=30,maxLineGap=5)
    lines_p = cv2.HoughLinesP(edges,1,np.pi/360,10,minLineLength=5,maxLineGap=10) #20 5 ##5,10

    vert = 0
    level = 0

    '''
    for i in range(len(lines_p)):
        x_1, y_1, x_2, y_2 = lines_p[i][0]
        cv2.line(img_br, (x_1, y_1), (x_2, y_2), (0, 255, 0), 2)
    '''

    for line in lines_p:
        x1,y1,x2,y2 = line[0]
        #cv2.line(img_br,(x1,y1),(x2,y2),(0,0,255),2) 
        cv2.line(mask,(x1,y1),(x2,y2),(0,0,255),2)  
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        #print(x1,x2,y1,y2)
        if x2 - x1 == 0:
            vert += 1
        elif y2 - y1 == 0 :
            level +=1
        else:
            # 计算斜率
            k = -(y2 - y1) / (x2 - x1)
            # 求反正切，再将得到的弧度转换为度
            result = np.arctan(k) * 57.29577
            if -5 < result < 5: level +=1
            if 80 < result < 90: vert +=1
    #print('\n')
    #print(img_path,vert,level,vert/(level+0.01))
    #print(vert,level,vert/(level+0.01))

    bound = 60
    area_2 = mask[2*bound:3*bound,:] 
    (mean , stddv) = cv2.meanStdDev(area_2)
    flag1 = stddv
    

    flag = vert/(level+0.01)
    print('Get result:')
    #if flag > 22:
    if flag1 > 58:
        print('inverse')
        return [[0.0]]
    else: 
        print('normal')
        return [[1]]

if __name__ == "__main__":
    image_infer()
    #image_infer(img_path)

