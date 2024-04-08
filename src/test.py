from histogramme import *
from reseauNeurones import *
from main import *
import cv2
import matplotlib.pyplot as plt

nomImage = input("quelle image veux-tu monsieur morororonne")
pathIm = "../data/jpeg/i" + nomImage + ".jpeg"

modeIndex = input("tu veux tu rézo nono (N) ou histototho (H)")

image = cv2.imread(pathIm)


nomVideo = input("quelle video tu veux à c't'heure?66??6??6 (001 à 100)")
pathVid = "../data/mp4/v" + nomVideo + ".mp4"

timestamp = float(input("quelle seconde ????????????????"))
frame = obtenirFrame(pathVid, int(timestamp*1000))

if modeIndex == "H":
    descImage = obtenirDescHistogrammeCouleur(image)
    descVid = obtenirDescHistogrammeCouleur(frame)

elif modeIndex == "N":
    descImage = obtenirDescReseauNeurones(image)
    descVid = obtenirDescReseauNeurones(frame)


cv2.imshow("image",image)
cv2.waitKey(0) 
plt.plot(descImage)
plt.title(f"Histogramme image")
plt.show() 


cv2.imshow("frame de la vidéo",frame)
cv2.waitKey(0) 
plt.plot(descVid)
plt.title(f"Histogramme video")
plt.show() 
