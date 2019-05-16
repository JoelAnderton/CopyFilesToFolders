from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import os
import shutil


def get_fromData(event=None):
    global from_folder
    from_folder = askdirectory()
    #print('From :', from_folder)
    fromEntry.insert(END, from_folder)

def get_toData(event=None):
    global to_folder
    to_folder = askdirectory()
    #print('To :', to_folder)
    toEntry.insert(END, to_folder)


def get_about(event=None):
    messagebox.showinfo('About', '''    Created by: Joel Anderton 
    Created date: 12/17/2018
    version: 2.0''')


def get_submit(event=None):
    site_dic = {'CO':r'Colombia', 'LC': r'Lancaster', 'NG':r'Nigeria', 'PH':r'Philippines', 'FC':r'Pittsburgh', 'PR': r'Puerto Rico'}
    for root, dirs, files in os.walk(from_folder):
        os.chdir(to_folder)

        for file in files:
            print('Creating: {}'.format(file))
            if siteCheck.get() and libCheck.get() and indivCheck.get():
                
                if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7])):
                    shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7], file))
                    

                elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2])))==False:
                        os.chdir(os.path.join(to_folder))
                        os.mkdir(os.path.join(to_folder,site_dic.get(file[0:2])))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library'))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7]))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7], file))
                        

                elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library'))==False:
                        os.chdir(os.path.join(to_folder, site_dic.get(file[0:2])))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library'))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7]))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7], file)) 
                        

                elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7])==False):
                        os.chdir(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library'))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7]))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file[0:7], file))
                        
                else:
                    print('Check where site, library, and indivudal folder are all checked')
                    continue
                   
            elif siteCheck.get()==False and libCheck.get() and indivCheck.get():
                if os.path.exists(os.path.join(to_folder, r'Library', file[0:7])):
                    shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, r'Library', file[0:7], file))
                    
                elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                        os.chdir(os.path.join(to_folder))
                        os.mkdir(os.path.join(to_folder, r'Library'))
                        os.mkdir(os.path.join(to_folder, r'Library', file[0:7]))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, r'Library', file[0:7], file))
                         
                elif os.path.exists(os.path.join(to_folder, r'Library', file[0:7])==False):
                        os.chdir(os.path.join(to_folder,  r'Library'))
                        os.mkdir(os.path.join(to_folder,  r'Library', file[0:7]))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder,  r'Library', file[0:7], file))

                else:
                    print('Check where site=False, library=True, and indivudal=True')
                    continue         
                                       
            elif siteCheck.get() and libCheck.get()==False and indivCheck.get():
                if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]), file[0:7])):
                    shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), file[0:7], file))
                    
                elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2])))==False:
                        os.chdir(os.path.join(to_folder))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2])))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2]), file[0:7]))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), file[0:7], file))
                         
                elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]), file[0:7])==False):
                        os.chdir(os.path.join(to_folder,  site_dic.get(file[0:2])))
                        os.mkdir(os.path.join(to_folder,  site_dic.get(file[0:2]), file[0:7]))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), file[0:7], file))

                else:
                    print('Check where site=True, library=False, and indivudal=True')
                    continue 

            elif siteCheck.get() and libCheck.get() and indivCheck.get()==False:
                if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library')):
                    shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file))
                    
                elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2])))==False:
                        os.chdir(os.path.join(to_folder))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2])))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library'))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), r'Library', file))
                         
                elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]), r'Library')==False):
                        os.chdir(os.path.join(to_folder,  site_dic.get(file[0:2])))
                        os.mkdir(os.path.join(to_folder,  site_dic.get(file[0:2]), r'Library'))
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder,  site_dic.get(file[0:2]), r'Library', file))

                else:
                    print('Check where site=True, library=True, and indivudal=False')
                    continue 

            elif siteCheck.get() and libCheck.get()==False and indivCheck.get()==False:
                if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2]))):
                    shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), file))
                    
                elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2])))==False:
                        os.chdir(os.path.join(to_folder))
                        os.mkdir(os.path.join(to_folder, site_dic.get(file[0:2])))            
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, site_dic.get(file[0:2]), file))

                else:
                    print('Check where site=True, library=False, and indivudal=False')
                    continue 

            elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get():
                if os.path.exists(os.path.join(to_folder, file[0:7])):
                    shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, file[0:7], file))
                    
                elif os.path.exists(os.path.join(to_folder, file[0:7]))==False:
                        os.chdir(os.path.join(to_folder))
                        os.mkdir(os.path.join(to_folder, file[0:7]))            
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, file[0:7], file))

                else:
                    print('Check where site=False, library=False, and indivudal=True')
                    continue 

            elif siteCheck.get()==False and libCheck.get() and indivCheck.get()==False:
                if os.path.exists(os.path.join(to_folder, r'Library')):
                    shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, r'Library', file))
                    
                elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                        os.chdir(os.path.join(to_folder))
                        os.mkdir(os.path.join(to_folder, r'Library'))            
                        shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, r'Library', file))

                else:
                    print('Check where site=False, library=True, and indivudal=False')
                    continue

            elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get()==False:
                shutil.copy2(os.path.join(from_folder, file), os.path.join(to_folder, file))
     
            else:
                print('Check all possiblities for site, Library, individual folder')
                continue
    messagebox.showinfo('Completed', 'Completed')
    #print('Done!!')

root = Tk()
root.title('Copy Files To Folders')
root.geometry('400x200+200+250')

from_folder = StringVar()
to_folder = StringVar()
libCheck = BooleanVar()
siteCheck = BooleanVar()
indivCheck = BooleanVar()


frame = Frame(root)
fromEntry = Entry(frame, textvariable=from_folder)
fromEntry.pack(side=LEFT)
getDataButton1 = Button(frame, text='Browse', command=get_fromData)
#getDataButton1.bind('<Button-1>', get_fromData)
getDataButton1.pack(side=LEFT)
frame.pack()

frame = Frame(root)
toEntry = Entry(frame, textvariable=to_folder)
toEntry.pack(side=LEFT)
getDataButton2 = Button(frame, text='Browse', command=get_toData)
#getDataButton2.bind('<Button-1>', get_toData)
getDataButton2.pack(side=LEFT)
frame.pack()

frame = Frame(root)
siteCheckBut = Checkbutton(frame, text='Make Site folders', variable=siteCheck)
siteCheckBut.pack()
frame.pack()

frame = Frame(root)
libCheckBut = Checkbutton(frame, text='Make a Library folder', variable=libCheck)
libCheckBut.pack()
frame.pack()

frame = Frame(root)
indivCheckBut = Checkbutton(frame, text='Make Individual folders', variable=indivCheck)
indivCheckBut.pack()
frame.pack()


frame = Frame()
submitButton = Button(frame, text='Submit', command=get_submit)
#submitButton.bind('<Button-1>', get_submit)
submitButton.pack()
frame.pack()

frame = Frame()
closeButton = Button(frame, text='Close', command=root.destroy)
closeButton.pack()
frame.pack()

frame = Frame()
closeButton = Button(frame, text='About', command=get_about)
closeButton.pack()
frame.pack()

root.mainloop()



