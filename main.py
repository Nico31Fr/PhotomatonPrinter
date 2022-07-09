#!/usr/bin/env python3
import PySimpleGUI as Sg
import os
import cups
import io
import time
from PIL import Image, ImageOps

# project import
import ftp_connection

_IMAGE_FF_L_: int = 2280  # 2592-2280 = 312/2 = 156
_IMAGE_FF_H_: int = 1520
_IMAGE_L_: int = 570
_IMAGE_H_: int = 380
_IM2PRINT_H_: int = int(_IMAGE_FF_H_ / 2)
_IM2PRINT_L_: int = int(_IMAGE_FF_L_ / 2)

# _OFFSET_FF_: int = 100
# _OFFSETCADRE_FF_: int = 5
# _OFFSET_: int = int(_OFFSET_FF_/5)
# _OFFSETCADRE_: int = int(_OFFSETCADRE_FF_/5)

_OFFSET_FF_: int = 20
_OFFSETCADRE_FF_: int = 0
_OFFSET_: int = int(_OFFSET_FF_ / 5)
_OFFSETCADRE_: int = int(_OFFSETCADRE_FF_ / 5)

_FILE2PRINT_ = '/home/nicolas/PycharmProjects/PhotomatonPrinter/tmp/Image2Print.png'
_PRINTERNAME_ = 'Canon_SELPHY_CP1300_USB_'

# Setting the points for cropped image
CROP_L = 156
CROP_T = 0
CROP_R = 156
CROP_B = 0
# Setting the points for cropped 4 image
_CROP_4_L_ = 156
_CROP_4_T_ = 0
_CROP_4_R_ = 156
_CROP_4_B_ = 0


def get_image_as_data(filename, deffilter, width=None, height=None):
    # from PIL import Image
    # use `pip install Pillow` to install PIL
    # import io
    im = Image.open(filename)
    im.putalpha(255)
    # Setting the points for cropped image
    iwidth, iheight = im.size
    im = im.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    if isinstance(width, int) and isinstance(height, int):  # Resize if dimensions provided
        im = im.resize((width, height))
        if deffilter == 'nb':
            im = ImageOps.grayscale(im)
    im_bytes = io.BytesIO()
    im.save(im_bytes, format="PNG")
    return im_bytes.getvalue()


def get_4_image_as_data_with_border(filename, deffilter, width=None, height=None):
    new_im = Image.new('RGB', (width, height))
    im1 = Image.open(filename[0])
    im2 = Image.open(filename[1])
    im3 = Image.open(filename[2])
    im4 = Image.open(filename[3])
    im1.putalpha(255)
    im2.putalpha(255)
    im3.putalpha(255)
    im4.putalpha(255)
    iwidth, iheight = im1.size
    im1 = im1.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    im2 = im2.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    im3 = im3.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    im4 = im4.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    #    cadre = Image.open("./Graphics/cadre.png")
    if isinstance(width, int) and isinstance(height, int):  # Resize if dimensions provided
        im1 = im1.resize((int((width - (3 * _OFFSET_)) / 2), int((height - (3 * _OFFSET_)) / 2)))
        im2 = im2.resize((int((width - (3 * _OFFSET_)) / 2), int((height - (3 * _OFFSET_)) / 2)))
        im3 = im3.resize((int((width - (3 * _OFFSET_)) / 2), int((height - (3 * _OFFSET_)) / 2)))
        im4 = im4.resize((int((width - (3 * _OFFSET_)) / 2), int((height - (3 * _OFFSET_)) / 2)))
        #        cadre = cadre.resize((width, height))
        if deffilter == 'nb':
            im1 = ImageOps.grayscale(im1)
            im2 = ImageOps.grayscale(im2)
            im3 = ImageOps.grayscale(im3)
            im4 = ImageOps.grayscale(im4)
    new_im.paste(im1, (_OFFSET_, _OFFSET_))
    new_im.paste(im2, ((int((width - (3 * _OFFSET_)) / 2) + 2 * _OFFSET_), _OFFSET_))
    new_im.paste(im3, (_OFFSET_, int(((height - (3 * _OFFSET_)) / 2) + 2 * _OFFSET_)))
    new_im.paste(im4, (
        (int((width - (3 * _OFFSET_)) / 2) + 2 * _OFFSET_), int(((height - (3 * _OFFSET_)) / 2) + 2 * _OFFSET_)))
    #    new_im.paste(cadre, (0, 0), cadre)
    im_bytes = io.BytesIO()
    new_im.save(im_bytes, format="PNG")
    return im_bytes.getvalue()


