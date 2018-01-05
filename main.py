
from PIL import Image, ImageDraw
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
import colorsys

def main():
    #Инициализация
    SIZE = 150
    DICT_RGB_COLOR = {}  
    DICT_LAB_COLOR = {} 

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

    #Создание итогового изображения
    space = (round((bg_w - img_w) / 2))
    horz_size = (img_w-(space*(k-1)))/k
    virt_size = (2*space)+img_h
    horizontal = space+horz_size
    posx = space
    background.save(infile+'final'+'.PNG')

main()
