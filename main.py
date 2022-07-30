#!/usr/bin/env python3
############################################################
#
# Protomaton Printer Satation V1.0 by N.Cot
#
############################################################

import PySimpleGUI as Sg
import os
import cups
import time
import io
from PIL import Image

# project import
import ftp_connection
import image

_IMAGE_FF_L_: int = 2280
_IMAGE_FF_H_: int = 1520
_IMAGE_L_: int = int(_IMAGE_FF_L_/4)
_IMAGE_H_: int = int(_IMAGE_FF_H_/4)

_FILE2PRINT_ = '/home/nicolas/PycharmProjects/PhotomatonPrinter/tmp/Image2Print.png'
_PRINTERNAME_ = 'Canon_SELPHY_CP1300_USB_'


def print_4_photo(filename, deffilter, wind):
    data_bytes_io = io.BytesIO(image.get_4_image_as_data_with_border(filename, deffilter, _IMAGE_FF_L_, _IMAGE_FF_H_))
    img = Image.open(data_bytes_io)
    img.save(_FILE2PRINT_, format="PNG")
    return startprint(wind)


def print_1_photo(filename, deffilter, wind):
    data_bytes_io = io.BytesIO(image.get_image_as_data_with_border(filename, deffilter, _IMAGE_FF_L_, _IMAGE_FF_H_))
    img = Image.open(data_bytes_io)
    img.save(_FILE2PRINT_, format="PNG")
    return startprint(wind)


def startprint(wind):

    if os.path.isfile(_FILE2PRINT_):
        # Open a connection to cups
        conn = cups.Connection()
        printers = conn.getPrinters()

        if _PRINTERNAME_ not in printers:
            print("imprimante %s non connecté" % _PRINTERNAME_)
            wind['_LOG_'].Update("imprimante %s non connecté" % _PRINTERNAME_)
            return

        print("Impression en cours sur ", conn)
        time.sleep(1)
        # print the buffer file
        printqueuelength = len(conn.getJobs())
        if printqueuelength > 1:
            print("Impression impossible")
            wind['_LOG_'].Update('Impression impossible')
            return
        else:
            try:
                print("impression")
                pid = conn.printFile(_PRINTERNAME_, _FILE2PRINT_, "PhotoBooth", {})
                while conn.getJobs().get(pid, None) is not None:
                    Sg.popup_animated('Graphics/animat-printer-color.gif',
                                      message='Impression en cours',
                                      no_titlebar=False, time_between_frames=100, text_color='black',
                                      background_color='white',
                                      keep_on_top=True)
                Sg.popup_animated(None)  # close all Animated Popups
                print("impression OK")
            except IOError as e:
                print("impression erreur %s" % e)


