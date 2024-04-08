import cv2
from main import longueurVideo, obtenirFrame


sommeFps = 0
sommeDuree = 0
sommePix = 0
firstPix = []
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
    sommeDuree += longueurVideo(path)
    firstPix.append(obtenirFrame(path, 0)[0])



moyenneFps = sommeFps/100
sommeDuree = sommeDuree/100

print(firstPix)
print(moyenneFps)
print(sommeDuree)
