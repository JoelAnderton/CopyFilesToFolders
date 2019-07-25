#########################################################################################
# Created by: Joel Anderton
# Created date: 12/17/2018
#
# Purpose: To copy all Subject files (or a select list based off a .csv file) from
#         one location to another and allow for creating subfolders such as:
#             - Site folder (i.e. Colombia, Lancaster, Nigeria, Philippines, Pittsbrugh, Puerto Rico)
#             - a "Library" folder
#             - individual subject folders
# Updates:
#    12/17/2018:
#       - Made it into a GUI! (previous "MoveFiles" program was a console app)
#       - Allowed for various OFC2 style subfolders to be made#
#    12/19/2018
#       - Added the option use a .csv file to limit StudyIDs to copy 
#    12/20/2018
#       - Made it handle unidentified files that don't match the OFC2 style
#     1/3/2019
#       - WINDOWS version uses the ttk theme to create nicer Windows buttons
#     4/5/2019
#       - Added option to create an "Images" subfolder
#       - Made it so that StudyIDs in the filename become uppercase when the file moves
#       - Does not matter if the StudyIDs in a .csv file has StudyIDs as upper or lower case
#    6/3/2019
#       - Added the option to specify file naming conventions or file extensions
#       - Create a log of all file  moves that gets append everytime the program is run
#       - Create an option to create an individual log for an individual run of the program
#   6/10/2019
#       - Unified the separate python programs for Windows and Mac into 1 cross-platform program
#   7/18/2019
#       - Fix issue where if the file is lowercase, but the .csv had the StudyID as uppercase it would 
#       show on the log as both "Success" and "Failed" - one for the lowercase, one for the uppercase.
#       - Fix individual folders uppercase
#   7/20/2019
#       - Added "Mode" option to change between "Keep Originals" and "Remove Originals"
#   7/24/2019
#       - Fixed log.csv spaces that show in the front of string in each cell
#########################################################################################
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
import os
import shutil
import csv
import re
import datetime
import sys


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'MacOS',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


# Gets data from the "From here" text box
def get_fromData(event=None):
    global from_folder
    from_folder = askdirectory()
    fromEntry.insert(END, from_folder)


# Gets data from the "To here" text box
def get_toData(event=None):
    global to_folder
    to_folder = askdirectory()
    toEntry.insert(END, to_folder)  


# Gets data from the ".CSV" file text box
def get_csv(event=None):
    global csv_path
    global StudyID_list_from_csv
    StudyID_list_from_csv = []
    csv_path = askopenfilename()
    limitEntry.insert(END, csv_path)

    # opens .csv file
    with open(limitEntry.get(), 'r') as f:
            reader = csv.reader(f, delimiter=',')  # reads in .csv file
            for rowDict in reader:
                StudyID = rowDict[0].upper() # if the StudyID is typed in lowercase, this changes it to uppercase
                StudyID_list_from_csv.append(StudyID)


# Continuous log
def contin_log(moved_files, unable_to_move):
    if get_platform() != 'Windows':
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")

    if os.path.exists('log.csv') == False:
        with open('log.csv', 'a+') as log:
            log.writelines('Success/Fail, Date, StudyID, From Here, To Here')
            log.writelines('\n')

    with open('log.csv', 'a+') as log:
        for file in moved_files:
            log.writelines(file)
            log.writelines('\n')
        
        # Add in files that failed   
        if unable_to_move != []:
            for file in unable_to_move:
                log.writelines('FAIL!, ' + str(datetime.datetime.now()) + ',' + file)
                log.writelines('\n')


# Create a log file
def create_log(moved_files, unable_to_move):
    with asksaveasfile(mode='a+', defaultextension=".csv") as create_csv:
        create_csv.writelines('Success/Fail, Date, StudyID, From Here, To Here')
        create_csv.writelines('\n')
        for file in moved_files:
            create_csv.writelines(file)
            create_csv.writelines('\n')

        # Add in files that failed
        if unable_to_move != []:
            for file in unable_to_move:
                create_csv.writelines('FAIL!, ' + str(datetime.datetime.now()) + ',' + file)
                create_csv.writelines('\n')


