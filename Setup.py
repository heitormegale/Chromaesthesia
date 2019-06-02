import os
directory="C:\\Users\\heito\\Desktop\\UCSB\\Spring 2019\\15C\\Music" #<-- your directory
os.chdir(directory)
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

createFolder(os.path.join(directory,'IndividualSounds'))
createFolder(os.path.join(directory,'ImageFolder'))
createFolder(os.path.join(directory,'Separate_Sounds'))