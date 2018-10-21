import os
import exifread
import time
import filecmp

def exifRename(srcFilePath):
    basePath, fileName = os.path.split(srcFilePath);
    if not os.path.exists(srcFilePath):
        print("ERROR: No file exist. Please check your input!")
        return '';
    if(fileName==''): # no legal filename is extracted
        return ''; 
    
    FIELD = 'EXIF DateTimeOriginal'
    tags=[];
    try:
        with open(srcFilePath, 'rb') as fd:
            tags = exifread.process_file(fd)
    except:
        print("WARN: Fail to open file " + srcFilePath);
    

    if FIELD in tags: # file does have exif use it
        exifName = str(tags[FIELD]).replace(':', '-') + os.path.splitext(fileName)[1]
    else: #if no exif use local time
        exifName = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())+ os.path.splitext(fileName)[1]
    

    tot = 1
    while os.path.exists(basePath+exifName):
        if filecmp.cmp(basePath+exifName,srcFilePath) == True :  # same files no need to convert and backup
            return ''
        #not the same file but exifName already exist(shot at the same time)
        exifName = str(tags[FIELD]).replace(':', '-') + '_' + str(tot) + os.path.splitext(fileName)[1]
        tot += 1
    
    return exifName
