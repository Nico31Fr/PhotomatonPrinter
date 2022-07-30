#!/usr/bin/env python3
from ftplib import FTP, all_errors
import os


# FTP_get_photo function
def ftp_get_photos(file_list, destination=".", time_out=10):
    # FTP connection
    try:
        ftp = FTP('192.168.0.1', 'photomatonprinterftp', 'photomatonprinterftp', timeout=time_out)
    except all_errors as e:
        print("FTP server connection error [%s] _ continue without FTP transfert" % e)
        return "__ERROR__"

    ftp.cwd('/volume')  # go to the directory
    #    print(ftp.dir())
    list_file_on_server = []
    ftp.retrlines('NLST', list_file_on_server.append)  # Get list of all files in directory
    #    print(list_file_on_server)
    download_finished = False
    retry = 0
    while download_finished is False and retry < 10:
        try:
            for index_photo in range(len(list_file_on_server)):
                if not list_file_on_server[index_photo] in file_list:
                    local_filename = os.path.join(destination, list_file_on_server[index_photo])
                    ftp.retrbinary('RETR ' + list_file_on_server[index_photo],
                                   open(local_filename, 'wb').write)
                    print("photo ", local_filename, "downloaded")
                    file_list.append(list_file_on_server[index_photo])
            download_finished = True
        except all_errors as e:
            retry = retry + 1
            print("Error while downloading[%s]" % e)
    #    print('Closing FTP connection')
    ftp.close()
    return file_list
