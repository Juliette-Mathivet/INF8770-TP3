import numpy as np
import cv2
import sys
import math
import time as t
from histogramme import *
from reseauNeurones import *
import csv

global descriptor
descriptor = ""

def distanceEuclidienne(array1, array2):
    array1 = np.array(array1)
    array2 = np.array(array2)
    return np.linalg.norm(array1 - array2)

def similariteCosinus(array1, array2):
    array1 = np.array(array1)
    array2 = np.array(array2)
    return np.dot(array1, array2)/(np.linalg.norm(array1) * np.linalg.norm(array2))

#https://www.futurelearn.com/info/courses/introduction-to-image-analysis-for-plant-phenotyping/0/steps/305359
def obtenirFrame(path, timestamp):
    video = cv2.VideoCapture(path)
    video.set(cv2.CAP_PROP_POS_MSEC, timestamp)
    ret, frame = video.read()
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

def indexerVideos():
    indexations = {}
    for i in range(1, 101):
        if(i < 10): 
            path = "../data/mp4/v00" + str(i) + ".mp4"
        elif(i < 100):
            path = "../data/mp4/v0" + str(i) + ".mp4"
        elif(i == 100):
            path = "../data/mp4/v" + str(i) + ".mp4"
        print(path[12:16])
        indexations[path[12:16]] = indexationFrames(path)
    return indexations

def rechercheMeilleureFrame(path, indexations):
    image = cv2.imread(path)
    if(descriptor == 'H'):
        descImage = obtenirDescHistogrammeCouleur(image)
    elif(descriptor == 'R'):
        descImage = obtenirDescReseauNeurones(image)
    
    bestDist = math.inf
    bestTime = None
    bestVideo = "out"
    seuil = 260.0

    for videoName in indexations:
        for timestamp in indexations[videoName]:
            dist = distanceEuclidienne(indexations[videoName][timestamp], descImage)
            
            if (dist < bestDist and dist < seuil): 
            #if (dist < bestDist): 
                bestDist = dist
                bestTime = timestamp
                bestVideo = videoName
    print(path[13:17] + ": " + str(bestDist))
    return bestVideo, bestTime


def main():
    global descriptor
    
    descriptor = sys.argv[1]
    # R : option pour Réseau Neuronal, H : option pour histogramme de couleur
    while(descriptor != 'R' and descriptor != 'H'):
        descriptor = input("Veuillez entrer un choix de descripteur valide (R ou H) \n")
    
    start = t.time()
    indexations = indexerVideos()
    end = t.time()
    print("Temps d'indexation: " + str(end - start))
    
    with open("../results/test.csv", 'w', newline="") as fichierResultat:
        fichierResultat.truncate()
        header = ["image", "video_pred", "minutage_pred"]
        csvwriter = csv.writer(fichierResultat)
        csvwriter.writerow(header)

        for i in range(1000):
            if(i < 10): 
                path = "../data/jpeg/i00" + str(i) + ".jpeg"
            elif(i < 100):
                path = "../data/jpeg/i0" + str(i) + ".jpeg"
            elif(i < 1000):
                path = "../data/jpeg/i" + str(i) + ".jpeg"

            resultatRecherche = rechercheMeilleureFrame(path, indexations)
            
            data = [path[13:17], resultatRecherche[0], resultatRecherche[1]]
            
            csvwriter.writerow(data)
            
        fichierResultat.close()
#ouvrir jpeg avec opencv



if __name__ == "__main__":
    main()