def photo_picker(default_folder, default_picture):

    folder = default_folder
    preview_image = default_picture
    list_image = [default_picture, default_picture, default_picture, default_picture]
    index_cadre = 0
    list_file_local: list = []
    imagefilter = "color"
    nbimageinlist = 0
    ftp_error_detected = False

    image_add = './icons/add.png'
    image_remove = './icons/back.png'
    image_imprimante = './icons/imprimante.png'

    list_file_local = ftp_connection.ftp_get_photos(list_file_local, destination=default_folder)
    if list_file_local == "__ERROR__":
        ftp_error_detected = True
    files_listing = image.get_image_files_list(folder, default_picture)

    column1 = [[Sg.Listbox(values=files_listing,
                change_submits=True,  # trigger an event whenever an item is selected
                expand_y=True,
                font=("Helvetica", 12),
                key="files_listbox")]]

    frame_preview = [[Sg.Image(data=image.get_image_as_data(default_picture, _IMAGE_L_, _IMAGE_H_), key="image",
                               size=(_IMAGE_L_, _IMAGE_H_))]]
    frame_log = [[Sg.Text('Photomaton Printer Station V0.1', text_color='black', key='_LOG_', background_color='white', size=100, border_width=5, relief='groove')]]

    column2 = [
        [Sg.Image(r'./Graphics/Instruction1.png', background_color='white')],
        [Sg.Text('', background_color='white')],
        [Sg.Text('', background_color='white')],
        [Sg.Frame('', frame_preview, background_color='white', relief=Sg.RELIEF_SOLID, border_width=5)],
        [Sg.VPush(background_color='White')],
        [Sg.Frame('', frame_log, background_color='white', border_width=0)]
    ]
    column3 = [
        [Sg.Image(r'./Graphics/Instruction2.png', background_color='white')],
        [Sg.VPush(background_color='White')],
        [Sg.Button(image_filename=image_add, image_size=(100, 72), image_subsample=2, key='-ADD-')],
        [Sg.Button(image_filename=image_remove, image_size=(100, 72), image_subsample=2, key='-REM-')],
        [Sg.VPush(background_color='White')],
        [Sg.VPush(background_color='White')]
    ]
    frame_compo = [[Sg.Image(data=image.get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_),
                             key="assambledImage", size=(_IMAGE_L_, _IMAGE_H_), background_color='Black')]]
    column4 = [
        [Sg.Image(r'./Graphics/Instruction3.png', background_color='white')],
        [Sg.Text('', background_color='white')],
        [Sg.Checkbox('Noir et Blanc', key="-NB-", default=False, enable_events=True, background_color='white',
                     text_color='black', font=("Helvetica", 14), ),
         Sg.Radio("Une Photo", 'NB_PHOTO', key="-1p-", default=True, enable_events=True, background_color='white',
                  text_color='black', font=("Helvetica", 14), ),
         Sg.Radio("Quatre Photos", 'NB_PHOTO', key="-4p-", enable_events=True, background_color='white',
                  text_color='black', font=("Helvetica", 14), )],
        [Sg.Frame('', frame_compo, background_color='white', relief=Sg.RELIEF_SOLID, border_width=5)],
        [Sg.VPush(background_color='White')],
        [Sg.Image(r'./Graphics/Instruction4.png', background_color='white'),
         Sg.Button(image_filename=image_imprimante, image_size=(200, 200), image_subsample=2, key='-IMPRESSION-')],
        [Sg.VPush(background_color='White')]
    ]

    layout = [
        [
            Sg.Column(column1, background_color='white', expand_y=True),
            Sg.Column(column2, background_color='white', element_justification='center', vertical_alignment='top', expand_y=True),
            Sg.Column(column3, background_color='white', element_justification='center', vertical_alignment='top', expand_y=True),
            Sg.Column(column4, background_color='white', element_justification='center', vertical_alignment='top', expand_y=True)
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

        if ftp_error_detected is False:
            list_file_local = ftp_connection.ftp_get_photos(list_file_local, destination=default_folder, time_out=5)

        image_files = image.get_image_files_list(folder, default_picture)

        if image_files.__len__() != nbimageinlist:
            nbimageinlist = image_files.__len__()
            window.find_element("files_listbox").Update(values=image_files)

        if event == "files_listbox":
            preview_image = os.path.join(folder, values["files_listbox"][0])
            window.find_element("image").Update(data=image.get_image_as_data(preview_image, _IMAGE_L_, _IMAGE_H_))

        if event == "-ADD-":
            list_image[index_cadre] = preview_image
            if values['-4p-']:
                if index_cadre < 3:
                    index_cadre = index_cadre + 1
                window.find_element("assambledImage").Update(
                    data=image.get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
            else:
                window.find_element("assambledImage").Update(
                    data=image.get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))

        if event == "-REM-":
            print(index_cadre)
            list_image[index_cadre] = default_pic
            if values['-4p-']:
                index_cadre = index_cadre - 1
                window.find_element("assambledImage").Update(
                    data=image.get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
            else:
                window.find_element("assambledImage").Update(
                    data=image.get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))

        if event == "-NB-":
            if values['-NB-']:
                imagefilter = 'nb'
                if values['-4p-']:
                    window.find_element("assambledImage").Update(
                        data=image.get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
                else:
                    window.find_element("assambledImage").Update(
                        data=image.get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))
            else:
                imagefilter = 'color'
                if values['-4p-']:
                    window.find_element("assambledImage").Update(
                        data=image.get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))
                else:
                    window.find_element("assambledImage").Update(
                        data=image.get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))

        if event == "-1p-":
            index_cadre = 0
            list_image = [default_picture, default_picture, default_picture, default_picture]
            window.find_element("assambledImage").Update(
                data=image.get_image_as_data_with_border(list_image[0], imagefilter, _IMAGE_L_, _IMAGE_H_))

        if event == "-4p-":
            index_cadre = 0
            list_image = [default_picture, default_picture, default_picture, default_picture]
            window.find_element("assambledImage").Update(
                data=image.get_4_image_as_data_with_border(list_image, imagefilter, _IMAGE_L_, _IMAGE_H_))

        if event == "-IMPRESSION-":
            if index_cadre > 0 and values['-4p-']:
                print_4_photo(list_image, imagefilter, window)
            else:
                print_1_photo(list_image[0], imagefilter, window)
                
        if event == Sg.WIN_CLOSED:
            break


if __name__ == "__main__":

    path_tmp = './tmp'
    path_photos = './photos'

    # Check whether the specified path exists or not
    isExist = os.path.exists(path_tmp)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path_tmp)
        print("The tmp directory is created!")

    isExist = os.path.exists(path_photos)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path_photos)
        print("The photos directory is created!")

    default_pic = "image.jpg"
    if not os.path.isfile(default_pic):
        print("default image not present _ exit")
        exit()

    photo_picker(path_photos, default_pic)