# Creates the "About" window
def get_about(event=None):
    messagebox.showinfo('About', '''    Created by: Joel Anderton 
    Created date: 12/17/2018

    OFC2 Copy Files to Folders
    version: 4.0
    
    Only works with files with OFC2 style StudyIDs
    The first 7 characters of the file must be the StudyID

    Updates:
    12/17/2018 - v. 2.1:
    - Made it into a GUI!
      (previous "MoveFiles" program was a console app)
    - Allowed for various OFC2 style subfolders to be made

    12/19/2018 - v. 2.2:
    - Added the option use a .csv file to limit StudyIDs to copy

    4/5/2019 - v. 2.3:
    - Added option to create an "Images" subfolder
    - Made it so that StudyIDs in the filename become uppercase when
      the file moves
    - Does not matter if the StudyIDs in a .csv file has StudyIDs as upper 
      or lower case

    6/3/2019 - v. 3.1:
    - Added the option to specify file naming conventions or file 
      extensions
    - Create a log of all file moves
    
    7/20/2019 v. 4.0
    - Added "Mode" option to change between "Keep Originals" and 
      "Remove Originals"
    ''')


def get_submit(event=None):
    site_dic = {'CO':r'Colombia', 'LC': r'Lancaster', 'NG':r'Nigeria', 'PH':r'Philippines', 'FC':r'Pittsburgh', 'PR': r'Puerto Rico',
                'BE':r'Beijing', 'CL':r'Colorado', 'DK':r'Denmark', 'GF':r'Guatemala', 'GW':r'Iowa(George Webby)', 'HF':r'Hungery', 'IN':r'India', 
                'MF':r'Madrid', 'MV':r'Madrid', 'OZ':r'Australia','PT':r'Patagonia', 'SF':r'St.Louis', 'SH':r'Shanghai', 'TK':r'Turkey', 'TW':r'Twinsburg', 'TX':r'Texas'}
    moved_files = []
    unable_to_move =[]
    subject_list = []
    for root, dirs, files in os.walk(from_folder):
        for file in files:
            try:
                # limit and specifyBox are both null
                if limitEntry.get() == '' and specifyBox.get() == '': # is the limiting .csv file being used
                    # Determines if the file contains a StudyID: If so, it uppercases the first 2 letters. If not, it changes nothing 
                    pattern = r'[a-zA-Z][a-zA-z][0-9]{4,5}'
                    match = re.findall(pattern, file)
                    if match:
                        file = file[0:2].upper() + file[2:]
                        indiv_folder = match[0].upper()
                        subject_list.append(indiv_folder)
                    else:
                        continue
                 
                # limit is not null and and specifyBox is null
                elif limitEntry.get() != '' and specifyBox.get() == '':
                    if (file[0:7].upper() in StudyID_list_from_csv) or (file[0:6].upper() in StudyID_list_from_csv):
                        # Determines if the file contains a StudyID: If so, it uppercases the first 2 letters. If not, it changes nothing 
                        pattern = r'[a-zA-Z][a-zA-z][0-9]{4,5}'
                        match = re.findall(pattern, file)
                        if match:
                            file = file[0:2].upper() + file[2:]
                            indiv_folder = match[0].upper()
                            subject_list.append(indiv_folder)
                        else:
                            continue 
                    else:
                        continue

                # limit is null and specifyBox is not null
                elif limitEntry.get() == '' and specifyBox.get() != '':
                    if specifyBox.get().upper() in file.upper():
                        pattern = r'[a-zA-Z][a-zA-z][0-9]{4,5}'
                        match = re.findall(pattern, file)
                        if match :
                            file = file[0:2].upper() + file[2:]
                            indiv_folder = match[0].upper()
                            subject_list.append(indiv_folder)
                        else: 
                            continue
                    else:
                        continue

                # both limit and specifyBox are not null
                elif limitEntry.get() != '' and specifyBox.get() != '':
                    if (file[0:7].upper() in StudyID_list_from_csv and specifyBox.get().upper() in file.upper()) or (file[0:6].upper() in StudyID_list_from_csv and specifyBox.get().upper() in file.upper()):
                        pattern = r'[a-zA-Z][a-zA-z][0-9]{4,5}'
                        match = re.findall(pattern, file)
                        if match:
                           file = file[0:2].upper() + file[2:]
                           indiv_folder = match[0].upper()
                           subject_list.append(indiv_folder)
                        else: 
                            continue
                    else:
                        continue
                    
                print('Creating: {}'.format(file))

                # if Site, Library, Individual, and Images all checked
                if siteCheck.get() and libCheck.get() and indivCheck.get() and imagesCheck.get() and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library',indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.makedirs(os.path.join(to_folder,site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library'))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images'))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, r'Images', file))

                    else:
                        print('Error 1 -  Check where site, library, and individual folder are all checked')
                        continue
                 
                # if Library, Individual, and Image checked
                elif siteCheck.get()==False and libCheck.get() and indivCheck.get() and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, r'Library', indiv_folder, r'Images')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder +',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                          #  os.chdir(os.path.join(to_folder))
                        os.makedirs(os.path.join(to_folder, r'Library', indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, r'Library', indiv_folder)==False):
                          #  os.chdir(os.path.join(to_folder,  r'Library'))
                        os.makedirs(os.path.join(to_folder,  r'Library', indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder,  r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, r'Images', file))

                    else:
                        print('Error 2 -  Check where site=False, library=True, and individual=True')
                        continue         
                 
                # if Site, Individual, and Image all checked
                elif siteCheck.get() and libCheck.get()==False and indivCheck.get() and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder)==False):
                        os.makedirs(os.path.join(to_folder,  site_dic.get(file[0:2].upper()), indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, r'Images', file))

                    else:
                        print('Error 3 -  Check where site=True, library=False, and individual=True')
                        continue 

                 # if Site, Library, and Image checked
                elif siteCheck.get() and libCheck.get() and indivCheck.get()==False and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images',)):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library')==False):
                        os.makedirs(os.path.join(to_folder,  site_dic.get(file[0:2].upper()), r'Library', r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder,  site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))

                    else:
                        print('Error 4 -  Check where site=True, library=True, and individual=False')
                        continue 

                # if Site and Image checked
                elif siteCheck.get() and libCheck.get()==False and indivCheck.get()==False and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images'))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file),os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))

                    else:
                        print('Error 5 -  Check where site=True, library=False, and individual=False')
                        continue 

                 # if Individual and Image checked
                elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get() and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, indiv_folder, r'Images')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, indiv_folder))==False:
                        os.makedirs(os.path.join(to_folder, indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, indiv_folder, r'Images'))==False:
                        os.makedirs(os.path.join(to_folder, indiv_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, indiv_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, indiv_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, r'Images', file))

                    else:
                        print('Error 6 -  Check where site=False, library=False, and individual=True')
                        continue 

                 # if Library and Image checked
                elif siteCheck.get()==False and libCheck.get() and indivCheck.get()==False and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, r'Library', r'Images')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                        os.makedirs(os.path.join(to_folder, r'Library', r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, r'Library', r'Images'))==False:
                        os.makedirs(os.path.join(to_folder, r'Library', r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', r'Images', file))

                    else:
                        print('Error 7 -  Check where site=False, library=True, and individual=False')
                        continue

                # Image only
                elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get()==False and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, r'Images')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, r'Images'))==False:
                        os.makedirs(os.path.join(to_folder, r'Images'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Images', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Images', file))

                    else:
                        print('Error 8 -  Check all possiblities for site, Library, individual folder')
                        continue

                # if Site, Library, and Individual checked
                elif siteCheck.get() and libCheck.get() and indivCheck.get() and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder)):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library'))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder +',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root,file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder)==False):
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', indiv_folder, file))

                    else:
                        print('Error 9 -  Check where site, library, and individual folder are all checked')
                        continue
                 
                # if Library, and Individual checked    
                elif siteCheck.get()==False and libCheck.get() and indivCheck.get() and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, r'Library', indiv_folder)):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, file))

                    elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                        os.makedirs(os.path.join(to_folder, r'Library', indiv_folder))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, file))

                    elif os.path.exists(os.path.join(to_folder, r'Library', indiv_folder)==False):
                        os.makedirs(os.path.join(to_folder,  r'Library', indiv_folder))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder,  r'Library', indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', indiv_folder, file))

                    else:
                        print('Error 10 -  Check where site=False, library=True, and individual=True')
                        continue         
                 
                # if Site and Individual  checked
                elif siteCheck.get() and libCheck.get()==False and indivCheck.get() and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder)):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder)==False):
                        os.makedirs(os.path.join(to_folder,  site_dic.get(file[0:2].upper()), indiv_folder))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), indiv_folder, file))

                    else:
                        print('Error 11 -  Check where site=True, library=False, and individual=True')
                        continue 

                 # if Site  and Library  checked
                elif siteCheck.get() and libCheck.get() and indivCheck.get()==False and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library')==False):
                        os.makedirs(os.path.join(to_folder,  site_dic.get(file[0:2].upper()), r'Library'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder,  site_dic.get(file[0:2].upper()), r'Library', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))

                    else:
                        print('Error 12 -  Check where site=True, library=True, and individual=False')
                        continue 

                # if Site only checked
                elif siteCheck.get() and libCheck.get()==False and indivCheck.get()==False and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()))):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper())))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))

                    else:
                        print('Error 13 -  Check where site=True, library=False, and individual=False')
                        continue 

                 # if Individual only checked
                elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get() and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, indiv_folder)):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, file))

                    elif os.path.exists(os.path.join(to_folder, indiv_folder))==False:
                        os.makedirs(os.path.join(to_folder, indiv_folder))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, indiv_folder, file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, indiv_folder, file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, indiv_folder, file))

                    else:
                        print('Error 14 -  Check where site=False, library=False, and individual=True')
                        continue 

                # if Library only checked
                elif siteCheck.get()==False and libCheck.get() and indivCheck.get()==False and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, r'Library')):
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', file))

                    elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                        os.makedirs(os.path.join(to_folder, r'Library'))
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(os.path.join(root, file), os.path.join(to_folder, r'Library', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', file))
                        else:
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, r'Library', file))

                    else:
                        print('Error 15 -  Check where site=False, library=True, and individual=False')
                        continue

                # if nothing checked
                elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get()==False and imagesCheck.get()==False:
                    if mode_dd_combo.get() == 'Remove Originals':
                        shutil.move(os.path.join(root, file), os.path.join(to_folder, file))
                        moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, file))
                    else:
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file))
                        moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + os.path.join(root, file) + ',' + os.path.join(to_folder, file))

                else:
                    print('Error 16 - Check all possibilities for site, Library, individual folder')
                    continue

            except:
                unable_to_move.append(file)   

    # Find if there are StudyIDs on the .csv that were not found 
    if limitEntry.get() != '': 
        if StudyID_list_from_csv != []:
           if 'STUDYID' in StudyID_list_from_csv: 
                StudyID_list_from_csv.remove('STUDYID')  # remove the word "StudyID" if in the csv
           StudyID_list_from_csv_set = {studyID.upper() for studyID in StudyID_list_from_csv}
           subject_list_set = {studyID.upper() for studyID in subject_list} # Convert StudyIDs in moved_files to a set
           diff = StudyID_list_from_csv_set.difference(subject_list_set) # Find the StudyIDs in the csv that were not moved
           for id in diff:
                unable_to_move.append(id)        

    # Continuous log
    contin_log(moved_files, unable_to_move)

    # Create a log
    if logCheck.get() == True:
        messagebox.showinfo('Save Log File', 'Save Log File')
        create_log(moved_files, unable_to_move)


