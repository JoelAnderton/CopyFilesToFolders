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
#
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
                StudyID = rowDict[0].upper() # if the StudyID is typed in lowercase, this changes it to uppercase
                StudyID_list_from_csv.append(StudyID)

# Creates the "About" window
def get_about(event=None):
    messagebox.showinfo('About', '''    Created by: Joel Anderton 
    Created date: 12/17/2018

    OFC2 Copy Files to Folders
    version: 2.3
    
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

    ''')


def get_submit(event=None):
    
    site_dic = {'CO':r'Colombia', 'LC': r'Lancaster', 'NG':r'Nigeria', 'PH':r'Philippines', 'FC':r'Pittsburgh', 'PR': r'Puerto Rico'}
    unable_to_move =[]
    for root, dirs, files in os.walk(from_folder):
        os.chdir(to_folder)
        for file in files:
            try:
                if limitEntry.get() == '': # is the limiting .csv file bing used
                    # Determines if the file contains a StudyID: If so, it uppercases the first 2 letters. If not, it changes nothing 
                    pattern = r'[a-zA-Z][a-zA-z][0-9]{4,5}'
                    match = re.findall(pattern, file)
                    if match:
                        file = file[0:2].upper() + file[2:]
                    else:
                        pass
                else:
                    if file[0:7].upper() in StudyID_list_from_csv:
                        # Determines if the file contains a StudyID: If so, it uppercases the first 2 letters. If not, it changes nothing 
                        pattern = r'[a-zA-Z][a-zA-z][0-9]{4,5}'
                        match = re.findall(pattern, file)
                        if match:
                            file = file[0:2].upper() + file[2:]
                        else:
                            pass
                        
                    else: # if the limiting .csv file is not being used, then continue
                        continue


                print('Creating: {}'.format(file))

                # if Site, Library, and Individual all checked
                if siteCheck.get() and libCheck.get() and indivCheck.get() and imagesCheck.get() and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images')):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images', file))
                        

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                        os.chdir(os.path.join(to_folder))
                        os.makedirs(os.path.join(to_folder,site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images'))
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images', file))
                        

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library'))==False:
                        os.chdir(os.path.join(to_folder, site_dic.get(file[0:2].upper())))
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images'))
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images', file)) 
                        

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper()))==False:
                        os.chdir(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library'))
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images'))
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images'))==False:
                        os.chdir(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper()))
                        os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images'))
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), r'Images', file))
                        
                    else:
                        print('Error 1 -  Check where site, library, and individual folder are all checked')
                        continue
                 
                # if Library, and Individual checked    
                elif siteCheck.get()==False and libCheck.get() and indivCheck.get() and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, r'Library', file[0:7].upper(), r'Images')):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', file[0:7].upper(), r'Images', file))
                    
                    elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, r'Library', file[0:7].upper(), r'Images'))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', file[0:7].upper(), r'Images', file))
                         
                    elif os.path.exists(os.path.join(to_folder, r'Library', file[0:7].upper())==False):
                            os.chdir(os.path.join(to_folder,  r'Library'))
                            os.makedirs(os.path.join(to_folder,  r'Library', file[0:7].upper(), r'Images'))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder,  r'Library', file[0:7].upper(), r'Images', file))

                    else:
                        print('Error 2 -  Check where site=False, library=True, and indivudal=True')
                        continue         
                 
                # if Site and Individual all checked    
                elif siteCheck.get() and libCheck.get()==False and indivCheck.get() and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper(), r'Images')):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper(), r'Images', file))
                    
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper(), r'Images'))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper(), r'Images', file))
                         
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper())==False):
                            os.chdir(os.path.join(to_folder,  site_dic.get(file[0:2].upper())))
                            os.makedirs(os.path.join(to_folder,  site_dic.get(file[0:2].upper()), file[0:7].upper(), r'Images'))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper(), r'Images', file))

                    else:
                        print('Error 3 -  Check where site=True, library=False, and indivudal=True')
                        continue 

                 # if Site  and Library  checked
                elif siteCheck.get() and libCheck.get() and indivCheck.get()==False and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images',)):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                    
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images'))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', r'Images', file))
                         
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library')==False):
                            os.chdir(os.path.join(to_folder,  site_dic.get(file[0:2].upper())))
                            os.makedirs(os.path.join(to_folder,  site_dic.get(file[0:2].upper()), r'Library', r'Images'))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder,  site_dic.get(file[0:2].upper()), r'Library', r'Images', file))

                    else:
                        print('Error 4 -  Check where site=True, library=True, and indivudal=False')
                        continue 

                # if Site only checked
                elif siteCheck.get() and libCheck.get()==False and indivCheck.get()==False and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper(), r'Images'))):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))
                    
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images'))  
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Images', file))

                    else:
                        print('Error 5 -  Check where site=True, library=False, and indivudal=False')
                        continue 

                 # if Individual only checked
                elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get() and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, file[0:7].upper(), r'Images')):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:7].upper(), r'Images', file))
                    
                    elif os.path.exists(os.path.join(to_folder, file[0:7].upper()))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, file[0:7].upper(), r'Images'))  
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:7].upper(), r'Images', file))

                    else:
                        print('Error 6 -  Check where site=False, library=False, and indivudal=True')
                        continue 

                 # if Library only checked
                elif siteCheck.get()==False and libCheck.get() and indivCheck.get()==False and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, r'Library', r'Images')):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', r'Images', file))
                    
                    elif os.path.exists(os.path.join(to_folder, r'Library', r'Images'))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, r'Library', r'Images')) 
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', r'Images', file))

                    else:
                        print('Error 7 -  Check where site=False, library=True, and indivudal=False')
                        continue

                # if nothing checked
                elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get()==False and imagesCheck.get():
                    if os.path.exists(os.path.join(to_folder, r'Images')):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Images', file))

                    elif os.path.exists(os.path.join(to_folder, r'Images'))==False:
                        os.chdir(os.path.join(to_folder))
                        os.makedirs(os.path.join(to_folder, r'Images')) 
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Images', file))
     
                    else:
                        print('Error 8 -  Check all possiblities for site, Library, individual folder')
                        continue


                # if Site, Library, and Individual all checked
                elif siteCheck.get() and libCheck.get() and indivCheck.get() and imagesCheck.get()==False:
                
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper())):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), file))
                    

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper()))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), file))
                        

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library'))==False:
                            os.chdir(os.path.join(to_folder, site_dic.get(file[0:2].upper())))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper()))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), file)) 
                        

                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper())==False):
                            os.chdir(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library'))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper()))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file[0:7].upper(), file))
                        
                    else:
                        print('Error 9 -  Check where site, library, and individual folder are all checked')
                        continue
                 
                # if Library, and Individual checked    
                elif siteCheck.get()==False and libCheck.get() and indivCheck.get() and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, r'Library', file[0:7].upper())):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', file[0:7].upper(), file))
                    
                    elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, r'Library', file[0:7].upper()))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', file[0:7].upper(), file))
                         
                    elif os.path.exists(os.path.join(to_folder, r'Library', file[0:7].upper())==False):
                            os.chdir(os.path.join(to_folder,  r'Library'))
                            os.makedirs(os.path.join(to_folder,  r'Library', file[0:7].upper()))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder,  r'Library', file[0:7].upper(), file))

                    else:
                        print('Error 10 -  Check where site=False, library=True, and indivudal=True')
                        continue         
                 
                # if Site and Individual all checked    
                elif siteCheck.get() and libCheck.get()==False and indivCheck.get() and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper())):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper(), file))
                    
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper()))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper(), file))
                         
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper())==False):
                            os.chdir(os.path.join(to_folder,  site_dic.get(file[0:2].upper())))
                            os.makedirs(os.path.join(to_folder,  site_dic.get(file[0:2].upper()), file[0:7].upper()))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file[0:7].upper(), file))

                    else:
                        print('Error 11 -  Check where site=True, library=False, and indivudal=True')
                        continue 

                 # if Site  and Library  checked
                elif siteCheck.get() and libCheck.get() and indivCheck.get()==False and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library')):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                    
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library'))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library', file))
                         
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()), r'Library')==False):
                            os.chdir(os.path.join(to_folder,  site_dic.get(file[0:2].upper())))
                            os.makedirs(os.path.join(to_folder,  site_dic.get(file[0:2].upper()), r'Library'))
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder,  site_dic.get(file[0:2].upper()), r'Library', file))

                    else:
                        print('Error 12 -  Check where site=True, library=True, and indivudal=False')
                        continue 

                # if Site only checked
                elif siteCheck.get() and libCheck.get()==False and indivCheck.get()==False and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper()))):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))
                    
                    elif os.path.exists(os.path.join(to_folder, site_dic.get(file[0:2].upper())))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, site_dic.get(file[0:2].upper())))            
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, site_dic.get(file[0:2].upper()), file))

                    else:
                        print('Error 13 -  Check where site=True, library=False, and indivudal=False')
                        continue 

                 # if Individual only checked
                elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get() and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, file[0:7].upper())):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:7].upper(), file))
                    
                    elif os.path.exists(os.path.join(to_folder, file[0:7].upper()))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, file[0:7].upper()))            
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file[0:7].upper(), file))

                    else:
                        print('Error 14 -  Check where site=False, library=False, and indivudal=True')
                        continue 

                 # if Library only checked
                elif siteCheck.get()==False and libCheck.get() and indivCheck.get()==False and imagesCheck.get()==False:
                    if os.path.exists(os.path.join(to_folder, r'Library')):
                        shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', file))
                    
                    elif os.path.exists(os.path.join(to_folder, r'Library'))==False:
                            os.chdir(os.path.join(to_folder))
                            os.makedirs(os.path.join(to_folder, r'Library'))            
                            shutil.copy2(os.path.join(root, file), os.path.join(to_folder, r'Library', file))

                    else:
                        print('Error 15 -  Check where site=False, library=True, and indivudal=False')
                        continue

                # if nothing checked
                elif siteCheck.get()==False and libCheck.get()==False and indivCheck.get()==False and imagesCheck.get()==False:
                    shutil.copy2(os.path.join(root, file), os.path.join(to_folder, file))
     
                else:
                    print('Error 16 - Check all possiblities for site, Library, individual folder')
                    continue

            except:
                unable_to_move.append(file)
    
    print()
    if unable_to_move != []:
        print('*******************************************')
        print('Unable to determine where to move file(s):')
        for file in unable_to_move:
            print(file)
            messagebox.showwarning('Unable to move file', 'Unable to move file: \n' + file)

    messagebox.showinfo('Completed', 'Completed')
    #print('Done!!')

