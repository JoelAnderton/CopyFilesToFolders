#########################################################################################
# Created by: Joel Anderton
# Created date: 12/17/2018
#
# Purpose: To copy all Subject files (or a select list based off a .csv file) from
#         one location to another and allow for creating subfolders for subject folders
# 
#       - Added the option use a .csv file to limit StudyIDs to copy 
#       - Made it handle unidentified files that don't match the COHRA2 style
#       - WINDOWS version uses the ttk theme to create nicer Windows buttons
#
# Updates -
#   2/26/2019 
#       - Added option to create visit level folders
#   4/9/2019  
#       - Added option to create an "Images" subfolder
#   7/26/2019
#       - Make code cross platform
#       - Add "Specify File Name" section
#       - Create log files
#       - Change between modes            
#   8/15/2019
#       - Improved handling file paths using pathlib (to prevent MacOS and Windows issues)
#       - Empty folders are deleted if "Remove Originals" is selected
#########################################################################################
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from pathlib import Path
from pathlib import PurePath
import os
import shutil
import csv
import re
import datetime
import sys


# Determines OS
def get_platform():
    '''Determine what OS is being used'''
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
    #print('From :', from_folder)
    fromEntry.insert(END, from_folder)


# Gets data from the "To here" text box
def get_toData(event=None):
    global to_folder
    to_folder = askdirectory()
    #print('To :', to_folder)
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
                StudyID = rowDict[0]
                StudyID_list_from_csv.append(StudyID)


def get_visitFolder(filename):
    pattern = r'[Vv][0-9]+'
    match = re.findall(pattern, filename)
    if match:
        stop = re.search(pattern, filename)
        folder = filename[0:stop.span()[1]]
        return folder
    else:
        folder = filename[0:8]
        return folder

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
    messagebox.showinfo('About',
    '''    Created by: Joel Anderton 
    Created date: 12/17/2018

    COHRA2 Copy Files to Folders
    version: 4.2
    
    Only works with files with COHRA2 
    style SubjectIDs.The first 8 
    characters of the file must be the 
    SubjectsID.

    Updates:
    1/17/2019 v. 2.1
    - Created program. Modeled off the 
       OFC2 version.
    - Added the option use a .csv file 
       to limit StudyIDs to copy
    
    2/26/2019 v. 2.2
    - Added the option to create visit 
       level folders
    
    4/9/2019 - v. 2.3
    - Added option to create an "Images" 
       subfolder

    7/26/2019 - v. 4.1
    - Added "Mode" option to change between 
      "Keep Originals" and "Remove Originals"
    - Added logging feature
    - Minor bug fixes
    - Updated version to be in sync with OFC2

    8/15/2019 - v. 4.2
    - Improved handling file paths 
    - Empty folders are deleted if "Remove Originals" is selected
    ''')


