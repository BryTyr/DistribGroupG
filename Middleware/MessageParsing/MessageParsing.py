import time


class MessageParsing:

    def parseMessages(Self,message):
        MessageType = int(message[12:13])
        print('Parsed message Type:'+str(MessageType))

        # this parses a join group request
        if MessageType==0:
            print("Do nothing")

        if MessageType==1 or MessageType==2 or MessageType==3 or MessageType==4:
            i = message.find("GroupID:") + 8
            j = message.find(",",i)
            GroupID = message[i:j]
            i = message.find("MemberID:") + 9
            j = message.find(",",i)
            MemberID = message[i:j]
            return GroupID,MemberID
        # received a message parse it
        if MessageType==6 or MessageType==7 or MessageType==8:
            i = message.find("GroupID:") + 8
            j = message.find(",",i)
            GroupID = message[i:j]
            i = message.find("MemberID:") + 9
            j = message.find(",",i)
            MemberID = message[i:j]
            i = message.find("MessageID:") + 10
            j = message.find(",",i)
            MessageID = message[i:j]
            i = message.find("MessageBody:") + 12
            j = message.find(",",i)
            MessageBody = message[i:]
            return GroupID,MemberID,MessageID,MessageBody



    def parseMembersFile(self,line):
            j = line.find(",",0)
            GroupID = line[0:j]
            k = line.find(",",j+1)
            MemberID = line[j+1:k]
            l = line.find(",",k+1)
            AdminLevel = line[k+1:l]
            return GroupID,MemberID,AdminLevel

    def parseActiveMembers(self,memberList):
        print("")
        i = memberList.find("ActiveMemberList:") + 17
        memberList = memberList[i:]
        GroupList = {}
        print("Parsed memeber list: " + memberList)
        while(memberList.find(",")!= -1):
            i = memberList.find(",")
            Member = memberList[:i]
            j = memberList.find(",",i+1)
            Active = memberList[i+1:j]
            GroupList[Member] = Active
            memberList = memberList[j+1:]
            if  memberList.find(";") < 3:
                print(memberList.find(";"))
                break

        print(GroupList)
        return GroupList

    def parsePastMessages(self,message):
            j = message.find(",",0)
            GroupID = message[0:j]
            k = message.find(",",j+1)
            MemberID = message[j+1:k]
            l = message.find(",",k+1)
            AdminLevel = message[k+1:l]
            m = message.find(",",l+1)
            messageID = message[l+1:m]
            n = message.find(",",m+1)
            messageBody = message[m+1:]
            return GroupID,MemberID,AdminLevel,messageID,messageBody
