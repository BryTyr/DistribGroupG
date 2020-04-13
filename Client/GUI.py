from Middleware.MessageParsing.MessageParsing import MessageParsing
import numpy as np
from csv import writer
from os import listdir
from os.path import isfile, join
import os
from tkinter import *

class GUI:
    connectionSystem=""
    messageHandler=""
    communicationManager=""
    groupAdmin=""
    messageParser=""
    UserID=""
    window=""
    SendMessageButton=""
    SendMessageBox=""
    JoinGroupButton=""
    JoinGroupListBox=""
    ViewMessageBox=""
    CurrentSelectedGroup=""

    def __init__(self,ConnectionSystem,UserID):
        print("setup")
        self.connectionSystem = ConnectionSystem
        self.messageHandler = self.connectionSystem.returnMessageHandler()
        self.communicationManager = self.connectionSystem.returnCommunicationManager()
        self.groupAdmin = self.messageHandler.returnGroupAdmin()
        self.messageParser = MessageParsing()
        self.UserID=UserID
        self.window = Tk()
        #self.setUp_Window()


    # check if you have already Joined
    # if not then request to join
    # if you have joined show last 5 messages
    def join_group(self):
        #group selected
        clicked_items = self.JoinGroupListBox.curselection()
        # read in the group files
        fileNames = [f for f in listdir("./Groups") if isfile(join("./Groups", f))]
        print(self.JoinGroupListBox.get(clicked_items[0]))
        self.CurrentSelectedGroup = self.JoinGroupListBox.get(clicked_items[0])
        print(fileNames)
        # check if group number present, this means the person is a member of the group. Else not in the group and send a request to join
        if str(self.JoinGroupListBox.get(clicked_items[0]))+'.csv' in fileNames:
            # user is in group
            self.displayMessage(str(self.JoinGroupListBox.get(clicked_items[0])))

        else:
            self.groupAdmin.joinGroup(str(self.JoinGroupListBox.get(clicked_items[0])),self.UserID)



    def send_message(self):
        result = self.SendMessageButton.get()
        self.communicationManager.sendMessage(555,str(result))
        #self.ViewMessageBox["text"] = result
        self.SendMessageButton.delete(0,END)
        print(result)

    def displayMessage(self,Group):
        # check if you have this group opened
        if str(Group)==str(self.CurrentSelectedGroup):
            messageDisplay=""
            # open group file and read in currently commiteed messages
            with open('./GroupMessages/'+str(Group)+'.csv', 'r') as f:
                lines = f.read().splitlines()
                # ifn more then 5 messages show last 5 messages else show all messages
                print(len(lines))
                if len(lines) > 5:
                    for index in range(len(lines)-5,len(lines)):
                        GroupID,MemberID,AdminLevel,messageID,messageBody = self.messageParser.parsePastMessages(lines[index])
                        messageDisplay=messageDisplay+"Member: "+str(MemberID)+" Message: "+str(messageBody)+"\n"
                else:
                    for line in lines:
                        GroupID,MemberID,AdminLevel,messageID,messageBody = self.messageParser.parsePastMessages(line)
                        messageDisplay=messageDisplay+"Member: "+str(MemberID)+" Message: "+str(messageBody)+"\n"

                self.ViewMessageBox["text"] = messageDisplay

        #else:
            #print("Message updated but this group is not currently selected")

        #print("message displayed")

    def exit_group(self):
        print("exited")


    def setUp_Window(self):
        root = self.window
        self.JoinGroupListBox = Listbox(root, width=20, height=10, selectmode= EXTENDED)
        fileNames = [f for f in listdir("./Groups") if isfile(join("./Groups", f))]
        for index in range(0,len(fileNames)):
            self.JoinGroupListBox.insert(index,str(fileNames[index])[:-4])
        self.JoinGroupListBox.pack()

        self.JoinGroupButton = Button(root, text="Join Group", command=self.join_group)
        self.JoinGroupButton.pack()

        button_delete = Button(root, text="Exit Group", command=self.exit_group)
        button_delete.pack()

        labelframeMessageViewBox = LabelFrame(root, text="Messages")
        labelframeMessageViewBox.pack(fill="both", expand="yes",side ="top" , pady = 5)

        messageLabel = Label(root,text="Enter message")
        messageLabel.pack(side ="top" , pady = 5)
        self.SendMessageButton = Entry(root)
        self.SendMessageButton.pack(side ="top")


        button_message = Button(root, text="Send", command=self.send_message)
        button_message.pack()

        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack()

        self.ViewMessageBox = Label(labelframeMessageViewBox)
        self.ViewMessageBox.pack(side ="top" , pady = 5)

        root.geometry("500x500+200+200")

        root.mainloop()
