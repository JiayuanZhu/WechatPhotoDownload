import itchat, time

from itchat.content import *
import os
from exifRename import exifRename

chatRoomNames = ['okiki']     # in the real case we only need okiki
baseDir = "C:\\WORK\\git\\WeChatPhotoDownload\\"  # Change the base folder for each deployed machine
configs = []    # a list of dict each dict item is {'chatroom':chatroom,'folderName':folderName}

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO],isGroupChat=True)
def download_files(msg):
    for item in configs:
        chatroom = item['chatroom']
        if(msg['ToUserName'] == chatroom['UserName'] or msg['FromUserName'] == chatroom['UserName']):
            #print("ToUserName is："+msg['ToUserName'])
            #print("FromUserName is:"+msg['FromUserName'])
            filePath = baseDir+item['folderName']+"\\"
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            msg.download(filePath+msg.fileName)     # download the file 
            exifName = exifRename(filePath+msg.fileName)  #get the new file name based on EXIF(date time)
            if(exifName != msg.fileName):
                os.rename(filePath+msg.fileName,filePath+exifName)  #rename the file based on EXIF or local time info 

# This callback is workable but I don't need it in real case. Good for debugging purpose.
# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     for item in configs:
#         chatroom = item['chatroom']
#         if(msg['ToUserName'] == chatroom['UserName'] or msg['FromUserName'] == chatroom['UserName']):
#             print("From UserName" + msg['FromUserName'])
#             print("To UserName" + msg['ToUserName'])
#             print(msg.isAt)
#             print("Actual NickName"+msg.actualNickName)
#             print("Msg Text" + msg.text)

# Automatically login if been kicked out(time out)
# TODO: if login time exceed a threshold, e.g. 20 times, send out an email to myself.
def exitCallback():
    print("I got disconnected! trying to reconnect")
    itchat.auto_login(hotReload=True,exitCallback=exitCallback)


if __name__ == "__main__":
    itchat.auto_login(hotReload=True,exitCallback=exitCallback)

    for names in chatRoomNames:
        chatrooms = itchat.search_chatrooms(name=names)
        for chatroom in chatrooms:
            configs.append({"chatroom": chatroom,"folderName":chatroom['NickName']})
    

    # print (u'正在监测的群',len(chatrooms),u'个');
    # print(''.join([item['NickName'] for item in chatrooms]))
    # print(''.join([item['UserName'] for item in chatrooms]))
    # print('..........................')
    #print(' '.join([item['chatroom']['NickName'] for item in configs]))
    # print("".join([item['NickName'] for item in items for ]))
    #print(' '.join([item['chatroom']['UserName'] for item in configs]))

    itchat.run(True)