# Creates main window
root = Tk()
#root.state('zoomed')
root.title('OFC2 Copy Files To Folders')
root.geometry('400x300+200+250')

# creates variables in window
from_folder = StringVar()
to_folder = StringVar()
csv_path  = StringVar()
libCheck = BooleanVar()
siteCheck = BooleanVar()
indivCheck = BooleanVar()
imagesCheck = BooleanVar()

# Title
frame = Frame(root)
title = ttk.Label(frame, text='OFC2 Copy files from one location to another:')
title.pack()
frame.pack()

# From Here text box
frame = Frame(root)
fromLabel = ttk.Label(frame, text='From here:')
fromLabel.pack(side=LEFT)
fromEntry = ttk.Entry(frame, textvariable=from_folder)
fromEntry.pack(side=LEFT)
getDataButton1 = ttk.Button(frame, text='Browse...', command=get_fromData, width=10)
getDataButton1.pack(side=LEFT)
frame.pack()

# To here text box
frame = Frame(root)
toLabel = ttk.Label(frame, text='To here:    ')
toLabel.pack(side=LEFT)
toEntry = ttk.Entry(frame, textvariable=to_folder)
toEntry.pack(side=LEFT)
getDataButton2 = ttk.Button(frame, text='Browse...', command=get_toData, width=10)
getDataButton2.pack(side=LEFT)
frame.pack()