def background_color(event):
    mode = mode_dd_combo.get()
    if mode == 'Remove Originals':
        root.config(background='firebrick1')
        title.config(background='firebrick1')
        lines1.config(background='firebrick1')
        lines2.config(background='firebrick1')
        lines3.config(background='firebrick1')
        mode_dd_label.config(background='firebrick1')
        fromLabel.config(background='firebrick1')
        toLabel.config(background='firebrick1')
        limitTitle.config(background='firebrick1')
        limitLabel.config(background='firebrick1')
        frame1.config(background='firebrick1')
        frame2.config(background='firebrick1')
        frame3.config(background='firebrick1')
        frame4.config(background='firebrick1')
        frame5.config(background='firebrick1')
        frame6.config(background='firebrick1')
        frame7.config(background='firebrick1')
        frame8.config(background='firebrick1')
        frame9.config(background='firebrick1')
        frame10.config(background='firebrick1')
        frame11.config(background='firebrick1')
        frame12.config(background='firebrick1')
        frame13.config(background='firebrick1')
        frame14.config(background='firebrick1')
        frame15.config(background='firebrick1') 
        frame16.config(background='firebrick1')
        frame17.config(background='firebrick1')
        specifyBoxTitle.config(background='firebrick1')
        specifyBoxLabel.config(background='firebrick1')

    elif mode == 'Keep Originals' and get_platform() == 'MacOS':
        root.config(background='white')
        title.config(background='white')
        lines1.config(background='white')
        lines2.config(background='white')
        lines3.config(background='white')
        mode_dd_label.config(background='white')
        fromLabel.config(background='white')
        toLabel.config(background='white')
        limitTitle.config(background='white')
        limitLabel.config(background='white')
        frame1.config(background='white')
        frame2.config(background='white')
        frame3.config(background='white')
        frame4.config(background='white')
        frame5.config(background='white')
        frame6.config(background='white')
        frame7.config(background='white')
        frame8.config(background='white')
        frame9.config(background='white')
        frame10.config(background='white')
        frame11.config(background='white')
        frame12.config(background='white')
        frame13.config(background='white')
        frame14.config(background='white')
        frame15.config(background='white') 
        frame16.config(background='white')
        frame17.config(background='white')
        specifyBoxTitle.config(background='white')
        specifyBoxLabel.config(background='white')

    else:
        root.config(background='SystemButtonFace')
        title.config(background='SystemButtonFace')
        lines1.config(background='SystemButtonFace')
        lines2.config(background='SystemButtonFace')
        lines3.config(background='SystemButtonFace')
        mode_dd_label.config(background='SystemButtonFace')
        fromLabel.config(background='SystemButtonFace')
        toLabel.config(background='SystemButtonFace')
        limitTitle.config(background='SystemButtonFace')
        limitLabel.config(background='SystemButtonFace')
        frame1.config(background='SystemButtonFace')
        frame2.config(background='SystemButtonFace')
        frame3.config(background='SystemButtonFace')
        frame4.config(background='SystemButtonFace')
        frame5.config(background='SystemButtonFace')
        frame6.config(background='SystemButtonFace')
        frame7.config(background='SystemButtonFace')
        frame8.config(background='SystemButtonFace')
        frame9.config(background='SystemButtonFace')
        frame10.config(background='SystemButtonFace')
        frame11.config(background='SystemButtonFace')
        frame12.config(background='SystemButtonFace')
        frame13.config(background='SystemButtonFace')
        frame14.config(background='SystemButtonFace')
        frame15.config(background='SystemButtonFace') 
        frame16.config(background='SystemButtonFace')
        frame17.config(background='SystemButtonFace')
        specifyBoxTitle.config(background='SystemButtonFace')
        specifyBoxLabel.config(background='SystemButtonFace')


