#!/usr/bin/env python3
from ftplib import FTP

# FTP_get_photo function
def FTP_get_Photos(file_list):
    # FTP connection
    try:
        ftp = FTP('192.168.0.1', 'photomatonprinterftp', 'photomatonprinterftp')
    except:
        print("FTP server connection error")
        return

    ftp.cwd('/volume')  # go to the directory
#    print(ftp.dir())
    list_file_on_server = []
    ftp.retrlines('NLST', list_file_on_server.append)  # Get list of all files in directory
#    print(list_file_on_server)
    download_finished = False
    retry = 0
    while download_finished == False and retry < 10:
        try:
            for index_photo in range(len(list_file_on_server)):
                if not list_file_on_server[index_photo] in file_list:
                    ftp.retrbinary('RETR ' + list_file_on_server[index_photo], open(list_file_on_server[index_photo], 'wb').write)
                    print("photo ", list_file_on_server[index_photo], "downloaded")
                    file_list.append(list_file_on_server[index_photo])
#                else:
#                    print("photo ", list_file_on_server[index_photo], "already downloaded")
            download_finished = True
        except:
            retry = retry + 1
            print("Error while downloading ", list_file_on_server[index_photo])

#    print('Closing FTP connection')
    ftp.close()
    return file_list