# Make site folders checkbox
frame = Frame(root)
siteCheckBut = ttk.Checkbutton(frame, text='Make Site subfolders          ', variable=siteCheck)
siteCheckBut.pack()
frame.pack()

# Make Library folders checkbox
frame = Frame(root)
libCheckBut = ttk.Checkbutton(frame, text='Make Library subfolders     ', variable=libCheck)
libCheckBut.pack()
frame.pack()

# Make Individual folder
frame = Frame(root)
indivCheckBut = ttk.Checkbutton(frame, text='Make Individual subfolders', variable=indivCheck)
indivCheckBut.pack()
frame.pack()

# Make Images folder
frame = Frame(root)
imagesCheckBut = ttk.Checkbutton(frame, text='Make Images subfolders      ', variable=imagesCheck)
imagesCheckBut.pack()
frame.pack()

# .CSV file
frame = Frame(root)
limitTitle = ttk.Label(frame, text='Use a .csv file to limit StudyIDs:')
limitTitle.pack()
limitLabel = ttk.Label(frame, text='.CSV path:')
limitLabel.pack(side=LEFT)
limitEntry = ttk.Entry(frame, textvariable=csv_path)
limitEntry.pack(side=LEFT)
getDataButton3 = ttk.Button(frame, text='Browse...', command=get_csv, width=10)
getDataButton3.pack(side=LEFT)
frame.pack()

# Submit button
frame = Frame()
submitButton = ttk.Button(frame, text='Submit', command=get_submit, width=10)
submitButton.pack()
frame.pack()

# Close button
frame = Frame()
closeButton = ttk.Button(frame, text='Close', command=root.destroy, width=10)
closeButton.pack()
frame.pack()

#About button
frame = Frame()
closeButton = ttk.Button(frame, text='About', command=get_about, width=10)
closeButton.pack()
frame.pack()

root.mainloop()