def get_submit(event=None):

    moved_files = []
    unable_to_move =[]
    subject_list = []

    for root, dirs, files in os.walk(fromEntry.get()):  
        for file in files:
            try:
                # limit and specifyBox are both null
                if limitEntry.get() == '' and specifyBox.get() == '': # is the limiting .csv file being used
                    # Determines if the file contains a StudyID: If so, it uppercases the first 2 letters. If not, it changes nothing 
                    pattern = r'[0-9]{8}'
                    match = re.findall(pattern, file)
                    if match:
                        indiv_folder = match[0]
                        subject_list.append(indiv_folder)
                    else:
                        continue
                 
                # limit is not null and and specifyBox is null
                elif limitEntry.get() != '' and specifyBox.get() == '':
                    if (file[0:8] in StudyID_list_from_csv):
                        # Determines if the file contains a StudyID: If so, it uppercases the first 2 letters. If not, it changes nothing 
                        pattern = r'[0-9]{8}'
                        match = re.findall(pattern, file)
                        if match:
                            indiv_folder = match[0]
                            subject_list.append(indiv_folder)
                        else:
                            continue 
                    else:
                        continue

                # limit is null and specifyBox is not null
                elif limitEntry.get() == '' and specifyBox.get() != '':
                    if specifyBox.get().upper() in file.upper():
                        pattern = r'[0-9]{8}'
                        match = re.findall(pattern, file)
                        if match :
                            indiv_folder = match[0]
                            subject_list.append(indiv_folder)
                        else: 
                            continue
                    else:
                        continue

                # both limit and specifyBox are not null
                elif limitEntry.get() != '' and specifyBox.get() != '':
                    if (file[0:8] in StudyID_list_from_csv and specifyBox.get().upper() in file.upper()):
                        pattern = r'[0-9]{8}'
                        match = re.findall(pattern, file)
                        if match:
                           indiv_folder = match[0]
                           subject_list.append(indiv_folder)
                        else: 
                            continue
                    else:
                        continue
                print('Creating: {}'.format(file))

                # individual and visit and Images
                if indivCheck.get() and visitCheck.get() and imagesCheck.get():
                    if Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images')).exists():
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file)))

                    elif Path(PurePath(toEntry.get(), file[0:8])).exists() is False:
                        Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file),  r'Images')).mkdir(parents=True, exist_ok=True)
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file)))

                    elif Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file))).exists() is False:
                        Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images')).mkdir(parents=True, exist_ok=True)
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' +str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file)))

                    elif Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images')).exists() is False:
                        Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images')).mkdir(parents=True, exist_ok=True)
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), r'Images', file)))

                    else:
                        print('Check where individual=True and visit=True and Images=True')
                        continue

                # individual folders and Images
                elif indivCheck.get() is True and visitCheck.get() is False and imagesCheck.get() is True:
                    if Path(PurePath(toEntry.get(), file[0:8], r'Images')).exists():
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], r'Images', file)))

                    elif Path(PurePath(toEntry.get(), file[0:8])).exists() is False:
                        Path(PurePath(toEntry.get(), file[0:8], r'Images')).mkdir(parents=True, exist_ok=True)
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], r'Images', file)))

                    else:
                        print('Check where individual=True and Images=True')
                        continue

                # visit folders and Images
                elif indivCheck.get() is False and visitCheck.get() is True and imagesCheck.get() is True:
                    if Path(PurePath(toEntry.get(), get_visitFolder(file), r'Images')).exists():
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), get_visitFolder(file), r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), get_visitFolder(file), r'Images', file)))

                    elif Path(PurePath(toEntry.get(), get_visitFolder(file), r'Images')).exists() is False:
                        Path(PurePath(toEntry.get(), get_visitFolder(file), r'Images')).mkdir(parents=True, exist_ok=True)
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), get_visitFolder(file), r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), get_visitFolder(file), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), get_visitFolder(file), r'Images', file)))

                    else:
                        print('Check where visit=True and Images=True')
                        continue

                # Images folders only
                elif indivCheck.get() is False and visitCheck.get() is False and imagesCheck.get() is True:
                    if Path(PurePath(toEntry.get(), r'Images')).exists():
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), r'Images', file)))

                    elif Path(PurePath(toEntry.get(), r'Images')).exists() is False:
                        Path(PurePath(toEntry.get(), r'Images')).mkdir(parents=True, exist_ok=True)
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), r'Images', file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), r'Images', file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), r'Images', file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), r'Images', file)))

                    else:
                        print('Check where Images=True')
                        continue

                # individual and visit folders
                elif indivCheck.get() and visitCheck.get() and imagesCheck.get() is False:
                    if Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file))).exists():
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file)))

                    elif Path(PurePath(toEntry.get(), file[0:8])).exists() is False:
                        Path(PurePath(toEntry.get(), file[0:8])).mkdir(parents=True, exist_ok=True)
                        if  Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file))).exists() is False:
                            os.makedirs(os.path.join(toEntry.get(), file[0:8], get_visitFolder(file)))
                            if mode_dd_combo.get() == 'Remove Originals':
                                shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file))
                                moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file)))
                                if len(os.listdir(root)) == 0: 
                                    os.rmdir(root)
                            else:
                                shutil.copy2(os.path.join(root, file), os.path.join(toEntry.get(), file[0:8], get_visitFolder(file), file))
                                moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file)))

                    elif Path(PurePath(toEntry.get(), file[0:8])).exists() is True:
                        if  Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file))).exists() is False:
                            Path(PurePath(toEntry.get(), file[0:8], get_visitFolder(file))).mkdir(parents=True, exist_ok=True)
                            if mode_dd_combo.get() == 'Remove Originals':
                                shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file))
                                moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file)))
                                if len(os.listdir(root)) == 0: 
                                    os.rmdir(root)
                            else:
                                shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file))
                                moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], get_visitFolder(file), file)))
                    
                    else:
                        print('Check where individual=True and visit=True and Images=false')
                        continue

                # individual folders only
                elif indivCheck.get() is True and visitCheck.get() is False and imagesCheck.get() is False:
                    if Path(PurePath(toEntry.get(), file[0:8])).exists():
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' + str(PurePath(toEntry.get(), file[0:8], file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' + str(PurePath(toEntry.get(), file[0:8], file)))

                    elif Path(PurePath(toEntry.get(), file[0:8])).exists() is False:
                        Path(PurePath(toEntry.get(), file[0:8])).mkdir(parents=True, exist_ok=True)
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), file[0:8], file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file[0:8], file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], file)))

                    else:
                        print('Check where individual=True')
                        continue

                # visit folders only
                elif indivCheck.get() is False and visitCheck.get() is True and imagesCheck.get() is False:
                    if Path(PurePath(toEntry.get(), get_visitFolder(file))).exists():
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), get_visitFolder(file), file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), get_visitFolder(file), file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], file)))

                    elif Path(PurePath(toEntry.get(), get_visitFolder(file))).exists() is False:
                        Path(PurePath(toEntry.get(), get_visitFolder(file))).mkdir(parents=True, exist_ok=True)
                        if mode_dd_combo.get() == 'Remove Originals':
                            shutil.move(PurePath(root, file), PurePath(toEntry.get(), get_visitFolder(file), file))
                            moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], file)))
                            if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                        else:
                            shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), get_visitFolder(file), file))
                            moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' +  str(PurePath(toEntry.get(), file[0:8], file)))

                    else:
                        print('Check where visit=True')
                        continue

                else:
                    if mode_dd_combo.get() == 'Remove Originals':
                        shutil.move(PurePath(root, file), PurePath(toEntry.get(), file))
                        moved_files.append('Success Move!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' + str(PurePath(toEntry.get(), file)))
                        if len(os.listdir(root)) == 0: 
                                os.rmdir(root)
                    else:
                        shutil.copy2(PurePath(root, file), PurePath(toEntry.get(), file))
                        moved_files.append('Success Copy!, ' + str(datetime.datetime.now()) + ',' + indiv_folder + ',' + str(PurePath(root, file)) + ',' + str(PurePath(toEntry.get(), file)))
            except:
                unable_to_move.append(file)
    
    
    # Find if there are StudyIDs on the .csv that were not found 
    if limitEntry.get() != '': 
        if StudyID_list_from_csv != []:
           if 'StudyID' in StudyID_list_from_csv: 
                StudyID_list_from_csv.remove('StudyID')  # remove the word "StudyID" if in the csv
           if 'SubjectID' in StudyID_list_from_csv: 
                StudyID_list_from_csv.remove('SubjectID')  # remove the word "SubjectID" if in the csv 
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
        specifyBoxTitle.config(background='SystemButtonFace')
        specifyBoxLabel.config(background='SystemButtonFace')