def get_image_as_data_with_border(filename, deffilter, width=None, height=None):
    im = Image.open(filename)
    im.putalpha(255)
    iwidth, iheight = im.size
    im = im.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    #    cadre = Image.open("./Graphics/cadre.png")
    if isinstance(width, int) and isinstance(height, int):  # Resize if dimensions provided
        im = im.resize((width, height))
        #        cadre = cadre.resize((width, height))
        if deffilter == 'nb':
            im = ImageOps.grayscale(im)
    #    im.paste(cadre, (0, 0), cadre)
    im_bytes = io.BytesIO()
    im.save(im_bytes, format="PNG")
    return im_bytes.getvalue()


def get_image_files_list(folder):
    all_files = os.listdir(folder)
    image_files = []
    for file in all_files:
        extension = file.lower().split(".")[-1]
        if extension in ["jpg", "png", "jpeg", "jpe"] and not file == default_pic:
            image_files.append(file)
    image_files.sort()
    return image_files


def print_4_photo(filename, deffilter, width=None, height=None):
    new_im = Image.new('RGB', (width, height))
    im1 = Image.open(filename[0])
    im2 = Image.open(filename[1])
    im3 = Image.open(filename[2])
    im4 = Image.open(filename[3])
    #    im1.putalpha(255)
    #    im2.putalpha(255)
    #    im3.putalpha(255)
    #    im4.putalpha(255)
    iwidth, iheight = im1.size
    im1 = im1.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    im2 = im2.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    im3 = im3.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    im4 = im4.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    #    cadre = Image.open("./Graphics/cadre.png")
    if isinstance(width, int) and isinstance(height, int):  # Resize if dimensions provided
        im1 = im1.resize((int((width - (3 * _OFFSET_FF_)) / 2), int((height - (3 * _OFFSET_FF_)) / 2)))
        im2 = im2.resize((int((width - (3 * _OFFSET_FF_)) / 2), int((height - (3 * _OFFSET_FF_)) / 2)))
        im3 = im3.resize((int((width - (3 * _OFFSET_FF_)) / 2), int((height - (3 * _OFFSET_FF_)) / 2)))
        im4 = im4.resize((int((width - (3 * _OFFSET_FF_)) / 2), int((height - (3 * _OFFSET_FF_)) / 2)))
    if deffilter == 'nb':
        im1 = ImageOps.grayscale(im1)
        im2 = ImageOps.grayscale(im2)
        im3 = ImageOps.grayscale(im3)
        im4 = ImageOps.grayscale(im4)
    new_im.paste(im1, (_OFFSET_FF_, _OFFSET_FF_))
    new_im.paste(im2, ((int((width - (3 * _OFFSET_FF_)) / 2) + 2 * _OFFSET_FF_), _OFFSET_FF_))
    new_im.paste(im3, (_OFFSET_FF_, int(((height - (3 * _OFFSET_FF_)) / 2) + 2 * _OFFSET_FF_)))
    new_im.paste(im4, ((int((width - (3 * _OFFSET_FF_)) / 2) + 2 * _OFFSET_FF_),
                       int(((height - (3 * _OFFSET_FF_)) / 2) + 2 * _OFFSET_FF_)))
    #    new_im.paste(cadre, (0, 0), cadre)
    new_im.save(_FILE2PRINT_, format="PNG")
    im1.close()
    im2.close()
    im3.close()
    im4.close()
    new_im.close()
    startprint()


def print_1_photo(filename, deffilter):
    im = Image.open(filename)
    #    im.putalpha(255)
    iwidth, iheight = im.size
    im = im.crop((CROP_L, CROP_T, iwidth - CROP_R, iheight - CROP_B))
    #    cadre = Image.open("./Graphics/cadre.png")
    if deffilter == 'nb':
        im = ImageOps.grayscale(im)
    #    im.paste(cadre, (0, 0), cadre)
    im.save(_FILE2PRINT_, format="PNG")
    im.close()
    startprint()