# Creates main window
root = Tk()
root.title('OFC2 Copy Files To Folders v. 4.0')
root.geometry('450x500+500+200')

# creates variables in window
mode = StringVar()
from_folder = StringVar()
to_folder = StringVar()
csv_path = StringVar()
specifyBox = StringVar()
libCheck = BooleanVar()
siteCheck = BooleanVar()
indivCheck = BooleanVar()
imagesCheck = BooleanVar()
logCheck = BooleanVar()

# WINDOWS
if get_platform() == 'Windows':

    # Title
    frame1 = Frame(root)
    title = ttk.Label(frame1, text='OFC2 Copy files from one location to another:')
    title.pack()
    frame1.pack()

    # Mode: Keep Originals vs. Remove Originals
    frame2 = Frame(root)
    mode_dd_label = ttk.Label(frame2, text='Mode: ')
    mode_dd_label.pack(side=LEFT)
    mode_dd_combo = ttk.Combobox(frame2, textvariable=mode, values=('Keep Originals', 'Remove Originals'), width=17)
    mode_dd_combo.bind("<<ComboboxSelected>>",  background_color)
    mode_dd_combo.set('Keep Originals')
    mode_dd_combo.pack()
    frame2.pack()

    frame3 = Frame(root)
    lines1 = Label(frame3, text='')
    lines1.pack()
    frame3.pack()

    # From Here text box
    frame4 = Frame(root)
    fromLabel = ttk.Label(frame4, text='From here:')
    fromLabel.pack(side=LEFT)
    fromEntry = ttk.Entry(frame4, textvariable=from_folder)
    fromEntry.pack(side=LEFT)
    getDataButton1 = ttk.Button(frame4, text='Browse...', command=get_fromData, width=10)
    getDataButton1.pack(side=LEFT)
    frame4.pack()

    # To here text box
    frame5 = Frame(root)
    toLabel = ttk.Label(frame5, text='To here:    ')
    toLabel.pack(side=LEFT)
    toEntry = ttk.Entry(frame5, textvariable=to_folder)
    toEntry.pack(side=LEFT)
    getDataButton2 = ttk.Button(frame5, text='Browse...', command=get_toData, width=10)
    getDataButton2.pack(side=LEFT)
    frame5.pack()

    # Make site folders checkbox
    frame6 = Frame(root)
    siteCheckBut = ttk.Checkbutton(frame6, text='Make Site subfolders           ', variable=siteCheck)
    siteCheckBut.pack()
    frame6.pack()

    # Make Library folders checkbox
    frame7 = Frame(root)
    libCheckBut = ttk.Checkbutton(frame7, text='Make Library subfolders      ', variable=libCheck)
    libCheckBut.pack()
    frame7.pack()

    # Make Individual folder
    frame8 = Frame(root)
    indivCheckBut = ttk.Checkbutton(frame8, text='Make Individual subfolders ', variable=indivCheck)
    indivCheckBut.pack()
    frame8.pack()

    # Make Images folder
    frame9 = Frame(root)
    imagesCheckBut = ttk.Checkbutton(frame9, text='Make Images subfolders     ', variable=imagesCheck)
    imagesCheckBut.pack()
    frame9.pack()

    frame10 = Frame(root)
    lines2 = Label(frame9, text='')
    lines2.pack()
    frame10.pack()

    # .CSV file
    frame11 = Frame(root)
    limitTitle = ttk.Label(frame11, text='Use a .csv file to limit StudyIDs: ')
    limitTitle.pack()
    limitLabel = ttk.Label(frame11, text='.CSV path:')
    limitLabel.pack(side=LEFT)
    limitEntry = ttk.Entry(frame11, textvariable=csv_path)
    limitEntry.pack(side=LEFT)
    getDataButton3 = ttk.Button(frame11, text='Browse...', command=get_csv, width=10)
    getDataButton3.pack(side=LEFT)
    frame11.pack()

    frame12 = Frame(root)
    lines3 = Label(frame12, text='')
    lines3.pack()
    frame12.pack()

    # Specify Filename convention box
    frame13 = Frame(root)
    specifyBoxTitle = ttk.Label(frame13, text='Specify any specific file naming conventions or file extensions: ')
    specifyBoxTitle.pack()
    specifyBoxLabel = ttk.Label(frame13, text='Example: _Clean, .txt, .obj etc...')
    specifyBoxLabel.pack()
    specifyBoxEntry = ttk.Entry(frame13, textvariable=specifyBox)
    specifyBoxEntry.pack()
    frame13.pack()

    # Make Log checkbox
    frame14 = Frame(root)
    logCheckBut = ttk.Checkbutton(frame14, text='Create a log file', variable=logCheck)
    logCheckBut.pack()
    frame14.pack()

    # Submit button
    frame15 = Frame(root)
    submitButton = ttk.Button(frame15, text='Submit', command=get_submit, width=10)
    submitButton.pack()
    frame15.pack()

    # Close button
    frame16 = Frame(root)
    closeButton = ttk.Button(frame16, text='Close', command=root.destroy, width=10)
    closeButton.pack()
    frame16.pack()

    #About button
    frame17 = Frame(root)
    closeButton = ttk.Button(frame17, text='About', command=get_about, width=10)
    closeButton.pack()
    frame17.pack()

    root.mainloop()

