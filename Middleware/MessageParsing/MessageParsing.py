


class MessageParsing:

    def parseMessages(Self,message):
        MessageType = int(message[12:13])
        print('Parsed message Type:'+str(MessageType))

        # this parses a join group request
        if MessageType==1:
            i = message.find("GroupID:") + 8
            j = message.find(",",i)
            GroupID = message[i:j]
            i = message.find("MemberID:") + 9
            j = message.find(",",i)
            MemberID = message[i:j]
            return GroupID,MemberID

        # the is a join group confirmation request
        if MessageType==2:
            i = message.find("GroupID:") + 8
            j = message.find(",",i)
            GroupID = message[i:j]
            i = message.find("MemberID:") + 9
            j = message.find(",",i)
            MemberID = message[i:j]
            return GroupID,MemberID


    def parseMembersFile(self,line):
            print(line)
            j = line.find(",",0)
            GroupID = line[0:j]
            k = line.find(",",j+1)
            MemberID = line[j+1:k]
            l = line.find(",",k+1)
            AdminLevel = line[k+1:l]
            return GroupID,MemberID,AdminLevel
