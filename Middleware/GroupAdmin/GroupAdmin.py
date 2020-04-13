from Middleware.MessageParsing.MessageParsing import MessageParsing
import numpy as np
from csv import writer
from os import listdir
from os.path import isfile, join
import os
import time
import csv



class GroupAdmin:
    connectionSystem = ""
    messageParsing = MessageParsing()
    UserID = ""

    # default constructor
    def __init__(self,ConnectionSystem,userID):
        self.connectionSystem = ConnectionSystem
        self.UserID = userID

    # method to ask to join a group
    def joinGroup(self,groupID,PotientialMemberID):
        Response = self.connectionSystem.SendMessage("MessageType:1,GroupID:"+str(groupID)+",MemberID:"+str(PotientialMemberID)+",")
        # Response = self.connectionSystem.ReceiveMessages()
        print("Check1"+str(Response))
        MessageID = Response[12:13]
        groupID,MyMemberID = self.messageParsing.parseMessages(Response)
        if str(PotientialMemberID) in str(MyMemberID) and MessageID in "2":
            print("Sucess Joined Group: "+str(groupID))
        else:
            # This can occur if the member has already joined
            print("Failed to join group, check with Admin ")



    # method to ask to join a group
    # Use MasterUserId Instead of 12345 ---Now Chnanged in line 39
    def addToGroup(self,groupID,PotientialMemberID,MasterUserId):
        #check if user has access to add members
        Access = self.CheckPrivligages(groupID,MasterUserId)

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

    # method to leave a group (User wants to resign)
    def leaveGroup(self,GroupID,MemberID):
            lines= list()
            #GroupFile = open('./Groups/'+str(groupID)+'.csv', "r")
            readfile = open('./Groups/'+str(GroupID)+'.csv', 'r')
            reader = readfile.readlines()
            for row in reader:
                groupID_No_Use,memberID_No_Use,AdminLevel = self.messageParsing.parseMembersFile(row)
                if str(MemberID) not in str(memberID_No_Use) or str(AdminLevel) == "2":
                    lines.append(row)


            writeFile1 = open('./Groups/'+str(GroupID)+'.csv', 'w')
            writeFile1.writelines(lines)
            #writer.writerows(lines)
            print("Member Left the Group")
            time.sleep(3.0)
            return "MessageType:9,GroupID:"+str(GroupID)+",MemberID:"+str(MemberID)+","



    # method to leave a group (Admin(Rank 0 or Rank 1) removes the user from a group)
    def removeFromGroup(self,GroupID,LeavingMemberID,MasterUserId):
        print("Checking Access Level")
        Access = self.CheckPrivligages(GroupID,MasterUserId)
        if Access == True :
            lines= list()
            #GroupFile = open('./Groups/'+str(groupID)+'.csv', "r")
            readfile = open('./Groups/'+str(GroupID)+'.csv', 'r')
            reader = readfile.readlines()
            for row in reader:
                groupID_No_Use,memberID_No_Use,AdminLevel = self.messageParsing.parseMembersFile(row)
                if str(LeavingMemberID) not in str(memberID_No_Use) or str(AdminLevel) == "2":
                    lines.append(row)


            writeFile1 = open('./Groups/'+str(GroupID)+'.csv', 'w')
            writeFile1.writelines(lines)

            if(str(AdminLevel) == "2"):
                print("Creator cannot be removed")
            else:
                print("Member "+str(LeavingMemberID)+" has been removed from the Group by "+str(MasterUserId))
                time.sleep(3.0)
                return "MessageType:10,GroupID:"+str(GroupID)+",MemberID:"+str(LeavingMemberID)+","

        else:
            print("No access rights contact an admin")




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


    def CreateNewGroup(self,PotantialGroupID,MemberID):

        filenames = [f for f in listdir("./Groups") if isfile(join("./Groups", f))]
        if str(PotantialGroupID)+ '.csv' in filenames:
            print("Group Already Exists. Change the Name/Id of the Group")
        else:
                with open('./Groups/'+str(PotantialGroupID)+'.csv', 'w') as writeFile:
                    fieldnames = ['GroupID','MemberID','MemberRank','Action']
                    writer1 = csv.DictWriter(writeFile, fieldnames)
                    writer1.writeheader()
                    writer1.writerow({'GroupID':''+str(PotantialGroupID)+'','MemberID':''+str(MemberID)+'','MemberRank':'2','Action':'CREATED'})

                    with open('./Groups/GroupLog.csv', 'a+') as write_obj:
                        # Create a writer object from csv module
                        csv_writer = writer(write_obj)
                        # Add contents of list as last row in the csv file
                        NewUser=[]
                        NewUser.append(str(PotantialGroupID))
                        NewUser.append(str(MemberID))
                        #NewUser.append("0")
                        NewUser.append("CREATED")
                        csv_writer.writerow(NewUser)

                    print("Successfully created the Group")
                    time.sleep(3.0)
                    return "MessageType:11,GroupID:"+str(PotantialGroupID)+",MemberID:"+str(MemberID)+","

    def DeleteExistingGroup(self,ToBeDeletedGroupId,ReqesterMemberID):

        filenames = [f for f in listdir("./Groups") if isfile(join("./Groups", f))]

        if str(ToBeDeletedGroupId)+ '.csv' in filenames:
                lines= list()

                with open('./Groups/'+str(ToBeDeletedGroupId)+'.csv', 'r') as readFile:
                    reader = readFile.readlines()

                    for row in reader:
                        groupID_No_Use,memberID_No_Use,AdminLevel = self.messageParsing.parseMembersFile(row)
                        #Group creater cannot leave the group
                        if str(AdminLevel) != "2":
                            #reader.close()
                            Accesslevel = True

                if Accesslevel == True :
                    os.remove('./Groups/'+str(ToBeDeletedGroupId)+'.csv')
                    with open('./Groups/GroupLog.csv', 'a+') as write_obj:
                        # Create a writer object from csv module
                        csv_writer = writer(write_obj)
                        # Add contents of list as last row in the csv file
                        NewUser=[]
                        NewUser.append(str(ToBeDeletedGroupId))
                        NewUser.append(str(ReqesterMemberID))
                        #NewUser.append("0")
                        NewUser.append("DELETED")
                        csv_writer.writerow(NewUser)
                        print("Successfully deleted the Group")
                        time.sleep(3.0)
                        return "MessageType:12,GroupID:"+str(ToBeDeletedGroupId)+",MemberID:"+str(ReqesterMemberID)+","
                else:
                    print("You are not allowed to leave this group since you are the creator")


        else:
                print("Group does not Exist. Please enter valid group number")
