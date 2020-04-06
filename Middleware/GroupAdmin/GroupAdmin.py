from Middleware.MessageParsing.MessageParsing import MessageParsing
import numpy as np
from csv import writer
from os import listdir
from os.path import isfile, join
import os
import time


class GroupAdmin:
    connectionSystem = ""
    messageParsing = MessageParsing()

    # default constructor
    def __init__(self,ConnectionSystem):
        self.connectionSystem = ConnectionSystem

    # method to ask to join a group
    def joinGroup(self,groupID,PotientialMemberID):
        Response = self.connectionSystem.SendMessage("MessageType:1,GroupID:"+str(groupID)+",MemberID:"+str(PotientialMemberID)+",")
        # Response = self.connectionSystem.ReceiveMessages()
        print(Response)
        MessageID = Response[12:13]
        groupID,MyMemberID = self.messageParsing.parseMessages(Response)
        if str(PotientialMemberID) in str(MyMemberID) and MessageID in "2":
            print("Sucess Joined Group: "+str(groupID))
        else:
            # This can occur if the member has already joined
            print("Failed to join group, check with Admin ")



    # method to ask to join a group
    def addToGroup(self,groupID,PotientialMemberID):
        #check if user has access to add members
        Access = self.CheckPrivligages(groupID,'12345')

        if Access == True:
            # cehck if member not already added
            GroupFile = open('./Groups/'+str(groupID)+'.csv', "r")
            row = GroupFile.readlines()
            for line in row:
                i = line.find(",") + 1
                j = line.find(",",i)
                MemberID = line[i:j]
                if MemberID == PotientialMemberID:
                    print('Member already Added!')
                    return "MessageType:3,GroupID:"+str(groupID)+",MemberID:"+str(PotientialMemberID)+","

            #add member to group
            # Open file in append mode
            with open('./Groups/'+str(groupID)+'.csv', 'a+', newline='') as write_obj:
                # Create a writer object from csv module
                csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
                NewUser=[]
                NewUser.append(str(groupID))
                NewUser.append(str(PotientialMemberID))
                NewUser.append("0")
                NewUser.append("JOIN")
                csv_writer.writerow(NewUser)
                print("added new Member")
                time.sleep(3.0)
                return "MessageType:2,GroupID:"+str(groupID)+",MemberID:"+str(PotientialMemberID)+","

        else:
            print("No access rights contact an admin")

    # method to leave a group
    def leaveGroup(self):
        print("left")

    # method to leave a group
    def removeFromGroup(self):
        print("Removed")


    def CheckPrivligages(self,GroupId,MyMemberID):
        # read in the group files
        fileNames = [f for f in listdir("./Groups") if isfile(join("./Groups", f))]
        # check if group number present, this means the person is a member of the group
        if str(GroupId)+'.csv' in fileNames:
            # check if this user has privigages
            # if user does return true else false
            GroupFile = open('./Groups/'+str(GroupId)+'.csv', "r")
            row = GroupFile.readlines()
            for line in row:
                groupID,memberID,AdminLevel = self.messageParsing.parseMembersFile(line)
                if str(MyMemberID) in str(memberID) and str(AdminLevel) != "0":
                    return True
            return False
        else:
            return False
