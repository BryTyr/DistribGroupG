from Middleware.MessageParsing.MessageParsing import MessageParsing
from threading import Thread
from time import sleep
import numpy as np
from csv import writer
from os import listdir
from os.path import isfile, join
import os
import time


class ActiveNodeFlooding:
    MyID = ""
    GroupUpdate = {}
    UpdatingGroupActivity = False
    coolOff = False
    MemberNumbers = 0
    NumberOfUpdates = 0
    connectionSystem = ""
    messageParsing = MessageParsing()

    # default constructor
    def __init__(self,ConnectionSystem,MyID):
        self.connectionSystem = ConnectionSystem
        self.MyID = MyID

    # sends a message to every node to say it is getting an pdated active member list
    def sendUpdateGroupActivity(self,GroupID,MyMemberID):
        print("send im active")
        print("Flooding")
        #
        if self.coolOff == False:
            self.connectionSystem.SendMessage("MessageType:4,GroupID:"+str(GroupID)+",MemberID:"+str(MyMemberID)+",")
        else:
            print("In a cool off period from last flooding process")

    # If a message from the above MessageType is received, the members list is updated
    # and if this is the first received update activity message received in a while then this node also does it
    def receivedGroupActiveUpdate(self,groupID,MemberID):
        print("updating group flooding request")
        if self.coolOff == True:
            print("In cool off from last update")
            return

        # check if currently in a flooding process for a group
        if self.UpdatingGroupActivity == True:
        # if yes update this Group member to active
            self.GroupUpdate[MemberID] = True
        # if no then create the group active dictionary and enter the first update
        else:
            self.GroupUpdate = {}
            # read in group file to create members in update dictionary
            GroupFile = open('./Groups/'+str(groupID)+'.csv', "r")
            row = GroupFile.readlines()
            for line in row:
                GroupID,GroupFileMemberID,AdminLevel = self.messageParsing.parseMembersFile(line)
                # checks to make sure user is not already added to dictionary
                if str(GroupFileMemberID) not in self.GroupUpdate:
                    if str(GroupFileMemberID) == str(MemberID):
                        self.GroupUpdate[GroupFileMemberID] = True
                    else:
                        self.GroupUpdate[GroupFileMemberID] = False
            self.MemberNumbers = len(self.GroupUpdate)
            self.UpdatingGroupActivity=True
            print(self.GroupUpdate)
        # this part checks how many updates has been received for the group
        # if threshold received stop flooding and send final list
        self.NumberOfUpdates+=1
        if self.NumberOfUpdates >= self.MemberNumbers*2:
            self.sendFinalUpdatedList(groupID)
        else:
            self.sendUpdateGroupActivity(groupID,self.MyID)

    # shares its final updated group list with every other node
    def sendFinalUpdatedList(self,groupID):
        print("Send List")
        updatedListMessage = "MessageType:5,GroupID:"+str(groupID)+",MemberID:"+str(self.MyID)+","+"ActiveMemberList:"
        #Final send message to show updated list
        for key, value in self.GroupUpdate.items():
            updatedListMessage = updatedListMessage+str(key)+","+str(value)+","
        # this stops group updating for x time
        updatedListMessage=updatedListMessage+";"
        self.setCoolOffGroupFlooding()
        self.MemberNumbers = 0
        self.NumberOfUpdates = 0
        self.UpdatingGroupActivity=False
        # send final list
        self.connectionSystem.SendMessage(updatedListMessage)

    def compareFinalUpdateLists(self,message):
        print("Compared final update lists: "+message)
        ActiveNodeDict = self.messageParsing.parseActiveMembers(message)
        for key, activeValue in ActiveNodeDict.items():
            print(activeValue)
            Active = self.GroupUpdate.get(key)
            print(Active)
            # add key to dictionary user was not contacted
            if Active == None:
                self.GroupUpdate[key] = activeValue
                continue

            # consensus
            if str(Active) == str(activeValue):
                print('The same value match')
                continue

            # no consusus failure state
            if str(Active) != str(activeValue):
                print('error! consensus not reached')



    # sets a background thread that waits 20 seconds(cool off period) before allowing new group updates
    def setCoolOffGroupFlooding(self):
        self.coolOff = True
        myThread = Thread(target=self.coolOffTimerExpired, args=(20,))
        myThread.start()

    def coolOffTimerExpired(self,seconds):
        sleep(seconds)
        self.coolOff = False