# Creates main window
root = Tk()
root.title('COHRA2 Copy Files To Folders v. 4.2')


# creates variables in window
mode = StringVar()
from_folder = StringVar()
to_folder = StringVar()
indivCheck = BooleanVar()
visitCheck = BooleanVar()
imagesCheck = BooleanVar()
csv_path = StringVar()
specifyBox = StringVar()
logCheck = BooleanVar()
logCheck.set(True)


# WINDOWS
if get_platform() == 'Windows':
    root.geometry('450x450+500+200')
    # Title
    frame1 = Frame(root)
    title = ttk.Label(frame1, text='COHRA2 Copy files from one location to another:')
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
    lines1 = ttk.Label(frame3, text='')
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

    # Make Individual folder
    frame6 = Frame(root)
    indivCheckBut = ttk.Checkbutton(frame6, text='Make Individual folders  ', variable=indivCheck)
    indivCheckBut.pack()
    frame6.pack()

    # Make Visit folders
    frame7 = Frame(root)
    visitCheckBut = ttk.Checkbutton(frame7, text='Make Visit folders            ', variable=visitCheck)
    visitCheckBut.pack()
    frame7.pack()

    # Make Images folder
    frame8 = Frame(root)
    imagesCheckBut = ttk.Checkbutton(frame8, text='Make Images subfolders', variable=imagesCheck)
    imagesCheckBut.pack()
    frame8.pack()

    frame9 = Frame(root)
    lines2 = ttk.Label(frame9, text='')
    lines2.pack()
    frame9.pack()

    # .CSV file
    frame10 = Frame(root)
    limitTitle = ttk.Label(frame10, text='Use a .csv file to limit StudyIDs:')
    limitTitle.pack()
    limitLabel = ttk.Label(frame10, text='.CSV path:')
    limitLabel.pack(side=LEFT)
    limitEntry = ttk.Entry(frame10, textvariable=csv_path)
    limitEntry.pack(side=LEFT)
    getDataButton3 = ttk.Button(frame10, text='Browse...', command=get_csv, width=10)
    getDataButton3.pack(side=LEFT)
    frame10.pack()

    frame11 = Frame(root)
    lines3 = ttk.Label(frame11, text='')
    lines3.pack()
    frame11.pack()

    # Specify Filename convention box
    frame12 = Frame(root)
    specifyBoxTitle = ttk.Label(frame12, text='Specify any specific file naming conventions or file extensions: ')
    specifyBoxTitle.pack()
    specifyBoxLabel = ttk.Label(frame12, text='Example: _Clean, .txt, .obj etc...')
    specifyBoxLabel.pack()
    specifyBoxEntry = ttk.Entry(frame12, textvariable=specifyBox)
    specifyBoxEntry.pack()
    frame12.pack()

    # Make Log checkbox
    frame13 = Frame(root)
    logCheckBut = ttk.Checkbutton(frame13, text='Create a log file', variable=logCheck)
    logCheckBut.pack()
    frame13.pack()

    # Submit button
    frame14 = Frame()
    submitButton = ttk.Button(frame14, text='Submit', command=get_submit, width=10)
    submitButton.pack()
    frame14.pack()

    # Close button
    frame15 = Frame()
    closeButton = ttk.Button(frame15, text='Close', command=root.destroy, width=10)
    closeButton.pack()
    frame15.pack()

    #About button
    frame16 = Frame()
    closeButton = ttk.Button(frame16, text='About', command=get_about, width=10)
    closeButton.pack()
    frame16.pack()

    root.mainloop()

