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

def downloadImages():
    path = pathlib.Path(__file__).parent.absolute()

    if exists("images"):
        dir = os.listdir("images")
        if len(dir) != 0:
            print()
            texto = input("El directorio \"images\" no está vacio ¿Desea borrar su contenido?[S/N]: ")
            if texto.capitalize() == "S":
                shutil.rmtree(os.path.join(path, "images"))
                os.mkdir("images")
            else:
                print("No se puede continuar si el directorio \"images\" no está vacio")
                raise SystemExit(0)
    else:
        print("Creando directorio de imágenes...")
        os.mkdir("images")
    
    print("Descargarndo imágenes de SlideShare...")
    for i in range(1,22):
        url = "https://image.slidesharecdn.com/plandecontingencia-140605102313-phpapp01/95/plan-de-contingencia-" + str(i) + "-638.jpg?cb=1401963929"

        img_data = requests.get(url).content
        imagePath = os.path.join(path, "images")
        imagePath = os.path.join(imagePath, "image-" + str(i) + ".jpg")
        with open(imagePath, 'wb') as handler:
            handler.write(img_data)

def makePDF():
    print("Creando PDF...")
    path = pathlib.Path(__file__).parent.absolute()
    #imagesJPG = list()
    imagesRGB = list()
    for i in range(1,20):
        imagePath = os.path.join(path, "images")
        imagePath = os.path.join(imagePath, "image-" + str(i) + ".jpg")
        image = Image.open(imagePath)
        imagesRGB.append(image.convert("RGB"))
        
    pdfPath = os.path.join(path, "images")
    pdfPath = os.path.join(pdfPath, "image-0.jpg")
    imagesRGB[0].save("result.pdf", save_all=True, append_images=imagesRGB)
    print("Se ha creado el PDF \"result.pdf\"")

def main():
    os.path.join(os.path.dirname(__file__))
    downloadImages()
    makePDF()

if __name__ == "__main__":
    main()