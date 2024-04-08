from PIL import Image
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import cv2

# image_path = "../data/jpeg/i000.jpeg"
# image = Image.open(image_path)
# display(image)

# Nous avons utilisé la documentatino de openCV pour compléter le code 
#https://docs.opencv.org/4.x/d1/db7/tutorial_py_histogram_begins.html 
def obtenirDescHistogrammeCouleur(image): 

    # conversion de l'image en 3 tableaux R,G,B
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    RGBArray = np.asarray(image)
    Rarray = []
    Garray = []
    Barray = []
    # for pixel in RGBArray:
    #     Rarray = np.append(Rarray, pixel[0])
    #     Garray = np.append(Garray, pixel[1])
    #     Barray = np.append(Barray, pixel[2])

    # # conversion 256 -> 32 niveaux et création des histogrammes
    # histoR = np.histogram(Rarray, 64, (0.0, 256.0))
    # histoG = np.histogram(Garray, 64, (0.0, 256.0))
    # histoB = np.histogram(Barray, 64, (0.0, 256.0))

    # # concaténation des 3 quantifications en un seul vecteur de dimension D
    # # HistoR [1,4,6,4]
    # # HistoG [2,7,9,3]
    # # HistoB [5,8,3,1]
    # # histogramme = np.array([])
    # # for index in range(len(histoR[0])):
    # #     histogramme = np.append(histogramme, histoR[0][index]/len(RGBArray))
    # #     histogramme = np.append(histogramme, histoG[0][index]/len(RGBArray))
    # #     histogramme = np.append(histogramme, histoB[0][index]/len(RGBArray))
    # # histogramme (desc) [1, 2, 5, 4, 7, 8, 6, 9, 3, 4, 3, 1]    
    # #                     0  1  2
    # #                     -------
    # #                      

    # histogramme = np.append(histoR[0], [histoG[0], histoB[0]])

    # plt.plot(histoR[0])
    # plt.title(f"Descripteur d'une image à partir d'un histogramme de couleur")
    # plt.show()

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    channels = []
    channels = cv2.split(image)
    # Rarray = cv2.equalizeHist(Rarray)
    # Garray = cv2.equalizeHist(Garray)
    # Barray = cv2.equalizeHist(Barray)

    # Rarray = cv2.equalizeHist(channels[0].flatten())
    # Rarray = Rarray.flatten()
    Rarray = cv2.calcHist([image],[0],None,[4],[0,256])
    
    # Garray = cv2.equalizeHist(channels[1].flatten())
    # Garray = Garray.flatten()
    Garray = cv2.calcHist([image],[1],None,[4],[0,256])
    
    # Barray = cv2.equalizeHist(channels[2].flatten())
    # Barray = Barray.flatten()
    Barray = cv2.calcHist([image],[2],None,[4],[0,256])

    desc = []
    for i in range(len(Rarray)):
        desc.append(Rarray[i])
        desc.append(Garray[i])
        desc.append(Barray[i])

    desc = np.array(desc)
    return(desc)