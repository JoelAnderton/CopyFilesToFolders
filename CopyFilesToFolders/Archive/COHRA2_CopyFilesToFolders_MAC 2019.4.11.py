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
#       2/26/2019 - Added option to create visit level folders
#
#########################################################################################

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import os
import shutil
import csv
import re

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



# Creates the "About" window
def get_about(event=None):
    messagebox.showinfo('About', '''    Created by: Joel Anderton 
    Created date: 12/17/2018

    COHRA2 Copy Files to Folders
    version: 2.2
    
    Only works with files with COHRA2 style SubjectIDs
    The first 8 characters of the file must be the SubjectsID

    Updates:
    1/17/2019:
    - Created program. Modeled off the OFC2 version.
    - Added the option use a .csv file to limit StudyIDs to copy
    
    2/26/2019
    - Added the option to create visit level folders
    ''')


def get_submit(event=None):
    unable_to_move =[]
    for root, dirs, files in os.walk(from_folder):
        os.chdir(to_folder)
        for file in files:
            try:
                if limitEntry.get() == '': 
                    #StudyID_list_from_csv = []
                    #print('Nothing happening here')
                    file = file
                else:
                    if file[0:8] in StudyID_list_from_csv:
                        file = file
                        #print('Moving: ', file)
                    else:
                        #print(file[0:7])
                        #print(StudyID_list_from_csv)
                        #print('skipping')
                        continue
                
                print('Creating: {}'.format(file))

                # individual and visit folders
                if indivCheck.get() and visitCheck.get():
                    if os.path.exists(os.path.join(to_folder, file[0:8], get_visitFolder(file))):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:8], get_visitFolder(file), file))

                    elif os.path.exists(os.path.join(to_folder, file[0:8])) is False:
                         os.chdir(os.path.join(to_folder))
                         os.mkdir(os.path.join(to_folder, file[0:8]))
                         if os.path.exists(os.path.join(to_folder, file[0:8], get_visitFolder(file))) is False:
                             os.chdir(os.path.join(to_folder, file[0:8]))
                             os.mkdir(os.path.join(to_folder, file[0:8], get_visitFolder(file)))
                             os.chdir(os.path.join(to_folder, file[0:8], get_visitFolder(file)))
                             shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:8], get_visitFolder(file), file))

                    elif os.path.exists(os.path.join(to_folder, file[0:8])) is True:
                         if os.path.exists(os.path.join(to_folder, file[0:8], get_visitFolder(file))) is False:
                             os.chdir(os.path.join(to_folder, file[0:8]))
                             os.mkdir(os.path.join(to_folder, file[0:8], get_visitFolder(file)))
                             os.chdir(os.path.join(to_folder, file[0:8], get_visitFolder(file)))
                             shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:8], get_visitFolder(file), file))

                    else:
                        print('Check where indivudal=True and visit=True')
                        continue


                # indivudal folders only
                elif indivCheck.get() is True and visitCheck.get() is False:
                    if os.path.exists(os.path.join(to_folder, file[0:8])):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:8], file))

                    elif os.path.exists(os.path.join(to_folder, file[0:8])) is False:
                            os.chdir(os.path.join(to_folder))
                            os.mkdir(os.path.join(to_folder, file[0:8]))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:8], file))
                    else:
                        print('Check where indivudal=True')
                        continue

                # visit folders only
                elif indivCheck.get() is False and visitCheck.get() is True:
                    if os.path.exists(os.path.join(to_folder, get_visitFolder(file))):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, get_visitFolder(file), file))

                    elif os.path.exists(os.path.join(to_folder, get_visitFolder(file))) is False:
                        os.chdir(os.path.join(to_folder))
                        os.mkdir(os.path.join(to_folder, get_visitFolder(file)))
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, get_visitFolder(file), file))

                    else:
                        print('Check where visit=True')
                        continue

                else:
                    shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file))
                    #print(os.path.join(root, file), os.path.join(to_folder, file))
            except:
                unable_to_move.append(file)
    
    print()
    if unable_to_move != []:
        print('*******************************************')
        print('Unable to determine where to move file(s):')
        for file in unable_to_move:
            print(file)
            messagebox.showwarning('Unable to move file', 'Unable to move file: \n' + file)
    
    print('Done!')
    messagebox.showinfo('Completed', 'Completed')
    #print('Done!!')

# Creates main window
root = Tk()
#root.state('zoomed')
root.title('COHRA2 Copy Files To Folders')
root.geometry('400x300+200+250')

# creates variables in window
from_folder = StringVar()
to_folder = StringVar()
csv_path = StringVar()
indivCheck = BooleanVar()
visitCheck = BooleanVar()

# Title
frame = Frame(root)
title = Label(frame, text='COHRA2 Copy files from one location to another:')
title.pack()
frame.pack()

# From Here text box
frame = Frame(root)
fromLabel = Label(frame, text='From here:')
fromLabel.pack(side=LEFT)
fromEntry = Entry(frame, textvariable=from_folder)
fromEntry.pack(side=LEFT)
getDataButton1 = Button(frame, text='Browse...', command=get_fromData, width=10)
#getDataButton1.bind('<Button-1>', get_fromData)
getDataButton1.pack(side=LEFT)
frame.pack()

# To here text box
frame = Frame(root)
toLabel = Label(frame, text='To here:')
toLabel.pack(side=LEFT)
toEntry = Entry(frame, textvariable=to_folder)
toEntry.pack(side=LEFT)
getDataButton2 = Button(frame, text='Browse...', command=get_toData, width=10)
#getDataButton2.bind('<Button-1>', get_toData)
getDataButton2.pack(side=LEFT)
frame.pack()


# Make Individual folder
frame = Frame(root)
indivCheckBut = Checkbutton(frame, text='Make Individual folders', variable=indivCheck)
indivCheckBut.pack()
frame.pack()

# Make Visit folders
frame = Frame(root)
visitCheckBut = Checkbutton(frame, text='Make Visit folders', variable=visitCheck)
visitCheckBut.pack()
frame.pack()

# .CSV file
frame = Frame(root)
limitTitle = Label(frame, text='Use a .csv file to limit StudyIDs:')
limitTitle.pack()
limitLabel = Label(frame, text='.CSV path:')
limitLabel.pack(side=LEFT)
limitEntry = Entry(frame, textvariable=csv_path)
limitEntry.pack(side=LEFT)
getDataButton3 = Button(frame, text='Browse...', command=get_csv, width=10)
getDataButton3.pack(side=LEFT)
frame.pack()

# Submit button
frame = Frame()
submitButton = Button(frame, text='Submit', command=get_submit, width=10)
#submitButton.bind('<Button-1>', get_submit)
submitButton.pack()
frame.pack()

# Close button
frame = Frame()
closeButton = Button(frame, text='Close', command=root.destroy, width=10)
closeButton.pack()
frame.pack()

#About button
frame = Frame()
closeButton = Button(frame, text='About', command=get_about, width=10)
closeButton.pack()
frame.pack()

root.mainloop()




