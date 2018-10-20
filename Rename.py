import os
import exifread
import shutil
import filecmp
srcFolderName = 'C:\\Users\\jizhu\\Pictures\\New\\src\\'
dstFolderName = 'C:\\Users\\jizhu\\Pictures\\New\\dst\\'
profNormal = 0
profCollision = 0
profNoEXIF = 0
profSameFile = 0
def getExif(filename):
    FIELD = 'EXIF DateTimeOriginal'
    fd = open(srcFolderName+filename, 'rb')
    tags = exifread.process_file(fd)
    fd.close()
    print('=== ', srcFolderName+filename)
    if FIELD in tags:
        new_name = str(tags[FIELD]).replace(':', '-') + os.path.splitext(filename)[1]
        tot = 1
        #sameFile = False
        while os.path.exists(dstFolderName+new_name):
            if filecmp.cmp(dstFolderName+new_name,srcFolderName+filename) == True :
                global profSameFile
                profSameFile += 1
                #sameFile = True
                print(srcFolderName+filename+' already exist!')
                print('new name is'+dstFolderName+new_name)
                return
            new_name = str(tags[FIELD]).replace(':', '-') + '_' + str(tot) + os.path.splitext(filename)[1]
            tot += 1
        #print(new_name)
        shutil.copy2(srcFolderName+filename, dstFolderName+new_name)
        if tot == 1:
            global profNormal
            profNormal += 1
        else:
            global profCollision
            profCollision += 1
    else:
        print('No {} found'.format(FIELD))
        shutil.copy2(srcFolderName+filename, dstFolderName+filename)
        global profNoEXIF
        profNoEXIF += 1

for filename in os.listdir(srcFolderName):
    fullPath = os.path.join(srcFolderName, filename)
    if os.path.isfile(fullPath):
        #print("it is file")
        getExif(filename)
    #else:
        #print("it is dir")
print("Normal Image #: ",profNormal)
print("Same File exists #: ", profSameFile)
print("Image with Collision #: ", profCollision)
print("Image with No EXIF #: ", profNoEXIF)

