import cv2
import numpy as np
import time
import math

def escreve_texto(img, text, origem, color):
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(img, text, origem, font, 1, color, 2, cv2.LINE_AA)

cont = 0
left = 0
right = 0


vc = cv2.VideoCapture("pedra-papel-tesoura.mp4")

while vc.isOpened():
    ret, img = vc.read()

    sizex = 100
    sizey = 40
    color = (5,79,119)

    if img is None:
       cv2.destroyWindow('Pedra Papel e Tesoura')
       vc.release()   
    else:
        img = cv2.resize(img, (800, 600))

        crop_img = img[100:600, 100:450]
        crop_img1 = img[100:600, 350:800]

        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        grey1 = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)

        k_size = (35, 35)
        filtro_blur = cv2.GaussianBlur(grey, k_size, 0)
        filtro_blur1 = cv2.GaussianBlur(grey1, k_size, 0)

        _, thresh = cv2.threshold(filtro_blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        _, thresh1 = cv2.threshold(filtro_blur1, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(thresh.copy(), \
            cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        contours1, hierarchy1 = cv2.findContours(thresh1.copy(), \
            cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        max_area = -1
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area>max_area:
                aux = contours[i]
                max_area = area

        max_area1 = -2
        for i in range(len(contours1)):
            area1 = cv2.contourArea(contours1[i])
            if area1>max_area1:
                aux1 = contours1[i]
                max_area1 = area1        

        cnt = aux

        M = cv2.moments(cnt)

        if M["m00"] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        else: 
            M["m00"] == 0.1
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        
        cnt1 = aux1

        M1 = cv2.moments(cnt1)

        if M1["m00"] != 0:
            cx1 = int(M1['m10']/M1['m00'])
            cy1 = int(M1['m01']/M1['m00'])
        else: 
            M1["m00"] == 0.1
            cx1 = int(M1['m10']/M1['m00'])
            cy1 = int(M1['m01']/M1['m00'])

        drawing = np.zeros(crop_img.shape,np.uint8)
        drawing1 = np.zeros(crop_img1.shape,np.uint8)
        
        if max_area > 14500 and max_area < 17000:
            txt = "Paper"
            escreve_texto(img, txt, (100, 100), (0, 114, 160))
        elif max_area > 11500 and max_area < 14000:
            txt = "Rock"
            escreve_texto(img, txt, (100, 100), (0, 114, 160))
        elif max_area < 11500 and max_area > 6000:
            txt = "Scissors"
            escreve_texto(img, txt, (100, 100), (0, 114, 160))
        else:
            escreve_texto(img, "", (500, 100), (0, 114, 160))

        if max_area1 > 14500 and max_area1 < 17000:
            txt1 = "Paper"
            escreve_texto(img, txt1, (500, 100), (0, 114, 160))
        elif max_area1 > 11500 and max_area1 < 14000:
            txt1 = "Rock"
            escreve_texto(img, txt1, (500, 100), (0, 114, 160))
        elif max_area1 < 11500 and max_area1 > 6000:
            txt1 = "Scissors"
            escreve_texto(img, txt1, (500, 100), (0, 114, 160))
        else:
            escreve_texto(img, "", (500, 100), (0, 114, 160))


        if (txt == "Rock" and txt1 == "Scissors") or (txt == "Scissors" and txt1 == "Paper" ) or (txt == "Paper" and txt1 == "Rock"):
            escreve_texto(img, "left player won", (150, 40), (0, 0, 255))

        elif (txt == "Scissors" and txt1 == "Rock") or (txt == "Paper" and txt1 == "Scissors") or (txt == "Rock" and txt1 == "Paper"):
            escreve_texto(img, "right player won", (150, 40), (0, 0, 255))

        else:
            escreve_texto(img, "Draw the game", (320, 40), (0, 71, 100))

        cont += 1
        if cont >= 90:
            cont = 0

            if (txt == "Rock" and txt1 == "Scissors") or (txt == "Scissors" and txt1 == "Paper" ) or (txt == "Paper" and txt1 == "Rock"):
                left += 1

            elif (txt == "Scissors" and txt1 == "Rock") or (txt == "Paper" and txt1 == "Scissors") or (txt == "Rock" and txt1 == "Paper"):
                right += 1

            else:
                escreve_texto(img, "Draw the game", (320, 40), (0, 71, 100))

        text = f"Left: {left} X Right: {right}"
        escreve_texto(img, text, (150, 70), (5, 19, 119))            

        cv2.imshow('Pedra Papel e Tesoura', img)
        
        k = cv2.waitKey(10)
        if k == 27:
            break