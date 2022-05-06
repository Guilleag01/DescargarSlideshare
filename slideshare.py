# Iba a comentar este código, pero me ha dado mucha pereza así que así se queda
# Bueno, al final he comentado un poco porque me estaba poniendo nervioso
try:
    import requests
except:
    print("Es necesario instalar el módulo requests\nLo puedes instalar con \"pip install requests\"")
    raise SystemExit
from genericpath import exists
from gettext import install
import os
import shutil
from time import sleep
try:
    from PIL import Image
except:
    print("Es necesario instalar el módulo PIL\nLo puedes instalar con \"pip install Pillow\"")
    raise SystemExit(0)
import pathlib
import re

def downloadImages(image1, count):
    # Comprobación de si existe la carpeta images
    # y en caso de que exista preguntar al usuario
    # si quiere borrarla.
    if exists("images"):
        dir = os.listdir("images")
        if len(dir) != 0:
            print()
            texto = input("El directorio \"images\" no está vacio ¿Desea borrar su contenido? [S/n]: ")
            if texto.capitalize() == "S" or texto == "":
                shutil.rmtree("images")
                os.mkdir("images")
            else:
                print("No se puede continuar si el directorio \"images\" no está vacio")
                raise SystemExit(0)
    else:
        print("Creando directorio de imágenes...")
        os.mkdir("images")

    print("\nDescargarndo imágenes de SlideShare...")

    # Se separa la url para poder modificar el número
    # de imágen mas adelante
    urlParts = re.split(r'-1-1024.jpg', image1)
    
    i = 1
    while(True):
        # Todo el tema de la barra de carga
        longBarra = 50
        print("\r|", end = "")
        barra = int((i - 1) * longBarra / count)
        for j in range(barra):
            print("█", end = "")
        for j in range(longBarra-barra):
            print(" ", end = "")
        print("| " + "{:.2f}".format((i - 1) * 100 / count) + "% (" + str(i - 1) + " / " + str(count) + ")" , end = "")

        # Se reconstruye la url con el número de imágen
        # correspondiente y se descarga la imágen
        url = urlParts[0] + "-" + str(i) + "-1024.jpg" + urlParts[1]
        img_data = requests.get(url).content

        # Si la imágen está vacia es que ya no hay mas diapositivas
        if (img_data == b''):
            break
        
        # Guarda la imágen en la carpeta images con el nombre que 
        # corresponda
        imagePath = os.path.join("images", "image-" + str(i) + ".jpg")
        with open(imagePath, 'wb') as handler:
            handler.write(img_data)
        i+=1
    return i

def makePDF(numImagenes):
    print("\nCreando PDF...")
    imagesRGB = list()

    # Se abren las imágenes, se convierten a RGB y se almacenan en una lista
    for i in range(1,numImagenes + 1):
        imagePath = os.path.join("images", "image-" + str(i) + ".jpg")
        image = Image.open(imagePath)
        imagesRGB.append(image.convert("RGB"))
        
    # Se crea el pdf en base a las imágenes de la lista
    pdfPath = os.path.join("images", "image-0.jpg")
    imagesRGB[0].save("result.pdf", save_all=True, append_images=imagesRGB[1:])
    print("Se ha creado el PDF \"result.pdf\"")

def main():
    url = input("Introduce la url del slideshare que deseas descargar: ")
    text = requests.get(url).text
    image1 = ""
    num = 0
    images = list()
    try:
        images = re.findall(r'https://image.slidesharecdn.com[^".]*1024[^"]*"', text)
        image1 = images[0][:-1]
        num = len(images) - 1
    except:
        print("Ha habido un error")
        raise SystemExit(0)

    numIagenes = downloadImages(image1, num)
    print("")
    makePDF(numIagenes - 1)

if __name__ == "__main__":
    main()