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

#Code repéré au https://www.futurelearn.com/info/courses/introduction-to-image-analysis-for-plant-phenotyping/0/steps/305359
def obtenirFrame(path, timestamp):
    video = cv2.VideoCapture(path)
    video.set(cv2.CAP_PROP_POS_MSEC, timestamp)
    ret, frame = video.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
    encodedimg = cv2.imencode('.jpg', frame, encode_param)[1]
    decodedimg = cv2.imdecode(encodedimg, cv2.IMREAD_COLOR)
    return decodedimg

#Code repéré au  https://www.geeksforgeeks.org/get-video-duration-using-python-opencv/
def longueurVideo(path):
    video = cv2.VideoCapture(path)
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    seconds = round(frames / fps, 2)
    return seconds

# indexation
def indexationFrames(path):
    global descriptor
    longueur = longueurVideo(path)
    frames = {}
    i = 0
    while(i < longueur*1000-100):
        if(descriptor == 'H'):
            frames[i/1000] = (obtenirDescHistogrammeCouleur(obtenirFrame(path, i)))
        elif(descriptor == 'R'):
            frames[i/1000] = (obtenirDescReseauNeurones(obtenirFrame(path, i)))
        i += 250
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
    seuil = 0
    if(descriptor == 'H'):
        descImage = obtenirDescHistogrammeCouleur(image)
        seuil = 130000.0
    elif(descriptor == 'R'):
        descImage = obtenirDescReseauNeurones(image)
        seuil = 15.0
    
    bestDist = math.inf
    bestTime = None
    bestVideo = "out"

    for videoName in indexations:
        for timestamp in indexations[videoName]:
            dist = distanceEuclidienne(indexations[videoName][timestamp], descImage)
            
            if (dist < bestDist and dist < seuil): 
            #if (dist < bestDist): 
                bestDist = dist
                bestTime = timestamp
                bestVideo = videoName
                bestDesc = indexations[videoName][timestamp]
    
    # plt.plot(descImage)
    # plt.title(f"Histogramme image")
    # plt.show() 
    
    # plt.plot(bestDesc)
    # plt.title(f"Histogramme frame trouvée")
    # plt.show()
    #print(path[13:17] + ": " + str(bestDist))
    #print("Recherche complétée à " + str(round(int(path[14:17])/1000 * 100)) + " %         \r",)
    return bestVideo, bestTime


def main():
    global descriptor
    
    descriptor = sys.argv[1]
    # R : option pour Réseau Neuronal, H : option pour histogramme de couleur
    while(descriptor != 'R' and descriptor != 'H'):
        descriptor = input("Veuillez entrer un choix de descripteur valide (R ou H) \n")
    if(descriptor == 'R'): initialiserRN()
    
    start = t.time()
    indexations = indexerVideos()
    end = t.time()
    
    print("Temps d'indexation: " + str(end - start))
    
    with open("../results/test.csv", 'w', newline="") as fichierResultat:
        fichierResultat.truncate()
        header = ["image", "video_pred", "minutage_pred"]
        csvwriter = csv.writer(fichierResultat)
        csvwriter.writerow(header)

        start = t.time()
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
            
        end = t.time()
        N = len([frame for video in indexations.values() for frame in video])
        print("Nombre de frames indexées : " + str(N))
        
        D = len(indexations["v001"][0])
        print("Dimension vecteurs : " + str(D))
        
        tailleOriginale = 444039168
        tauxCompr = 1 - ((N*D*4)/tailleOriginale)
        print("Temps de recherche: " + str(round(end - start, 2)) + " s")
        print("Temps de recherche par image moyen: " + str(round(end - start, 2)) + " ms")
        print("Taux de compression : " + str(round(tauxCompr, 6)) + "%")
        fichierResultat.close()
#ouvrir jpeg avec opencv



if __name__ == "__main__":
    main()