else:
    root.geometry('450x500+500+200')
    # Title
    frame1 = Frame(root)
    title = Label(frame1, text='COHRA2 Copy files from one location to another:')
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

    # Make Individual folder
    frame6 = Frame(root)
    indivCheckBut = Checkbutton(frame6, text='Make Individual folders  ', variable=indivCheck)
    indivCheckBut.pack()
    frame6.pack()

    # Make Visit folders
    frame7 = Frame(root)
    visitCheckBut = Checkbutton(frame7, text='Make Visit folders           ', variable=visitCheck)
    visitCheckBut.pack()
    frame7.pack()

    # Make Images folder
    frame8 = Frame(root)
    imagesCheckBut = Checkbutton(frame8, text='Make Images subfolders', variable=imagesCheck)
    imagesCheckBut.pack()
    frame8.pack()

    frame9 = Frame(root)
    lines2 = Label(frame9, text='')
    lines2.pack()
    frame9.pack()

    # .CSV file
    frame10 = Frame(root)
    limitTitle = Label(frame10, text='Use a .csv file to limit StudyIDs:')
    limitTitle.pack()
    limitLabel = Label(frame10, text='.CSV path:')
    limitLabel.pack(side=LEFT)
    limitEntry = Entry(frame10, textvariable=csv_path)
    limitEntry.pack(side=LEFT)
    getDataButton3 = Button(frame10, text='Browse...', command=get_csv, width=10)
    getDataButton3.pack(side=LEFT)
    frame10.pack()

    frame11 = Frame(root)
    lines3 = Label(frame11, text='')
    lines3.pack()
    frame11.pack()

    # Specify Filename convention box
    frame12 = Frame(root)
    specifyBoxTitle = Label(frame12, text='Specify any specific file naming conventions or file extensions: ')
    specifyBoxTitle.pack()
    specifyBoxLabel = Label(frame12, text='Example: _Clean, .txt, .obj etc...')
    specifyBoxLabel.pack()
    specifyBoxEntry = Entry(frame12, textvariable=specifyBox)
    specifyBoxEntry.pack()
    frame12.pack()

    # Make Log checkbox
    frame13 = Frame(root)
    logCheckBut = Checkbutton(frame13, text='Create a log file', variable=logCheck)
    logCheckBut.pack()
    frame13.pack()

    # Submit button
    frame14 = Frame()
    submitButton = Button(frame14, text='Submit', command=get_submit, width=10)
    submitButton.pack()
    frame14.pack()

    # Close button
    frame15 = Frame()
    closeButton = Button(frame15, text='Close', command=root.destroy, width=10)
    closeButton.pack()
    frame15.pack()

    #About button
    frame16 = Frame()
    closeButton = Button(frame16, text='About', command=get_about, width=10)
    closeButton.pack()
    frame16.pack()

    root.mainloop()
