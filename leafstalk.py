
import numpy as np
import cv2


img = cv2.imread('leaf (3).jpg',0)
#изменение размеров изображения
r = 300.0 / img.shape[1]
dim = (300, int(img.shape[0] * r))
#tophat
kernel = np.ones((25,37),np.uint8)
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

thresh = cv2.threshold(tophat, 200, 255, cv2.THRESH_BINARY)[1]#удаление рамки после топхэта

_, contours,_ = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#поиск объектов на изображении

img3 = img.copy()

#вычисление диагонали прямоугольного контура объекта
def findDiag(cont):
    #создание прямоугольного контура вокруг объекта
    rect = cv2.minAreaRect(cont)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    #вычисление длины диагонали
    side = np.sqrt((box[0,0]-box[2,0])**2+(box[2,1]-box[0,1])**2)
    return side

#поиск самой длинной диагонали
for cont in contours:
    side = findDiag(cont)
    if side > maxSide:
        maxSide = side
 
#определение объекта с самой длинной диагональю        
for cont in contours:
    #определение координат пикселей объекта
    mask = np.zeros(thresh.copy().shape,np.uint8)
    cv2.drawContours(mask,[cont],0,255,-1)
    pixelpoints = np.transpose(np.nonzero(mask))
    #вычисление длин диагоналей
    side = findDiag(cont)
    #удаление объекта с самой длинной диагональю
    if side == maxSide:
        forPoint = pixelpoints
        for i in pixelpoints:
            img3[i[0],i[1]] = 0

#переход к цветному изображению
backtorgb = cv2.cvtColor(img3,cv2.COLOR_GRAY2RGB)

#поиск точки роста, coord - координаты точки роста
for i in forPoint:
    if img3[i[0]-1,i[1]] == 255:
        coord = i[0]-1,i[1]
        continue
    elif img3[i[0],i[1]+1] == 255:
         coord = i[0],i[1]+1
         continue
    elif img3[i[0]+1,i[1]] == 255:
         coord = i[0]+1,i[1]
         continue
    elif img3[i[0],i[1]-1] == 255:
         coord = i[0],i[1]-1
         continue

#выделение точки роста на изображении
backtorgb[coord[0],coord[1]] = [0,0,255]
height, width, channels = backtorgb.shape
print (coord)
cv2.line(backtorgb,(0,coord[0]),(height,coord[0]),(0,0,255),1)
cv2.line(backtorgb,(coord[1],width),(coord[1],0),(0,0,255),1)

res1 = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
res2 = cv2.resize(img3, dim, interpolation = cv2.INTER_AREA)
res3 = cv2.resize(backtorgb, dim, interpolation = cv2.INTER_AREA)

#cv2.imshow('imgs', np.hstack([res1,res2]))
cv2.imshow('rgb', res3)
cv2.waitKey(0)
cv2.destroyAllWindows()
