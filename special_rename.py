import os
srcFolderName = 'C:\\works\\tmp\\test'
base = 5
for filename in os.listdir(srcFolderName):
    fullPath = os.path.join(srcFolderName, filename)
    new_filename = filename[base:base+4]+'-'+filename[base+4:base+6]+'-'+filename[base+6:base+8]+' '+filename[base+8:base+10]+'-'+filename[base+10:base+12]+'-'+filename[base+12:]
    new_fullPath = os.path.join(srcFolderName,new_filename)
    os.rename(fullPath,new_fullPath)
 

