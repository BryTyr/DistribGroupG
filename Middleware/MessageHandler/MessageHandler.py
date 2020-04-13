from Middleware.MessageParsing.MessageParsing import MessageParsing
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from Middleware.FaultHandling.ActiveNodeFlooding import ActiveNodeFlooding
from Middleware.CommunicationManager.CommunicationManager import CommunicationManager
from os import listdir
from os.path import isfile, join
import os



class MessageHandler:

    UserID = ""
    Groups = []
    messageParsing = ""
    groupAdmin = ""
    activeNodeFlooding = ""
    communicationManager = ""

    # default constructor
    def __init__(self,ConnectionSystem,communicationManager,UserID):
        self.Groups = [f for f in listdir("./Groups") if isfile(join("./Groups", f))]
        self.messageParsing = MessageParsing()
        self.groupAdmin = GroupAdmin(ConnectionSystem,UserID)
        self.activeNodeFlooding = ActiveNodeFlooding(ConnectionSystem,UserID)
        #self.communicationManager = CommunicationManager(ConnectionSystem,UserID)
        self.communicationManager = communicationManager

    def handleMessage(self,message):
        # Parse the Message
        i = message.find("GroupID:") + 8
        j = message.find(",",i)
        GroupID = message[i:j]

        # check if this user is part of this group else ignore
        if str(GroupID)+".csv" in self.Groups:
             # This gets the type of message
            MessageType = int(message[12:13])

            # Enter here for: Adding new members to a group
            if MessageType == 1:
                GroupID,PotientialMemberID = self.messageParsing.parseMessages(message)
                self.groupAdmin.addToGroup(GroupID,PotientialMemberID)

            # Enter here for: Sucessfully Adding a new member to a group
            if MessageType == 2:
                GroupID,JoiningMemberID = self.messageParsing.parseMessages(message)
                self.groupAdmin.JoinGroupResponse(2,GroupID,JoiningMemberID)

            # Enter here for: Failed to Add a new member to a group
            if MessageType == 3:
                GroupID,JoiningMemberID = self.messageParsing.parseMessages(message)
                self.groupAdmin.JoinGroupResponse(3,GroupID,JoiningMemberID)

            # this calls when a group update is occuring
            if MessageType == 4:
                    GroupID,MemberID = self.messageParsing.parseMessages(message)
                    self.activeNodeFlooding.receivedGroupActiveUpdate(GroupID,MemberID)

            # final updating of a group flooding
            if MessageType == 5:
                    self.activeNodeFlooding.compareFinalUpdateLists(message)

            # Received a text message from a group member
            if MessageType == 6:
                self.communicationManager.ReceivedMessage(message)

            # final updating of a group flooding
            if MessageType == 7:
                self.communicationManager.ReceivedMessage(message)

            # final updating of a group flooding
            if MessageType == 8:
                self.communicationManager.ReceivedMessage(message)


        else:
            return

    def returnGroupAdmin(self):
        return self.groupAdmin
