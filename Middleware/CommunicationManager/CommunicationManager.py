from Middleware.MessageParsing.MessageParsing import MessageParsing
from Middleware.FaultHandling.ActiveNodeFlooding import ActiveNodeFlooding
from threading import Thread
from time import sleep
from os import listdir
from os.path import isfile, join
from csv import writer
import os
import time


class CommunicationManager:
    connectionSystem = ""
    groupAdmin = ""
    GUI=""
    messageParsing = MessageParsing()
    CurrentMessageBody=""
    MyID = ""
    GroupMessaes = {}
    CurrentlySendingMessage = False
    groupActive = ""
    CurrentMessage = ""
    CurrentMessageID = 0
    LastCommitedMessage = 0
    activeNodeFlooding = ""
    ActiveNodesTopology={}
    currentTargetGroupID=""
    ReceivedMessageCount=0
    AbortMessage=False

    currentTargetGroupID=0
    backoffTimer = 5

    GroupActiveMembers = {}

    # default constructor
    def __init__(self,ConnectionSystem,MyID):
        self.connectionSystem = ConnectionSystem
        self.MyID = MyID


    def passGUI(self,GUI):
        self.GUI=GUI

    def setActiveNodeFlooding(self,nodeFlooding):
        self.activeNodeFlooding = nodeFlooding

    def setGroupAdmin(self,groupAdmin):
        self.groupAdmin = groupAdmin


    # sets a background thread that waits 10 seconds before deciding if message to be commited
    def setCountDownToCommit(self):
        myThread = Thread(target=self.countdownExpired, args=(10,))
        myThread.start()

    def countdownExpired(self,seconds):
        sleep(seconds)
        self.checkIfThresholdMet()
    # sets a background thread that waits 10 seconds before deciding if message to be commited
    def setCountDownToUnAbort(self):
        myThread = Thread(target=self.countdownExpiredAbort, args=(30,))
        myThread.start()

    def countdownExpiredAbort(self,seconds):
        sleep(seconds)
        self.AbortMessage=False

    def setAbortMessage(self):
        self.AbortMessage=True
        self.setCountDownToUnAbort()


    def sendMessage(self,TargetGroupID,TargetMessageBody):
        # gets last commited message from file
        with open('./GroupMessages'+str(self.MyID)+'/'+str(TargetGroupID)+'.csv', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            GroupID,MemberID,AdminLevel,messageID,messageBody = self.messageParsing.parsePastMessages(last_line)
            self.groupActive = TargetGroupID
            self.CurrentMessage = "MessageType:6,GroupID:"+str(TargetGroupID)+",MemberID:"+str(self.MyID)+","+"MessageID:"+str(int(messageID)+1)+","+"MessageBody:"+str(TargetMessageBody)
        self.currentTargetGroupID = TargetGroupID
        self.CurrentMessageBody=TargetMessageBody

        # send message with Updated id
        self.activeNodeFlooding.sendUpdateGroupActivity(TargetGroupID,self.MyID)
        time.sleep(3.0)
        self.ActiveNodesTopology = self.activeNodeFlooding.getActiveNodeDict()
        self.setCountDownToCommit()

        self.CurrentlySendingMessage = True
        self.LastCommitedMessage = int(messageID)
        self.CurrentMessageID = int(messageID)+1
        #send message to system
        self.connectionSystem.SendMessage("MessageType:6,GroupID:"+str(TargetGroupID)+",MemberID:"+str(self.MyID)+","+"MessageID:"+str(int(messageID)+1)+","+"MessageBody:"+str(TargetMessageBody))



    # reads the last line of its commit log
    # if the id is 1 ahead the nit says ready to commit
    # else if say no
    def ReceivedMessage(self,message):
        print("received message")
        if self.AbortMessage==True:
            return
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
                    print("Inside message sending")
                    # if not then check your ready to commit and send a response
                    with open('./GroupMessages'+str(self.MyID)+'/'+str(ReceivedGroupID)+'.csv', 'r') as f:
                        lines = f.read().splitlines()
                        last_line = lines[-1]
                        GroupID,MemberID,AdminLevel,messageID,messageBody = self.messageParsing.parsePastMessages(last_line)

                    self.LastCommitedMessage = int(messageID)

                    # Message matches current ID ready to commit it
                    time.sleep(3.0)
                    #received a message for an already commited message
                    print("Last Commited Message Numbers")
                    print(self.LastCommitedMessage)
                    print(ReceivedmessageID)
                    print(self.AbortMessage)

                    if self.LastCommitedMessage == int(ReceivedmessageID) or self.AbortMessage==True:
                        return

                    if int(messageID)+1 == int(ReceivedmessageID) :
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
            self.GroupActiveMembers[MemberID] = False


    # checks if the threshold met and if so then commit else reset everything
    def checkIfThresholdMet(self):
        LengthOfGroup = len(self.GroupActiveMembers)
        print(LengthOfGroup)
        positiveResponses = 1
        negitiveResponses = 0
        ActiveNodes = 0
        # reset boolean
        self.ActiveNodesTopology = self.activeNodeFlooding.getActiveNodeDict()
        print(len(self.ActiveNodesTopology))
        self.CurrentlySendingMessage = False
        print("Amount of recorded members")
        print(self.GroupActiveMembers)
        for key,value in self.GroupActiveMembers.items():
            print(key)
            print(value)
            if str(value) == str(True):
                positiveResponses+=1
            if str(value) == str(False):
                negitiveResponses+=1

        # get number of active nodes
        with open('./GroupLog/GroupLog.csv', 'a+') as write_obj:
            print("OpenedgroupLog")
            for key,value in self.ActiveNodesTopology.items():
                csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
                NewUser=[]
                NewUser.append(str(self.groupActive))
                NewUser.append(str(key))
                if str(value) == str(True):
                    NewUser.append("Active")
                else:
                    NewUser.append("Inactive")
                csv_writer.writerow(NewUser)
                csv_writer.writerow("")


        for key,value in self.ActiveNodesTopology.items():
            print(key)
            print(value)
            # Add contents of list as last row in the csv file

            if str(value) == str(True):
                ActiveNodes+=1


        #print(positiveResponses)
        #print(ActiveNodes)
        #minority check
        if negitiveResponses > 0:
            print("In minority")
            self.groupAdmin.sendMessageFile(self.currentTargetGroupID)
            self.AbortMessage=True
            self.setAbortMessage()
            self.connectionSystem.SendMessage("MessageType:15,GroupID:"+str(self.currentTargetGroupID)+",MemberID:"+str(self.MyID)+",")
            print("......................................................................................")
            print("\n\n\n\n\n\n\n\n\n\n")
            print("A node remerging occured please refresh and send message again")
            print("......................................................................................")
            time.sleep(15.0)

            print("..................................................")
            print("Refresh now")
            # self.AbortMessage=True
            # self.setAbortMessage()
            # self.connectionSystem.SendMessage("MessageType:15,GroupID:"+str(self.currentTargetGroupID)+",MemberID:"+str(self.MyID)+",")
            #self.connectionSystem.SendMessage(self.CurrentMessage)
            #self.sendMessage(self.currentTargetGroupID,self.CurrentMessageBody)
            return
            #send message to system
            #self.connectionSystem.SendMessage(self.CurrentMessage)


        #
        # check for majority also timeout print failed due to not majority, return to break
        #
        # add in backoff of 5 seconds per failure
        #

        GroupFile = open('./Groups'+str(self.MyID)+'/'+str(self.currentTargetGroupID)+'.csv', "r")
        row = GroupFile.readlines()
        GroupLength = len(row)
        print("................................................................................................................................")
        print("Partition check")
        print("Number of total nodes in the group: "+str(GroupLength))
        print("Number of Nodes currently active: "+str(ActiveNodes))
        print("................................................................................................................................")

        majority = (GroupLength/2) + 1
        print(ActiveNodes)
        print(majority)
        print(positiveResponses)
        #--------------------------------------------------------------------

        if (ActiveNodes >= int(majority)) and (positiveResponses == ActiveNodes):
            self.backoffTimer = 5
            print("\n\n\n\n\n\n\n")
            print("Commit Sucessful")
            print(self.CurrentMessage)
            # reset to zero
            self.GroupActiveMembers={}
            self.commitMessage(self.CurrentMessage)
        else:
            print("Not enough positive responses aborting commit")
            sleep(self.backoffTimer)
            if self.backoffTimer < 30:
                self.backoffTimer += 5
            print("Not enough positive responses aborting commit")


    def commitMessage(self,currentMessage):

        GroupID,MemberID,messageID ,MessageBody = self.messageParsing.parseMessages(currentMessage)

        with open('./GroupMessages'+str(self.MyID)+'/'+str(GroupID)+'.csv', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            ParsedGroupID,ParsedMemberID,AdminLevel,ParsedMessageID,ParsedMessageBody = self.messageParsing.parsePastMessages(last_line)
        self.LastCommitedMessage = ParsedMessageID

        print(int(messageID))
        print(self.LastCommitedMessage)

        if int(self.LastCommitedMessage) <= int(messageID) and int(self.LastCommitedMessage)+1 == (int(messageID)):

            print("commited")
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
            self.LastCommitedMessage = int(messageID)
            print(self.LastCommitedMessage)

            self.connectionSystem.SendMessage("MessageType:14,GroupID:"+str(GroupID)+",MemberID:"+str(self.MyID)+","+"MessageID:"+str(int(self.CurrentMessageID))+","+"MessageBody:"+str(MessageBody))
            self.GUI.displayMessage(GroupID)

        else:
            return


    def displayMessages(self,GroupID):
        Messages = []
        GroupFile = open('./GroupMessages'+str(self.MyID)+'/'+str(GroupID)+'.csv', "r")
        row = GroupFile.readlines()
        for line in row:
            GroupID,MemberID,AdminLevel,messageID,messageBody = self.messageParsing.parsePastMessages(line)
            Messages.append([MemberID,AdminLevel,messageBody])
        print(Messages)
