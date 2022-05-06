# Iba a comentar este código, pero me ha dado mucha pereza así que así se queda
try:
    import requests
except:
    print("Es necesario instalar el módulo requests\nLo puedes instalar con \"pip install requests\"")
    raise SystemExit
from genericpath import exists
from gettext import install
import os
import shutil
try:
    from PIL import Image
except:
    print("Es necesario instalar el módulo PIL\nLo puedes instalar con \"pip install Pillow\"")
    raise SystemExit(0)
import pathlib
import re

def downloadImages(image1):
    #path = pathlib.Path(__file__).parent.absolute()

    if exists("images"):
        dir = os.listdir("images")
        if len(dir) != 0:
            print()
            texto = input("El directorio \"images\" no está vacio ¿Desea borrar su contenido?[S/N]: ")
            if texto.capitalize() == "S":
                shutil.rmtree("images")
                os.mkdir("images")
            else:
                print("No se puede continuar si el directorio \"images\" no está vacio")
                raise SystemExit(0)
    else:
        print("Creando directorio de imágenes...")
        os.mkdir("images")
    
    print("Descargarndo imágenes de SlideShare...")
    urlParts = re.split(r'-1-1024.jpg', image1)
    i = 1
    while(True):
        #url = "https://image.slidesharecdn.com/plandecontingencia-140605102313-phpapp01/95/plan-de-contingencia-" + str(i) + "-1024.jpg?cb=1401963929 1024w"
        url = urlParts[0] + "-" + str(i) + "-1024.jpg" + urlParts[1]

        img_data = requests.get(url).content
        if (img_data == b''):
            break
        
        #imagePath = os.path.join(path, "images")
        imagePath = os.path.join("images", "image-" + str(i) + ".jpg")
        with open(imagePath, 'wb') as handler:
            handler.write(img_data)
        i+=1
    return i

def makePDF(numImagenes):
    print("Creando PDF...")
    #path = pathlib.Path(__file__).parent.absolute()
    #imagesJPG = list()
    imagesRGB = list()
    for i in range(1,numImagenes + 1):
        #imagePath = os.path.join(path, "images")
        imagePath = os.path.join("images", "image-" + str(i) + ".jpg")
        image = Image.open(imagePath)
        imagesRGB.append(image.convert("RGB"))
        
    #pdfPath = os.path.join(path, "images")
    pdfPath = os.path.join("images", "image-0.jpg")
    imagesRGB[0].save("result.pdf", save_all=True, append_images=imagesRGB[1:])
    print("Se ha creado el PDF \"result.pdf\"")

def main():
    # https://www.slideshare.net/ericschmidt/trillion-dollar-coach-book-bill-campbell
    url = input("Introduce la url del slideshare que deseas descargar: ")
    text = requests.get(url).text
    image1 = ""
    try:
        image1 = re.findall(r'https://image.slidesharecdn.com[^".]*1024[^"]*"', text)[0][:-1]
    except:
        print("Ha habido un error")
        raise SystemExit(0)

    numIagenes = downloadImages(image1)
    makePDF(numIagenes - 1)

if __name__ == "__main__":
    main()