import numpy as np
import cv2
import sys
from histogramme import *
from reseauNeurones import *

global descriptor
descriptor = ""

def distanceEuclidienne(array1, array2):
    return np.linalg.nomr(array1 - array2)

#https://www.futurelearn.com/info/courses/introduction-to-image-analysis-for-plant-phenotyping/0/steps/305359
def obtenirFrame(path, timestamp):
    video = cv2.VideoCapture(path)
    video.set(cv2.CAP_PROP_POS_MSEC, timestamp)
    ret, frame = video.read()
    #cv2.imshow('frame', frame)
    #cv2.waitKey(0)
    return frame

# https://www.geeksforgeeks.org/get-video-duration-using-python-opencv/
def longueurVideo(path):
    video = cv2.VideoCapture(path)
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    seconds = round(frames / fps)
    return seconds

# indexation
def indexationFrames(path):
    global descriptor
    longueur = longueurVideo(path)
    frames = {}
    i = 0
    while(i < longueur):
        if(descriptor == 'H'):
            frames[i] = (obtenirDescHistogrammeCouleur(obtenirFrame(path, i*1000)))
        elif(descriptor == 'R'):
            frames[i] = (obtenirDescReseauNeurones(obtenirFrame(path, i*1000)))
        i += 1
    return frames




#TODO path dymanique

# recherche avec NN ou Histo

def main():
    global descriptor
    descriptor = sys.argv[1]
    # R : option pour Réseau Neuronal, H : option pour histogramme de couleur
    while(descriptor != 'R' and descriptor != 'H'):
        descriptor = input("Veuillez entrer un choix de descripteur valide (R ou H) \n")
    print(indexationFrames("../data/mp4/v001.mp4"))


#ouvrir jpeg avec opencv



if __name__ == "__main__":
    main()