from Middleware.MessageParsing.MessageParsing import MessageParsing
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from os import listdir
from os.path import isfile, join
import os



class MessageHandler:

    UserID = '1111111'
    Groups = []
    messageParsing = ""
    groupAdmin = ""

    # default constructor
    def __init__(self,ConnectionSystem):
        self.Groups = [f for f in listdir("./Groups") if isfile(join("./Groups", f))]
        self.messageParsing = MessageParsing()
        self.groupAdmin = GroupAdmin(ConnectionSystem)

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
                return self.groupAdmin.addToGroup(GroupID,PotientialMemberID)

            # Enter here for: Sucessfully Adding a new member to a group
            if MessageType == 2:
                    print("...")




        else:
            return
