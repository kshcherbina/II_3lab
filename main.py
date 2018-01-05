
from PIL import Image, ImageDraw
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import colorsys
from KMeans import *

def main():
    #Инициализация
    SIZE = 150
    DICT_RGB_COLOR = {}  
    DICT_LAB_COLOR = {} 

    centroid = []
    rgb_centroid = []

    infile = input('Название файла: ')
    k = int(input('Количество кластеров: '))
    image = Image.open(infile)

    img_w, img_h = image.size   
    background = Image.new('RGB', (round((img_w * 1.025)), round((img_h * 1.5))), 'white') 
    bg_w, bg_h = background.size
    offset = (round((bg_w - img_w) / 2), round((bg_w - img_w) / 2))
    background.paste(image, offset)

    image = image.convert('RGB')
    image = image.resize((SIZE, SIZE))
    image = image.convert('P', palette=Image.ADAPTIVE, colors=256)
    image.putalpha(0)

    rgb_color = image.getcolors(256) #Получение цветов из картинки
 
    # RGB dic
    i = 0
    for color in rgb_color:
        DICT_RGB_COLOR[i] = color
        i += 1

    # Lab dic
    for key in DICT_RGB_COLOR:
        DICT_LAB_COLOR[key] = (
        convert_color(sRGBColor(DICT_RGB_COLOR[key][1][0],DICT_RGB_COLOR[key][1][1],DICT_RGB_COLOR[key][1][2]),LabColor))

    #Кластеризация методом k-средних 

    #Инициализация списков
    for i in range(k):
        rgb_centroid.append([])
        centroid.append(DICT_LAB_COLOR[randrange(0, len(DICT_LAB_COLOR))])

    centroid = init_centroids(DICT_LAB_COLOR,k)

    for i in range(15):
        centroid = k_means(DICT_LAB_COLOR,DICT_RGB_COLOR,k,centroid)

    #Создание итогового изображения

    for i in range(k):    # Lab -> RGB
        rgb_centroid[i] = convert_color(centroid[i], sRGBColor)
        rgb_centroid[i] = rgb_centroid[i].get_value_tuple()
        rgb_centroid[i] = (round(rgb_centroid[i][0]),round(rgb_centroid[i][1]),round(rgb_centroid[i][2]))

    rgb_centroid.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
    draw2 = ImageDraw.Draw(background)
    space = (round((bg_w - img_w) / 2))
    horz_size = (img_w-(space*(k-1)))/k
    virt_size = (2*space)+img_h
    horizontal = space+horz_size
    posx = space

    #добавляем цвета на картинку нашу
    for i in range(k):
        draw2.rectangle([posx, virt_size, horz_size+posx, bg_h-space], fill=rgb_centroid[i])
        posx += horizontal

    del draw2

    background.save(infile+'-final'+'.PNG')

main()
