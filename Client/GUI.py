from Middleware.MessageParsing.MessageParsing import MessageParsing
import numpy as np
from csv import writer
from os import listdir
from os.path import isfile, join
import os
from tkinter import *
import sys

class GUI:
    connectionSystem=""
    messageHandler=""
    communicationManager=""
    groupAdmin=""
    messageParser=""
    UserID=""
    window=""
    SendMessageBox=""
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

        if len(clicked_items) > 0:
            # read in the group files
            fileNames = [f for f in listdir("./Groups"+str(self.UserID)) if isfile(join("./Groups"+str(self.UserID), f))]
            print(self.JoinGroupListBox.get(clicked_items[0]))
            self.CurrentSelectedGroup = self.JoinGroupListBox.get(clicked_items[0])
            print(fileNames)
            # check if group number present, this means the person is a member of the group.
            if str(self.JoinGroupListBox.get(clicked_items[0]))+'.csv' in fileNames:
                # user is in group
                self.displayMessage(str(self.JoinGroupListBox.get(clicked_items[0])))

        else:
            GroupToJoin = self.EnterGroupBox.get()
            self.groupAdmin.joinGroup(str(GroupToJoin),self.UserID)



    def updateGroups(self):
            self.EnterGroupBox.delete(0,END)
            self.JoinGroupListBox.delete('0','end');
            fileNames = [f for f in listdir("./Groups"+str(self.UserID)) if isfile(join("./Groups"+str(self.UserID), f))]
            for index in range(0,len(fileNames)):
                self.JoinGroupListBox.insert(index,str(fileNames[index])[:-4])
            self.JoinGroupListBox.pack()


    # check if userID entered
    # if not then remove this person(leave group)
    # esle if userID entered, check if you have permissions to remove people and remove them
    def removeFromGroup(self):
        print("removal from group")
        clicked_items = self.JoinGroupListBox.curselection()
        self.CurrentSelectedGroup = self.JoinGroupListBox.get(clicked_items[0])
        self.groupAdmin.leaveGroup(str(self.CurrentSelectedGroup),self.UserID)

    def wipeMessages(self):
        self.ViewMessageBox["text"] = "No Group Selected"





    def send_message(self):
        result = self.SendMessageBox.get()
        self.SendMessageBox.delete(0,END)
        self.communicationManager.sendMessage(555,str(result))
        #self.ViewMessageBox["text"] = result
        print(result)

    def displayMessage(self,Group):
        # check if you have this group opened
        if str(Group)==str(self.CurrentSelectedGroup):
            messageDisplay=""
            # open group file and read in currently commiteed messages
            with open('./GroupMessages'+str(self.UserID)+'/'+str(Group)+'.csv', 'r') as f:
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
        fileNames = [f for f in listdir("./Groups"+str(self.UserID)) if isfile(join("./Groups"+str(self.UserID), f))]
        for index in range(0,len(fileNames)):
            self.JoinGroupListBox.insert(index,str(fileNames[index])[:-4])
        self.JoinGroupListBox.pack()

        self.JoinGroupButton = Button(root, text="Join Group", command=self.join_group)
        self.JoinGroupButton.pack()

        button_delete = Button(root, text="Exit Group", command=self.removeFromGroup)
        button_delete.pack()

        messageLabel = Label(root,text="Enter Group Number")
        messageLabel.pack(side ="top" , pady = 5)
        self.EnterGroupBox = Entry(root)
        self.EnterGroupBox.pack(side ="top")

        labelframeMessageViewBox = LabelFrame(root, text="Messages")
        labelframeMessageViewBox.pack(fill="both", expand="yes",side ="top" , pady = 5)

        messageLabel = Label(root,text="Enter message")
        messageLabel.pack(side ="top" , pady = 5)
        self.SendMessageBox = Entry(root)
        self.SendMessageBox.pack(side ="top")

        root.protocol('WM_DELETE_WINDOW', self.exitApplication)



        button_message = Button(root, text="Send", command=self.send_message)
        button_message.pack()

        b3 = Button(root, text='Quit', command=root.quit)
        b3.pack()

        self.ViewMessageBox = Label(labelframeMessageViewBox)
        self.ViewMessageBox.pack(side ="top" , pady = 5)

        self.wipeMessages()

        root.geometry("500x500+200+200")

        root.mainloop()

    def exitApplication(self):
        self.connectionSystem.exitSystem()
        sys.exit()