# All other OS (i.e. Mac/Linux)
else:

    # Title
    frame1 = Frame(root)
    title = Label(frame1, text='OFC2 Copy files from one location to another:')
    title.pack()
    frame1.pack()

    # Mode: Keep Originals vs. Remove Originals
    frame2 = Frame(root)
    mode_dd_label = Label(frame2, text='Mode: ')
    mode_dd_label.pack(side=LEFT)
    mode_dd_combo = ttk.Combobox(frame2, textvariable=mode, values=('Keep Originals', 'Remove Originals'), width=17)
    mode_dd_combo.bind("<<ComboboxSelected>>", background_color)
    mode_dd_combo.set('Keep Originals')
    mode_dd_combo.pack()
    frame2.pack()

    frame3 = Frame(root)
    lines1 = Label(frame3, text='')
    lines1.pack()
    frame3.pack()

    # From Here text box
    frame4 = Frame(root)
    fromLabel = Label(frame4, text='From here:')
    fromLabel.pack(side=LEFT)
    fromEntry = Entry(frame4, textvariable=from_folder)
    fromEntry.pack(side=LEFT)
    getDataButton1 = Button(frame4, text='Browse...', command=get_fromData, width=10)
    getDataButton1.pack(side=LEFT)
    frame4.pack()

    # To here text box
    frame5 = Frame(root)
    toLabel = Label(frame5, text='To here:    ')
    toLabel.pack(side=LEFT)
    toEntry = Entry(frame5, textvariable=to_folder)
    toEntry.pack(side=LEFT)
    getDataButton2 = Button(frame5, text='Browse...', command=get_toData, width=10)
    getDataButton2.pack(side=LEFT)
    frame5.pack()

    # Make site folders checkbox
    frame6 = Frame(root)
    siteCheckBut = Checkbutton(frame6, text='Make Site subfolders          ', variable=siteCheck)
    siteCheckBut.pack()
    frame6.pack()

    # Make Library folders checkbox
    frame7 = Frame(root)
    libCheckBut = Checkbutton(frame7, text='Make Library subfolders     ', variable=libCheck)
    libCheckBut.pack()
    frame7.pack()

    # Make Individual folder
    frame8 = Frame(root)
    indivCheckBut = Checkbutton(frame8, text='Make Individual subfolders ', variable=indivCheck)
    indivCheckBut.pack()
    frame8.pack()

    # Make Images folder
    frame9 = Frame(root)
    imagesCheckBut = Checkbutton(frame9, text='Make Images subfolders     ', variable=imagesCheck)
    imagesCheckBut.pack()
    frame9.pack()

    frame10 = Frame(root)
    lines2 = Label(frame10, text='')
    lines2.pack()
    frame10.pack()

    # .CSV file
    frame11 = Frame(root)
    limitTitle = Label(frame11, text='Use a .csv file to limit StudyIDs: ')
    limitTitle.pack()
    limitLabel = Label(frame11, text='.CSV path:')
    limitLabel.pack(side=LEFT)
    limitEntry = Entry(frame11, textvariable=csv_path)
    limitEntry.pack(side=LEFT)
    getDataButton3 = Button(frame11, text='Browse...', command=get_csv, width=10)
    getDataButton3.pack(side=LEFT)
    frame11.pack()

    frame12 = Frame(root)
    lines3 = Label(frame12, text='')
    lines3.pack()
    frame12.pack()

    # Specify Filename convention box
    frame13 = Frame(root)
    specifyBoxTitle = Label(frame13, text='Specify any specific file naming conventions or file extensions: ')
    specifyBoxTitle.pack()
    specifyBoxLabel = Label(frame13, text='Example: _Clean, .txt, .obj etc...')
    specifyBoxLabel.pack()
    specifyBoxEntry = Entry(frame13, textvariable=specifyBox)
    specifyBoxEntry.pack()
    frame13.pack()

    # Make Log checkbox
    frame14 = Frame(root)
    logCheckBut = Checkbutton(frame14, text='Create a log file', variable=logCheck)
    logCheckBut.pack()
    frame14.pack()

    # Submit button
    frame15 = Frame()
    submitButton = Button(frame15, text='Submit', command=get_submit, width=10)
    submitButton.pack()
    frame15.pack()

    # Close button
    frame16 = Frame()
    closeButton = Button(frame16, text='Close', command=root.destroy, width=10)
    closeButton.pack()
    frame16.pack()

    # About button
    frame17 = Frame()
    closeButton = Button(frame17, text='About', command=get_about, width=10)
    closeButton.pack()
    frame17.pack()

    root.mainloop()

