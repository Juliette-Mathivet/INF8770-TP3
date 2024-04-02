from PIL import Image
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import cv2

# image_path = "../data/jpeg/i000.jpeg"
# image = Image.open(image_path)
# display(image)

def obtenirDescHistogrammeCouleur(image): 

    # conversion de l'image en 3 tableaux R,G,B
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    RGBArray = np.asarray(image)
    Rarray = []
    Garray = []
    Barray = []
    for pixel in RGBArray:
        Rarray = np.append(Rarray, pixel[0])
        Garray = np.append(Garray, pixel[1])
        Barray = np.append(Barray, pixel[2])

    # conversion 256 -> 32 niveaux et création des histogrammes
    histoR = np.histogram(Rarray, 32, (0.0, 256.0))
    histoG = np.histogram(Garray, 32, (0.0, 256.0))
    histoB = np.histogram(Barray, 32, (0.0, 256.0))

    # concaténation des 3 quantifications en un seul vecteur de dimension D
    histogramme = np.append(histoR[0], [histoG[0], histoB[0]])

    plt.plot(histogramme)
    plt.title(f"Descripteur d'une image à partir d'un histogramme de couleur")
    plt.show()

    return(histogramme)