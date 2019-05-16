from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import os
import shutil
import csv


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

def get_submit(event=None):
    
    site_dic = {'CO':r'Colombia', 'LC': r'Lancaster', 'NG':r'Nigeria', 'PH':r'Philippines', 'FC':r'Pittsburgh', 'PR': r'Puerto Rico'}
    
    for root, dirs, files in os.walk(from_folder):
        for file in files:
            if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7])):
                    #shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7], file))
                    print(os.path.join(root, file),' --->', os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7], file))












# Creates main window
root = Tk()
root.title('OFC2 Copy Files To Folders')
root.geometry('400x300+200+250')

# creates variables in window
from_folder = StringVar()
to_folder = StringVar()



# From Here text box
frame = Frame(root)
fromLabel = Label(frame, text='From here:')
fromLabel.pack(side=LEFT)
fromEntry = Entry(frame, textvariable=from_folder)
fromEntry.pack(side=LEFT)
getDataButton1 = Button(frame, text='Browse', command=get_fromData)
#getDataButton1.bind('<Button-1>', get_fromData)
getDataButton1.pack(side=LEFT)
frame.pack()

# To here text box
frame = Frame(root)
toLabel = Label(frame, text='To here:')
toLabel.pack(side=LEFT)
toEntry = Entry(frame, textvariable=to_folder)
toEntry.pack(side=LEFT)
getDataButton2 = Button(frame, text='Browse', command=get_toData)
#getDataButton2.bind('<Button-1>', get_toData)
getDataButton2.pack(side=LEFT)
frame.pack()


# Submit button
frame = Frame()
submitButton = Button(frame, text='Submit', command=get_submit)
#submitButton.bind('<Button-1>', get_submit)
submitButton.pack()
frame.pack()


root.mainloop()