def startprint():
    if os.path.isfile(_FILE2PRINT_):
        # Open a connection to cups
        conn = cups.Connection()
        printers = conn.getPrinters()

        if _PRINTERNAME_ not in printers:
            print("imprimante %s non connecté" % _PRINTERNAME_)
            Sg.popup("imprimante non connecté", title='Erreur', auto_close=True, auto_close_duration=10, button_type=5, keep_on_top=True)
            return

        print("Impression en cours sur ", conn)
        time.sleep(1)
        # print the buffer file
        printqueuelength = len(conn.getJobs())
        if printqueuelength > 1:
            print("Impression impossible")
            Sg.popup('Impression impossible', title='Erreur', auto_close=True, auto_close_duration=10, button_type=5)
        else:
            try:
                print("impression")
                pid = conn.printFile(_PRINTERNAME_, _FILE2PRINT_, "PhotoBooth", {})
                while conn.getJobs().get(pid, None) is not None:
                    Sg.popup_animated('Graphics/animat-printer-color.gif',
                                      message='Impression en cours',
                                      no_titlebar=False, time_between_frames=100, text_color='black',
                                      background_color='white')
                Sg.popup_animated(None)  # close all Animated Popups
                print("impression OK")
            except:
                print("impression erreur ")


def photo_picker(default_folder, default_picture):
    folder = default_folder
    preview_image = default_picture
    list_image = [default_picture, default_picture, default_picture, default_picture]
    index_cadre = 0
    list_file_local: list = []
    imagefilter = "color"
    nbimageinlist = 0

    image_add = './icons/add.png'
    image_remove = './icons/back.png'
    image_imprimante = './icons/imprimante.png'

    list_file_local = ftp_connection.FTP_get_Photos(list_file_local)
    files_listing = get_image_files_list(folder)

    column1 = [
        #        [
        #            Sg.FolderBrowse('Configuration', key="-CONFIGURATION-")
        #        ],
        [
            Sg.Listbox(values=files_listing,
                       change_submits=True,  # trigger an event whenever an item is selected
                       size=(12, 55),
                       font=("Helvetica", 12),
                       key="files_listbox")
        ]
    ]
    frame_preview = [[Sg.Image(data=get_image_as_data(default_picture, imagefilter, _IMAGE_L_, _IMAGE_H_), key="image",
                               size=(_IMAGE_L_, _IMAGE_H_))]]
    column2 = [
        [Sg.Text('', background_color='white')],
        [Sg.Image(r'./Graphics/Instruction1.png', background_color='white')],
        [Sg.Text('', background_color='white')],
        [Sg.Text('', background_color='white')],
        [Sg.Frame('', frame_preview, background_color='white', relief=Sg.RELIEF_SOLID, border_width=5)]
    ]
    column3 = [
        [Sg.Text(' ', background_color='white')],
        [Sg.Image(r'./Graphics/Instruction2.png', background_color='white')],
        [Sg.Text(' ', background_color='white')],
        [Sg.Text(' ', background_color='white')],
        [Sg.Text(' ', background_color='white')],
        [Sg.Text(' ', background_color='white')],
        [Sg.Text(' ', background_color='white')],
        [Sg.Text(' ', background_color='white')],
        [Sg.Text(' ', background_color='white')],
        [Sg.Button(image_filename=image_add, image_size=(100, 72), image_subsample=2, key='-ADD-')],
        [Sg.Button(image_filename=image_remove, image_size=(100, 72), image_subsample=2, key='-REM-')]
    ]
    frame_compo = [[Sg.Image(data=get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_),
                             key="assambledImage", size=(_IMAGE_L_, _IMAGE_H_), background_color='Black')]]
    column4 = [
        [Sg.Text(' ', background_color='white')],
        [Sg.Image(r'./Graphics/Instruction3.png', background_color='white')],
        [Sg.Text(' ', background_color='white')],
        [Sg.Checkbox('Noir et Blanc', key="-NB-", default=False, enable_events=True, background_color='white',
                     text_color='black', font=("Helvetica", 14), ),
         Sg.Radio("Une Photo", 'NB_PHOTO', key="-1p-", default=True, enable_events=True, background_color='white',
                  text_color='black', font=("Helvetica", 14), ),
         Sg.Radio("Quatre Photos", 'NB_PHOTO', key="-4p-", enable_events=True, background_color='white',
                  text_color='black', font=("Helvetica", 14), )],
        [Sg.Frame('', frame_compo, background_color='white', relief=Sg.RELIEF_SOLID, border_width=5)],
        [Sg.Image(r'./Graphics/Instruction4.png', background_color='white'),
         Sg.Button(image_filename=image_imprimante, image_size=(200, 200), image_subsample=2, key='-IMPRESSION-')]
    ]

    layout = [
        [
            Sg.Column(column1, background_color='white'),
            Sg.Column(column2, background_color='white', element_justification='center', vertical_alignment='top'),
            Sg.Column(column3, background_color='white', element_justification='center', vertical_alignment='top'),
            Sg.Column(column4, background_color='white', element_justification='center', vertical_alignment='top')
        ]
    ]

    Sg.theme('lightGrey1')
    Sg.theme_border_width(0)  # make all element flat
    window = Sg.Window('Photomaton Printer App', layout, resizable=True, finalize=True)

    window.maximize()
    window.make_modal()
    window.keep_on_top_set()

    while True:

        event, values = window.Read(timeout=10000)

        list_file_local = ftp_connection.FTP_get_Photos(list_file_local)
        image_files = get_image_files_list(folder)

        if image_files.__len__() != nbimageinlist:
            nbimageinlist = image_files.__len__()
            # print(nbimageinlist)
            window.find_element("files_listbox").Update(values=image_files)

        # print(event)
        #        if values['-CONFIGURATION-']:
        #            if os.path.isdir(values["-CONFIGURATION-"]):
        #                folder = values["-CONFIGURATION-"]
        #                if len(image_files) > 0:
        #                    if isinstance(preview_image, int):
        #                        preview_image = os.path.join(folder, image_files[0])
        #                    window.find_element("image").Update(data=get_image_as_data(preview_image, 'color', _IMAGE_L_, _IMAGE_H_))
        if event == "files_listbox":
            preview_image = os.path.join(folder, values["files_listbox"][0])
            window.find_element("image").Update(data=get_image_as_data(preview_image, 'color', _IMAGE_L_, _IMAGE_H_))
        if event == "-ADD-":
            list_image[index_cadre] = preview_image
            if values['-4p-']:
                if index_cadre < 3:
                    index_cadre = index_cadre + 1
                window.find_element("assambledImage").Update(
                    data=get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
            else:
                window.find_element("assambledImage").Update(
                    data=get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))
        if event == "-REM-":
            print(index_cadre)
            list_image[index_cadre] = default_pic
            if index_cadre > 0 and values['-4p-']:
                index_cadre = index_cadre - 1
                window.find_element("assambledImage").Update(
                    data=get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
            else:
                window.find_element("assambledImage").Update(
                    data=get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))
        if event == "-NB-":
            if values['-NB-']:
                imagefilter = 'nb'
                if index_cadre > 0 and values['-4p-']:
                    window.find_element("assambledImage").Update(
                        data=get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
                else:
                    window.find_element("assambledImage").Update(
                        data=get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))
            else:
                imagefilter = 'color'
                if index_cadre > 0 and values['-4p-']:
                    window.find_element("assambledImage").Update(
                        data=get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
                else:
                    window.find_element("assambledImage").Update(
                        data=get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))
        if event == "-1p-":
            index_cadre = 0
            list_image = [default_picture, default_picture, default_picture, default_picture]
            window.find_element("assambledImage").Update(
                data=get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))
        if event == "-4p-":
            index_cadre = 0
            list_image = [default_picture, default_picture, default_picture, default_picture]
            window.find_element("assambledImage").Update(
                data=get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
        if event == "-IMPRESSION-":
            if index_cadre > 0 and values['-4p-']:
                print_4_photo(list_image, imagefilter, _IMAGE_FF_L_, _IMAGE_FF_H_)
            else:
                print_1_photo(list_image[0], imagefilter)
        if event == Sg.WIN_CLOSED:
            break


if __name__ == "__main__":
    default_pic = "image.jpg"
    photo_picker(".", default_pic)
