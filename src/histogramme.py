from PIL import Image
from IPython.display import display


image_path = "RGB.jpg"
image = Image.open(image_path)
display(image)

# conversion de l'image en 3 tableaux R,G,B

# conversion 256 -> 32 niveaux

# quantification

# concaténation des 3 quantifications en un seul vecteur de dimension D
