import cv2
import mediapipe as mp
import pyautogui
import numpy

pyautogui.FAILSAFE=False

cap=cv2.VideoCapture(0)

mp_hand=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
hands=mp_hand.Hands()
width_screen , hight_screen=pyautogui.size()
px ,py=0,0
xc,yc=0,0

def handLandMark(framee):
    landMarkList=[]
    
    restuls=hands.process(framee)
    if restuls.multi_hand_landmarks:
        for handml in restuls.multi_hand_landmarks:
            for id ,lm in enumerate(handml.landmark):
                h ,w , c=Frame.shape
                cx , cy= int(lm.x*w), int(lm.y*h)
            
                mp_draw.draw_landmarks(Frame,handml,mp_hand.HAND_CONNECTIONS)
                landMarkList.append([id,cx,cy])
    return landMarkList


def fingers(lanMarkLists):
    
    fingerTips=[]
    tipsId=[4,8,12,16,20]

    if lanMarkLists[tipsId[0]][1] > lanMarkLists[tipsId[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)
    
    for idd in range(1,5):
        if lanMarkLists[tipsId[idd]][2] < lanMarkLists[tipsId[idd] - 3][2]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)
    return fingerTips

while True:
    rat,Frame=cap.read()
    
    framRGB=cv2.cvtColor(Frame,cv2.COLOR_BGR2RGB)
    lmlist=handLandMark(framRGB)

    if len(lmlist)!=0:
        x1 ,y1 = lmlist[8][1:]
        x2 ,y2 = lmlist[12][1:]
        finger= fingers(lmlist)
        if finger[1]== 1 and finger[2]==0:
            x3= numpy.interp(x1,(0,640),(0,width_screen))
            y3= numpy.interp(y1,(0,480),(0,hight_screen))
            
            xc= px + (x3-px) /3
            yc= py + (y3-py) /3
            
            pyautogui.moveTo(width_screen-xc, yc)
            px, py= xc,yc
        
        if finger[0]== 0 and finger[1]==1 and finger[2]==1 and finger[3]== 0 and finger[4]== 0:
            pyautogui.click()
            
    cv2.imshow("hands",Frame)
    
    if cv2.waitKey(99) & 0xFF== ord("q"):
        break

cv2.destroyAllWindows()
cap.release()