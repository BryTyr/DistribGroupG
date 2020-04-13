from Middleware.MessageParsing.MessageParsing import MessageParsing
from threading import Thread
from time import sleep
from os import listdir
from os.path import isfile, join
from csv import writer
import os
import time


class CommunicationManager:
    connectionSystem = ""
    GUI=""
    messageParsing = MessageParsing()
    MyID = ""
    GroupMessaes = {}
    CurrentlySendingMessage = False
    groupActive = ""
    CurrentMessage = ""


    GroupActiveMembers = {}

    # default constructor
    def __init__(self,ConnectionSystem,MyID):
        self.connectionSystem = ConnectionSystem
        self.MyID = MyID


    def passGUI(self,GUI):
        self.GUI=GUI


    # sets a background thread that waits 10 seconds before deciding if message to be commited
    def setCountDownToCommit(self):
        myThread = Thread(target=self.countdownExpired, args=(10,))
        myThread.start()

    def countdownExpired(self,seconds):
        sleep(seconds)
        self.checkIfThresholdMet()



    def sendMessage(self,TargetGroupID,TargetMessageBody):
        # gets last commited message from file
        with open('./GroupMessages'+str(self.MyID)+'/'+str(TargetGroupID)+'.csv', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            GroupID,MemberID,AdminLevel,messageID,messageBody = self.messageParsing.parsePastMessages(last_line)
            self.CurrentlySendingMessage = True
            self.groupActive = TargetGroupID
            self.CurrentMessage = "MessageType:6,GroupID:"+str(TargetGroupID)+",MemberID:"+str(self.MyID)+","+"MessageID:"+str(int(messageID)+1)+","+"MessageBody:"+str(TargetMessageBody)
            self.setCountDownToCommit()
        # send message with Updated id
        self.connectionSystem.SendMessage("MessageType:6,GroupID:"+str(TargetGroupID)+",MemberID:"+str(self.MyID)+","+"MessageID:"+str(int(messageID)+1)+","+"MessageBody:"+str(TargetMessageBody))


    # reads the last line of its commit log
    # if the id is 1 ahead thenit says ready to commit
    # else if say no
    def ReceivedMessage(self,message):
        print("here")
        # parses the current received message
        ReceivedGroupID,ReceivedMemberID,ReceivedmessageID,MessageBody = self.messageParsing.parseMessages(message)

        # check if you are part of this group
        GroupFile = open('./Groups'+str(self.MyID)+'/'+str(ReceivedGroupID)+'.csv', "r")
        row = GroupFile.readlines()
        for line in row:
            groupID,memberID,AdminLevel = self.messageParsing.parseMembersFile(line)
            if str(memberID) in str(self.MyID):
                print("inside joined groups: part of this group")
                # if you are part of the group check if you sent this message if not enter this loop
                if self.CurrentlySendingMessage == False:
                    print("Inside currently sending message")
                    # if not then check your ready to commit and send a response
                    with open('./GroupMessages'+str(self.MyID)+'/'+str(ReceivedGroupID)+'.csv', 'r') as f:
                        lines = f.read().splitlines()
                        last_line = lines[-1]
                        GroupID,MemberID,AdminLevel,messageID,messageBody = self.messageParsing.parsePastMessages(last_line)

                    # Message matches current ID ready to commit it
                    time.sleep(2.0)
                    if int(messageID)+1 == int(ReceivedmessageID):
                        self.connectionSystem.SendMessage("MessageType:7,GroupID:"+str(GroupID)+",MemberID:"+str(self.MyID)+","+"MessageID:"+str(int(ReceivedmessageID))+","+"MessageBody:"+str(MessageBody))
                        return
                    else:
                        self.connectionSystem.SendMessage("MessageType:8,GroupID:"+str(GroupID)+",MemberID:"+str(self.MyID)+","+"MessageID:"+str(int(ReceivedmessageID))+","+"MessageBody:"+str(MessageBody))
                        return
                # else if you did send the initial message update your received messages with true or false
                else:
                    print("indide commit thresholds")
                    self.addToCommitThreshold(message)


    def addToCommitThreshold(self,message):

        GroupID,MemberID,MessageID,MessageBody = self.messageParsing.parseMessages(message)
        MessageType = int(message[12:13])
        # if 7 then the user who replid is ready to commit the message
        if MessageType == 7:
            print("commit ready from: "+MemberID)
            self.GroupActiveMembers[MemberID] = True
            #self.displayMessages(GroupID)
        # if 8 then the user who replid is wanting to abort the message
        if MessageType == 8:
            print("not ready from member: "+MemberID)


    # checks if the threshold met and if so then commit else reset everything
    def checkIfThresholdMet(self):
        LengthOfGroup = len(self.GroupActiveMembers)
        positiveCount = 0
        # reset boolean
        self.CurrentlySendingMessage = False
        print("Amount of recorded members")
        print(self.GroupActiveMembers)
        for key,value in self.GroupActiveMembers.items():
            print(key)
            print(value)
            if str(value) == str(True):
                positiveCount+=1

        print(positiveCount)
        print(LengthOfGroup)
        if str(positiveCount) == str(LengthOfGroup):
            print("Commit Sucessful")
            self.commitMessage()
        else:
            print("Not enough positive responses aborting commit")


    def commitMessage(self):
        print("commited")
        GroupID,MemberID,messageID ,MessageBody = self.messageParsing.parseMessages(self.CurrentMessage)

        with open('./GroupMessages'+str(self.MyID)+'/'+str(GroupID)+'.csv', 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            NewMessage=[]
            NewMessage.append(str(GroupID))
            NewMessage.append(str(MemberID))
            NewMessage.append('0')
            NewMessage.append(messageID)
            NewMessage.append(MessageBody)
            csv_writer.writerow(NewMessage)
            print("added new Message")
        self.GUI.displayMessage(GroupID)


    def displayMessages(self,GroupID):
        Messages = []
        GroupFile = open('./GroupMessages'+str(self.MyID)+'/'+str(GroupID)+'.csv', "r")
        row = GroupFile.readlines()
        for line in row:
            GroupID,MemberID,AdminLevel,messageID,messageBody = self.messageParsing.parsePastMessages(line)
            Messages.append([MemberID,AdminLevel,messageBody])
        print(Messages)
