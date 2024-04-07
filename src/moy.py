import cv2


sommeFps = 0
for i in range(1, 101):
    if(i < 10): 
        path = "../data/mp4/v00" + str(i) + ".mp4"
    elif(i < 100):
        path = "../data/mp4/v0" + str(i) + ".mp4"
    elif(i == 100):
        path = "../data/mp4/v" + str(i) + ".mp4"
    
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    sommeFps += fps

moyenneFps = sommeFps/100
