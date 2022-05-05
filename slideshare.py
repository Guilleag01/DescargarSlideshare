try:
    import requests
except:
    install("requests")
from gettext import install
import os
import shutil
try:
    from PIL import Image
except:
    install("Pillow")

import pathlib



def downloadImages():
    path = pathlib.Path(__file__).parent.absolute()
    try:
        shutil.rmtree(os.path.join(path, "images"))
    except:
        print("Creando directorio de imágenes...")
    os.mkdir("images")
    for i in range(1,22):
        url = "https://image.slidesharecdn.com/plandecontingencia-140605102313-phpapp01/95/plan-de-contingencia-" + str(i) + "-638.jpg?cb=1401963929"

        img_data = requests.get(url).content
        imagePath = os.path.join(path, "images")
        imagePath = os.path.join(imagePath, "image-" + str(i) + ".jpg")
        with open(imagePath, 'wb') as handler:
            handler.write(img_data)

def makePDF():
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

def main():
    path = pathlib.Path(__file__).parent.absolute()
    # print(os.path.join(path,"images"))
    downloadImages()
    makePDF()


if __name__ == "__main__":
    main()